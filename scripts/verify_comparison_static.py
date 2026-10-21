from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote, urljoin
import json
import re
from check_language_policy import check

ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=set()
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.add(attrs['id'])
        self.links.extend(attrs[k] for k in ('href','src') if k in attrs)

pages={}
for file in ROOT.rglob('*.html'):
    if any(p in {'source','.git','node_modules','.wrangler','audits','audit'} for p in file.relative_to(ROOT).parts):continue
    doc=Page();doc.feed(file.read_text(encoding='utf-8'));pages[file.resolve()]=doc
errors=[]
for file,doc in pages.items():
    base='https://allkonjac.com/'+file.relative_to(ROOT).as_posix()
    for link in doc.links:
        u=urlsplit(urljoin(base,link))
        if u.netloc!='allkonjac.com' or u.scheme not in ('http','https'):continue
        route=u.path or '/'
        target=ROOT/unquote(route.lstrip('/'))
        if route.endswith('/'):target=target/'index.html'
        if not target.is_file():errors.append([str(file.relative_to(ROOT)),link,'missing file'])
        elif u.fragment and target.resolve() in pages and u.fragment not in pages[target.resolve()].ids:
            errors.append([str(file.relative_to(ROOT)),link,'missing fragment'])
data=json.loads((ROOT/'source/comparison/translation-input.json').read_text(encoding='utf-8'))
for lang in ('th','id'):
    values=json.loads((ROOT/f'source/comparison/{lang}.json').read_text(encoding='utf-8'))
    for u in data['units']:
        def numbers(s):
            for word,value in [('seven','7'),('tujuh','7'),('three','3'),('tiga','3')]:
                s=re.sub(r'\b'+word+r'\b',value,s,flags=re.I)
            return re.findall(r'\d+',s.replace('20,000','20000').replace('20.000','20000'))
        if numbers(u['text'])!=numbers(values[u['id']]):errors.append([lang,u['id'],'numeric mismatch'])
check(ROOT)
report={'public_html_pages':len(pages),'errors':errors,'passed':not errors}
folder=ROOT/'audits/comparison-2026-10-20';folder.mkdir(parents=True,exist_ok=True)
(folder/'links.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
raise SystemExit(1 if errors else 0)
