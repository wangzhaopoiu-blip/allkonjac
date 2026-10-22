"""Create private print layouts; Chromium preserves Thai shaping with the local font."""
from pathlib import Path
from html import escape
import json
from buyer_resources import quotation
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'audits/quotation-print'
out.mkdir(parents=True,exist_ok=True)
d=json.loads((ROOT/'source/data/quotation-sample.json').read_text(encoding='utf-8'))
style='''@font-face{font-family:Thai;src:url('/assets/fonts/NotoSansThai-variable.ttf')}@page{size:A4;margin:16mm}*{box-sizing:border-box}body{font:10.5pt/1.45 Arial,sans-serif;color:#183529;margin:0}html[lang=th] body{font-family:Thai,Arial,sans-serif;font-size:10pt;line-height:1.65}h2{font-size:23pt;margin:0 0 14px}h3{font-size:13pt;margin:20px 0 8px}p{margin:8px 0}.sample-notice{background:#edf3ed;border-left:4px solid #376747;padding:10px;font-weight:700}.quote-table{width:100%;border-collapse:collapse;font-size:10pt;margin:15px 0}.quote-table caption{text-align:left;font-weight:bold;margin-bottom:8px}.quote-table th,.quote-table td{padding:8px 6px;border-bottom:1px solid #b7c9bb;text-align:left;vertical-align:top}.quote-table thead{background:#e1ebe1}.quote-table tfoot tr:last-child{font-weight:bold;background:#e1ebe1}li{margin:6px 0}ul,ol{padding-left:20px}.quote-terms{break-before:page}.quote-terms h3{margin-top:0;font-size:19pt}.quote-terms li{margin-bottom:15px;break-inside:avoid}.quote-footnote{border-top:1px solid #a8bda9;margin-top:20px;padding-top:10px;font-size:9pt}table,tr{break-inside:avoid}'''
for lang in d:
 (out/f'{lang}.html').write_text('<!doctype html><html lang="'+lang+'"><head><meta charset="utf-8"><meta name="robots" content="noindex"><title>'+escape(d[lang]['title'])+'</title><style>'+style+'</style></head><body>'+quotation(lang,True)+'</body></html>',encoding='utf-8')
print('Prepared 3 internal print layouts.')
