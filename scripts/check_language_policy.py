"""Reject Han text and Chinese font declarations in published text assets.

Original raster images and fonts are deliberately preserved. Internal sources are
excluded by the same publishing boundary as .assetsignore.
"""
from pathlib import Path
import html
import re

HAN=re.compile('[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\U00020000-\U0002ebef]')
FONTS=re.compile(r'Noto\s*Sans\s*(?:SC|CJK)|Microsoft\s*YaHei|PingFang\s*SC|SimSun|SimHei|WenQuanYi|Source\s*Han',re.I)
EXCLUDED={'.git','.github','.wrangler','node_modules','source','content','scripts','audits','audit','work','original-assets','__pycache__','.openai'}

def inspect(text):
    decoded=html.unescape(text)
    decoded=re.sub(r'\\u([0-9a-fA-F]{4})',lambda m:chr(int(m[1],16)),decoded)
    decoded=re.sub(r'\\([0-9a-fA-F]{2,6})\s?',lambda m:chr(int(m[1],16)) if int(m[1],16)<=0x10ffff else '',decoded)
    return bool(HAN.search(decoded) or FONTS.search(decoded))

def check(root, output=None):
    failures=[];count=0
    for p in root.rglob('*'):
        relative=p.relative_to(root)
        if any(part in EXCLUDED for part in relative.parts) or p.name in {'README.md','AGENTS.md'}:continue
        if p.is_file() and p.suffix in {'.html','.css','.js','.svg','.json','.xml','.txt'}:
            count+=1
            text=(output or {}).get(relative.as_posix(),p.read_text(encoding='utf-8-sig'))
            if inspect(text):failures.append(relative.as_posix())
    for relative,text in (output or {}).items():
        if inspect(text) and relative not in failures:failures.append(relative)
    if failures:raise ValueError('Language policy violation: '+', '.join(failures))
    print(f'Language policy passed: {count} public text assets plus generated output; original raster images preserved.')

if __name__=='__main__':check(Path(__file__).resolve().parents[1])
