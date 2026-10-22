"""Stage only canonical pages, 404, discovery files and approved public assets."""
from pathlib import Path
import hashlib,json,shutil,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.wrangler/public'
urls=[n.text for n in ET.parse(ROOT/'sitemap.xml').getroot().iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert len(urls)==39
files=[u.removeprefix('https://allkonjac.com/').rstrip('/')+'/index.html' if u!='https://allkonjac.com/' else 'index.html' for u in urls]
files += ['404.html','robots.txt','sitemap.xml','llms.txt','favicon.ico']
files += [p.relative_to(ROOT).as_posix() for p in (ROOT/'assets').rglob('*') if p.is_file()]
assert not any('market-snacks' in p for p in files), 'Unapproved snack preview must not be packaged'
expected=set(files)
existing={p.relative_to(OUT).as_posix() for p in OUT.rglob('*') if p.is_file()}
assert not existing-expected, 'Unexpected stale package files: '+str(existing-expected)
manifest=[]
for rel in sorted(expected):
 src=ROOT/rel;dst=OUT/rel
 assert src.is_file(),rel
 dst.parent.mkdir(parents=True,exist_ok=True)
 shutil.copyfile(src,dst)
 manifest.append({'path':'/'+rel,'sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
(ROOT/'audits/buyer-public-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(f'Packaged {len(manifest)} public files; source, audits and customer originals excluded.')
