"""Shared, localized buyer tools. Public samples never contain the source identity."""
from pathlib import Path
from html import escape as e
import json

ROOT = Path(__file__).resolve().parents[1]
LANGS = ('en', 'th', 'id')

def data():
    return json.loads((ROOT / 'source/data/buyer-resources.json').read_text(encoding='utf-8'))

def quotation(lang, full=False):
    d = json.loads((ROOT / 'source/data/quotation-sample.json').read_text(encoding='utf-8'))[lang]
    rows = ''.join('<tr><th scope="row">'+e(name)+'</th><td>'+e(d['packing'])+'</td><td>40</td><td>'+price+'</td><td>'+amount+'</td></tr>'
                   for name, price, amount in zip(d['products'], ['2,000.00','3,000.00'], ['80,000.00','120,000.00']))
    totals = ''.join('<tr><th scope="row" colspan="4">'+e(label)+'</th><td>'+value+'</td></tr>'
                     for label, value in zip(d['totals'], ['200,000.00','-6,000.00','0.00','194,000.00']))
    result = '<section class="quotation-sample" id="quotation-example"><div class="wrap"><h2>'+e(d['title'])+'</h2><p class="sample-notice">'+e(d['notice'])+'</p><p>'+e(d['intro'])+'</p>'
    result += '<p><strong>SAMPLE-QT-2026-001 · CNY</strong></p><p>'+e(d['seller'])+'<br>'+e(d['buyer'])+'</p>'
    if not full:
        hint = {'en':'On a small screen, scroll the table sideways to see all prices.', 'th':'บนหน้าจอขนาดเล็ก เลื่อนตารางในแนวนอนเพื่อดูราคาทั้งหมด', 'id':'Pada layar kecil, geser tabel ke samping untuk melihat semua harga.'}[lang]
        result += '<p class="quote-footnote">'+e(hint)+'</p>'
    result += '<div class="quote-table-scroll" tabindex="0" role="region" aria-label="'+e(d['title'])+'"><table class="quote-table"><caption>'+e(d['title'])+' · CNY</caption><thead><tr>'+''.join('<th scope="col">'+e(h)+'</th>' for h in d['headers'])+'</tr></thead><tbody>'+rows+'</tbody><tfoot>'+totals+'</tfoot></table></div><p>'+e(d['freight'])+'</p><h3>'+e(d['conditionsTitle'])+'</h3><ul>'+''.join('<li>'+e(t)+'</li>' for t in d['conditions'])+'</ul>'
    if full:
        result += '<section class="quote-terms"><h3>'+e(d['termsTitle'])+'</h3><ol>'+''.join('<li>'+e(t)+'</li>' for t in d['terms'])+'</ol></section>'
    else:
        result += '<a class="btn primary quote-download" href="/assets/documents/quotation-example-'+lang+'.pdf" download>'+e(d['download'])+'</a>'
    return result+'<p class="quote-footnote">'+e(d['footer'])+'</p></div></section>'

def inquiry_tools(page, lang, message):
    d = data()[lang]
    prefix = '' if lang == 'en' else '/'+lang
    links = {'ingredients': [('ingredients/coa-reference/', d['coa']), ('ingredients/#quotation-example', d['quote'])],
             'equipment': [('equipment/#equipment-specifications', d['specs'])],
             'drying-lines': [('blog/plan-konjac-dried-chip-drying-line/', d['guide'])],
             'technology': [('blog/konjac-glucomannan-food-applications-research-guide/', d['research'])]}
    refs = ''.join('<a href="'+prefix+'/'+url+'">'+e(label)+'</a> ' for url,label in links[page])
    return '<div class="buyer-tools"><h3>'+e(d['availableTitle'])+'</h3><p>'+e(d['available'][page])+'</p><div class="related-links">'+refs+'</div><h3>'+e(d['templateTitle'])+'</h3><p>'+e(d['help'])+'</p><pre id="enquiry-template" class="enquiry-template">'+e(message)+'</pre><button hidden class="btn secondary copy-enquiry" type="button" data-copy-enquiry data-success="'+e(d['copied'])+'" data-failure="'+e(d['failed'])+'">'+e(d['copy'])+'</button><span class="copy-status" role="status" aria-live="polite"></span></div>'

SLUGS = ['choose-konjac-powder-gum', 'konjac-refined-powder-vs-konjac-gum', 'konjac-glucomannan-ingredient-selection-hydration-viscosity', 'konjac-glucomannan-food-applications-research-guide', 'konjac-equipment-project-brief', 'plan-konjac-dried-chip-drying-line']

def add_article_routes(output):
    for lang in LANGS:
        d = data()[lang]
        prefix = '' if lang == 'en' else '/'+lang
        for i,slug in enumerate(SLUGS):
            file = (prefix+'/blog/'+slug+'/index.html').lstrip('/')
            text = output[file]
            links = [(prefix+'/blog/'+SLUGS[j]+'/', d['articleLabels'][j]) for j in ([1,2] if i==0 else [0,3] if i in (1,2) else [2,0] if i==3 else [5 if i==4 else 4])]
            if i in (0,1,2):
                links.append((prefix+'/ingredients/#quotation-example',d['quote']))
            block = '<section class="buyer-reading-route" style="max-width:1100px;margin:32px auto;padding:24px"><h2>'+e(d['readingTitle'])+'</h2><p>'+e(d['purposes'][i])+'</p><ul>'+''.join('<li><a href="'+url+'">'+e(label)+'</a></li>' for url,label in links)+'</ul><p>'+e(d['updated'])+' <time datetime="2026-10-21">2026-10-21</time></p></section>'
            text = text.replace('</main>', block+'</main>', 1)
            import re
            text = re.sub(r'("dateModified"\s*:\s*")[^"]+("|$)', r'\g<1>2026-10-21\2', text)
            output[file] = text
