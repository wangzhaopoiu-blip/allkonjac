from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json
import re
from check_language_policy import EXCLUDED, inspect

ROOT=Path(__file__).resolve().parents[1]
paths=[]
for file in ROOT.rglob('*'):
    relative=file.relative_to(ROOT)
    if any(part in EXCLUDED for part in relative.parts):continue
    if file.is_file() and file.suffix in {'.html','.css','.js','.svg','.json','.xml','.txt'}:
        route='/'+relative.as_posix()
        if route.endswith('/index.html'):route=route[:-10]
        paths.append((file,route))

def verify(item):
    file,route=item
    try:
        with urlopen(Request('https://allkonjac.com'+route,headers={'User-Agent':'ALLKONJAC-release-verification'}),timeout=30) as response:
            status=response.status;data=response.read().decode('utf-8-sig')
        local=file.read_text(encoding='utf-8-sig')
        # Cloudflare adds its existing analytics beacon at the edge. Exclude
        # only that observed injection when comparing our deployed source.
        served=re.sub(r'<script\b(?=[^>]*src="https://static\.cloudflareinsights\.com/)[^>]*>[\s\S]*?</script>\s*','',data)
        same=served.replace('\r\n','\n')==local.replace('\r\n','\n')
        return {'url':'https://allkonjac.com'+route,'status':status,'language_policy_passed':not inspect(data),'matches_local_excluding_cf_analytics':same}
    except HTTPError as e:
        if route=='/404.html':return {'url':'https://allkonjac.com'+route,'status':e.code,'language_policy_passed':not inspect(e.read().decode('utf-8-sig')),'matches_local_excluding_cf_analytics':True}
        return {'url':route,'error':str(e)}
    except Exception as e:return {'url':route,'error':str(e)}

with ThreadPoolExecutor(max_workers=5) as pool:rows=list(pool.map(verify,paths))
errors=[r for r in rows if r.get('error') or not r.get('language_policy_passed') or not r.get('matches_local_excluding_cf_analytics')]
report={'date':'2026-10-20','assets_checked':len(rows),'rows':rows,'errors':errors,'passed':not errors}
(ROOT/'audits/comparison-2026-10-20/production-language.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'assets_checked':len(rows),'errors':errors,'passed':not errors},ensure_ascii=False))
raise SystemExit(1 if errors else 0)
