"""Verify the deployed page inventory, byte content, assets and redirect boundaries."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://allkonjac.com'
OUT = ROOT / 'audits/production-unified-2026-10-21.json'


def fetch(url):
    with TemporaryDirectory() as tmp:
        body, headers = Path(tmp) / 'body', Path(tmp) / 'headers'
        result = subprocess.run(['curl.exe', '-sS', '--retry', '1', '--max-time', '35',
                                 '-o', str(body), '-D', str(headers), '-w', '%{http_code}', url],
                                capture_output=True, encoding='utf-8', check=True)
        return int(result.stdout), body.read_bytes(), headers.read_text(encoding='utf-8')


def normalize(value):
    text = value.decode('utf-8-sig').replace('\r\n', '\n')
    # Cloudflare can inject its own analytics loader after deployment.
    return re.sub(r'<script\b[^>]*(?:data-cf-beacon|static.cloudflareinsights.com)[\s\S]*?</script>', '', text).strip()


def check_file(relative):
    url = BASE + '/' + relative
    if relative.endswith('index.html'):
        url = url.removesuffix('index.html')
    status, body, headers = fetch(url)
    initial_status = status
    if relative == 'assets/equipment3d/viewer.html' and status in (301, 302, 307, 308):
        destination = re.search(r'(?im)^location:\s*(.*?)\s*$', headers)
        if destination and destination[1] == '/assets/equipment3d/viewer':
            status, body, headers = fetch(BASE + destination[1])
    local = (ROOT / relative).read_bytes()
    text_file = relative.endswith(('.html', '.xml', '.txt', '.css', '.js', '.json', '.svg'))
    matches = normalize(body) == normalize(local) if text_file else body == local
    return {'path': url.removeprefix(BASE), 'status': status, 'initial_status': initial_status, 'matches_local': matches,
            'local_sha256': hashlib.sha256(local).hexdigest(),
            'noindex_header': bool(re.search(r'(?im)^x-robots-tag:.*noindex', headers))}


if __name__ == '__main__':
    urls = [node.text for node in ET.parse(ROOT / 'sitemap.xml').getroot()
            .iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    assert len(urls) == 39
    pages = [url.removeprefix(BASE).lstrip('/') + 'index.html' for url in urls]
    files = pages + ['sitemap.xml', 'llms.txt', 'robots.txt', 'favicon.ico']
    files += [p.relative_to(ROOT).as_posix() for p in (ROOT / 'assets').rglob('*') if p.is_file()]
    with ThreadPoolExecutor(max_workers=6) as pool:
        rows = list(pool.map(check_file, files))
    errors = [row['path'] for row in rows if row['status'] != 200 or not row['matches_local'] or row['noindex_header']]
    routing = []
    for url, expected, location in [
            ('http://allkonjac.com/th/ingredients/?release=20261021&lang=th', 301,
             BASE + '/th/ingredients/?release=20261021&lang=th'),
            (BASE + '/not-a-page-release-20261021/', 404, None),
            (BASE + '/source/data/coa-reference-en.json', 404, None),
            (BASE + '/audits/unified-release-2026-10-21.md', 404, None),
            (BASE + '/scripts/build.py', 404, None)]:
        status, _, headers = fetch(url)
        match = re.search(r'(?im)^location:\s*(.*?)\s*$', headers)
        target = match[1] if match else None
        passed = status == expected and (location is None or target == location)
        routing.append({'url': url, 'status': status, 'location': target, 'passed': passed})
        if not passed:
            errors.append(url)
    report = {'date': '2026-10-21', 'canonical_pages': 39, 'verified_files': len(rows),
              'files': rows, 'routing': routing, 'errors': errors, 'passed': not errors}
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: report[key] for key in ['canonical_pages', 'verified_files', 'routing', 'errors', 'passed']}, ensure_ascii=False))
    raise SystemExit(bool(errors))
