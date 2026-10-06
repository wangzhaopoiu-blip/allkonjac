"""Audit generated pages and local destinations without a browser or deployment."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, re, hashlib, sys
import xml.etree.ElementTree as ET
from build import BASE, PAGES, LANGUAGES, page_path, page_url, validate_output

ROOT=Path(__file__).resolve().parents[1]
class Document(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.tags=[]; self.feed(text)
    def handle_starttag(self,tag,attrs): self.tags.append((tag,dict(attrs)))

def audit():
    errors=[]; records=[]; documents={}
    for lang in LANGUAGES:
        for page in PAGES:
            path=page_path(page,lang); source=(ROOT/path.strip('/')/'index.html').read_text(encoding='utf-8')
            try: validate_output(source,page,lang)
            except Exception as e: errors.append(f'{path}: {e}')
            documents[path]=(source,Document(source))
    for path,(source,doc) in documents.items():
        tags=doc.tags
        if '{{' in source: errors.append(f'{path}: unresolved source token')
        if len([1 for tag,_ in tags if tag=='h1'])!=1: errors.append(f'{path}: h1 count')
        if not re.search(r'<title>[^<]+</title>',source): errors.append(f'{path}: missing title')
        descriptions=[a for t,a in tags if t=='meta' and a.get('name')=='description']
        if len(descriptions)!=1 or not descriptions[0].get('content'): errors.append(f'{path}: missing description')
        for tag,attrs in tags:
            if tag=='img' and ('alt' not in attrs or (not attrs['alt'] and attrs.get('aria-hidden')!='true')):
                errors.append(f'{path}: missing image alt or decorative-image annotation')
            for field in ['src','href']:
                if field not in attrs: continue
                url=attrs[field]; parsed=urlsplit(url)
                if parsed.scheme or parsed.netloc: continue
                destination=parsed.path or path
                if not destination.startswith('/'): errors.append(f'{path}: relative local URL {url}'); continue
                target=(ROOT/unquote(destination).lstrip('/'))
                if target.is_dir(): target=target/'index.html'
                if not target.exists(): errors.append(f'{path}: missing destination {url}'); continue
                if parsed.fragment and target.suffix=='.html':
                    targetdoc=Document(target.read_text(encoding='utf-8'))
                    if parsed.fragment not in {a.get('id') for _,a in targetdoc.tags}: errors.append(f'{path}: missing fragment {url}')
        records.append({'path':path,'language':next(a['lang'] for t,a in tags if t=='html'),'images':sum(t=='img' for t,_ in tags),'links':sum(t=='a' for t,_ in tags),'static_checks':'passed'})
    namespace='{http://www.sitemaps.org/schemas/sitemap/0.9}'
    sitemap=ET.fromstring((ROOT/'sitemap.xml').read_text(encoding='utf-8'))
    locations=[n.find(namespace+'loc').text for n in sitemap.findall(namespace+'url')]
    expected={page_url(p,l) for p in PAGES for l in LANGUAGES}
    if set(locations)!=expected or len(locations)!=15: errors.append('Sitemap URL set differs from fifteen canonical pages')
    llms=(ROOT/'llms.txt').read_text(encoding='utf-8')
    if any(url not in llms for url in expected): errors.append('AI content index misses a language page')
    for lang in ['th','id']:
        en=json.loads((ROOT/'content/en.json').read_text(encoding='utf-8'))
        locale=json.loads((ROOT/f'content/{lang}.json').read_text(encoding='utf-8'))
        if set(en)!=set(locale): errors.append(f'{lang}: translation keys differ')
        for key,value in locale.items():
            if re.search(r'\[\d{4}\]',value): errors.append(f'{lang}: retained batch marker {key}')
            shared={'WhatsApp: +86 156 3713 6906'}
            if lang=='id': shared.update({'Menu','Email','Email: 583411495@qq.com'})
            if value==en[key] and en[key] not in shared: errors.append(f'{lang}: unchanged English string {key}')
        forbidden=['หมากฝรั่ง','แอปพลิเคชัน','เครื่องอบผ้า','บุกบุก'] if lang=='th' else ['permen karet','SEMUA KONJ','Remah roti','lamaran','Garis Pengeringan','bubuk halus']
        for word in forbidden:
            if any(word in v for v in locale.values()): errors.append(f'{lang}: unreviewed draft term {word}')
    notfound=(ROOT/'404.html').read_text(encoding='utf-8')
    if not all(f'lang="{lang}"' in notfound for lang in LANGUAGES) or 'noindex,follow' not in notfound: errors.append('404 language or noindex missing')
    config=json.loads((ROOT/'wrangler.jsonc').read_text(encoding='utf-8-sig'))
    if config['assets']['not_found_handling']!='404-page': errors.append('404 hosting setting changed')
    font=ROOT/'assets/fonts/NotoSansThai-variable.ttf'
    if not font.exists() or not (font.parent/'OFL.txt').exists(): errors.append('Local Thai font or license missing')
    motion_pages=[path for path,(_,doc) in documents.items() if any(tag=='body' and 'motion-enabled' in attrs.get('class','').split() for tag,attrs in doc.tags)]
    report={'business_pages':15,'strings_per_language':233,'sitemap_urls':len(locations),'motion_enabled_pages':motion_pages,'records':records,'errors':errors,'font_sha256':hashlib.sha256(font.read_bytes()).hexdigest(),'browser_checks':'local preview blocked by saved permission; production browser checks recorded separately','hosting_response_checks':'production HTTP verification is recorded separately in the release report'}
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return len(errors)

if __name__=='__main__': sys.exit(bool(audit()))
