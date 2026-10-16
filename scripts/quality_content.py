"""English-only quality references and drying material content."""
from pathlib import Path
import html
import json
import re
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DETAIL_PATH = 'ingredients/coa-reference'
DETAIL_URL = 'https://allkonjac.com/' + DETAIL_PATH + '/'
STYLE = '<link rel="stylesheet" href="/assets/quality-content.css">'

def esc(value):
    return html.escape(str(value), quote=True)

def data():
    return json.loads((ROOT / 'source/data/coa-reference-en.json').read_text(encoding='utf-8'))

def enquiry(kind):
    if kind == 'coa':
        message = 'Hello ALL KONJAC, I would like to request a batch-specific COA. Product / grade: [please specify]. Lot or order number: [please specify].'
        label, subject = 'Request a Batch-specific COA', 'Batch-specific COA enquiry'
    else:
        message = 'Hello ALL KONJAC, I would like to discuss a drying line for whole konjac chips. Raw material: [bulbil / white konjac]. Target input or output: [quantity]. Available energy source: [please specify].'
        label, subject = 'Discuss Your Drying-line Requirements', 'Konjac drying-line enquiry'
    return (f'<div class="actions quality-actions"><a class="btn primary" href="https://wa.me/8615637136906?text={quote(message, safe="")}" target="_blank" rel="noopener">{label}</a>'
            f'<a class="btn secondary" href="mailto:583411495@qq.com?subject={quote(subject, safe="")}&amp;body={quote(message, safe="")}">Email Your Enquiry</a></div>')

def summary():
    cards = []
    for sample in data()['samples']:
        year = sample['year']
        result = {row['item']: row['result'] for row in sample['rows']}
        viscosity = result['Viscosity (No. 4 rotor, 12 r/min, 30°C)']
        values = [('Viscosity', f'{int(viscosity):,}', 'mPa·s'),
                  ('Glucomannan · dry basis', result['Glucomannan (dry basis)'], '%'),
                  ('Water content', result['Water content'], '%')]
        stats = ''.join(f'<div><dt>{name}</dt><dd>{value}<span>{unit}</span></dd>'
                        + ('<small class="supplier-mark">Supplier-provided update*</small>' if year == 2026 and name.startswith('Glucomannan') else '') + '</div>'
                        for name, value, unit in values)
        tag = 'HISTORICAL SAMPLE · 2024' if year == 2024 else '2026 SAMPLE REFERENCE + SUPPLIER UPDATE'
        cards.append(f'<article class="quality-card"><p class="quality-kicker">{tag}</p><h3>{esc(sample["title"])}</h3><p class="quality-reference">Report reference: {sample["report_number"]}</p><dl class="quality-stats">{stats}</dl><p class="test-condition">Viscosity: No. 4 rotor · 12 r/min · 30°C.</p><a class="text-link" href="/{DETAIL_PATH}/#{sample["id"]}">View the data and source notes →</a></article>')
    return ('<section class="quality-section" id="quality-documents"><div class="wrap"><div class="section-top"><div><div class="eyebrow">PRODUCT QUALITY DOCUMENTS</div><h2>Test data for a better-informed enquiry.</h2></div><p>Explore sample-specific test records and request the documents that match your product, grade and lot.</p></div>'
            '<div class="quality-grid">' + ''.join(cards) + '</div>'
            '<p class="quality-footnote">*93% is a supplier-provided updated value; a revised test report has not been reviewed. Other displayed values are historical sample results. These figures are not a uniform specification or a guarantee for every lot.</p>'
            '<p class="quality-footnote">Refined konjac flour: corresponding test records are pending. Purified konjac powder / konjac gum data are listed separately.</p>' + enquiry('coa') + '</div></section>')

def materials():
    items = [
        ('bulbil-machine-dried-chips-v4.webp', 'Machine-dried bulbil konjac chips', 'Irregular whole slices with natural folds, a pale cream-to-yellow appearance and occasional peel edges.'),
        ('white-machine-dried-chips-v4.webp', 'Machine-dried white konjac chips', 'Broad, whole slices with a light ivory appearance, fine surface texture and naturally curled edges.')]
    cards = []
    for index, (image, title, desc) in enumerate(items, 1):
        alt = title + ' — reference-based material visualization.'
        cards.append(f'<figure class="material-card"><a class="equipment-image-link" href="/assets/materials/{image}" data-equipment-image data-title="{esc(title)}" aria-label="{esc(title)}. View larger"><img src="/assets/materials/{image}" alt="{esc(alt)}" width="1448" height="1086" loading="lazy" decoding="async"><span class="material-zoom">View larger ↗</span></a><figcaption><span class="quality-kicker">WHOLE DRIED CHIPS · 0{index}</span><h3>{title}</h3><p>{desc}</p></figcaption></figure>')
    return ('<section class="materials-section" id="machine-dried-chips"><div class="wrap"><div class="section-top"><div><div class="eyebrow">MATERIALS & DRYING</div><h2>Plan the line around the chip.</h2></div><p>Raw material and slicing method influence the appearance of whole dried chips. Discuss preparation, conveying and drying as one connected process.</p></div><div class="quality-grid">' + ''.join(cards) + '</div>'
            '<p class="quality-footnote">Reference-based material visuals illustrate typical forms. Actual colour, slice dimensions and drying targets are confirmed for the incoming material and project.</p>' + enquiry('drying') + '</div></section>'
            '<dialog class="equipment-lightbox" aria-labelledby="equipment-lightbox-title"><form method="dialog"><button class="equipment-lightbox-close" type="submit">Close image ×</button></form><h3 id="equipment-lightbox-title">Material image viewer</h3><div class="equipment-lightbox-picture"></div><p>Reference-based material visualization. Actual material characteristics are confirmed for each project.</p></dialog>')

def detail_page(shell):
    header = re.search(r'<header>.*?</header>', shell, re.S).group(0)
    header = re.sub(r'<details class="language-switcher">.*?</details>', '<span class="language-switcher language-summary" aria-label="Page language: English">EN</span>', header, flags=re.S)
    footer = re.search(r'<footer>.*?</footer>', shell, re.S).group(0)
    articles = []
    for sample in data()['samples']:
        year = sample['year']
        metadata = ''.join(f'<div><dt>{esc(x["label"])}</dt><dd>{esc(x["value"])}</dd></div>' for x in sample['metadata'])
        update = sample.get('supplier_update')
        notice = ('<div class="supplier-notice"><strong>Supplier-provided update · 16 October 2026</strong><p>' + esc(update['note']) + '</p></div>') if update else ''
        rows = []
        for row in sample['rows']:
            label = row['item'] + (' — supplier-provided update*' if row.get('source') == 'supplier_update' else '')
            fields = ''.join(f'<td data-label="{title}">{esc(row[key])}</td>' for key, title in [('method','Test method'),('unit','Unit'),('criterion','Report criterion'),('result','Result / update'),('conclusion','Source / conclusion')])
            rows.append(f'<tr class="{"supplier-row" if row.get("source") == "supplier_update" else "report-row"}"><th scope="row">{esc(label)}</th>{fields}</tr>')
        note = '<p class="quality-footnote">The 93% entry is a separately identified supplier update, with no test method, report criterion or conformity decision assigned to it. The other eleven entries retain the historical report data.</p>' if update else ''
        if year == 2026:
            note += '<p class="quality-footnote">For lead and total arsenic, 0.04 mg/kg is the quantitation limit, not a measured concentration. The report provides no item conformity decision for these tests.</p>'
        articles.append(f'<article class="sample-report" id="{sample["id"]}"><div class="report-top"><div><div class="eyebrow">{year} SAMPLE REFERENCE</div><h2>{esc(sample["title"])}</h2><p>Report reference: {sample["report_number"]}</p></div><span class="test-count">{len(sample["rows"])} entries</span></div><dl class="report-metadata">{metadata}</dl><p class="quality-footnote">{esc(sample["basis"])}</p>{notice}<div class="test-table-wrap"><table class="test-table"><caption>{year} sample data' + (' and separately marked supplier update' if update else '') + '</caption><thead><tr><th scope="col">Test item</th><th scope="col">Test method</th><th scope="col">Unit</th><th scope="col">Report criterion</th><th scope="col">Result / update</th><th scope="col">Source / conclusion</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>' + note + '</article>')
    schema = {'@context':'https://schema.org','@type':'WebPage','name':'Sample Test Results & COA Reference','url':DETAIL_URL,'inLanguage':'en','isPartOf':{'@id':'https://allkonjac.com/#website'}}
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sample Test Results & COA Reference | ALL KONJAC</title><meta name="description" content="Explore historical konjac sample test data and a separately marked supplier update. Request a batch-specific COA for your product, grade and lot."><meta name="robots" content="index,follow"><link rel="canonical" href="' + DETAIL_URL + '"><meta property="og:type" content="website"><meta property="og:title" content="Sample Test Results & COA Reference | ALL KONJAC"><meta property="og:url" content="' + DETAIL_URL + '"><link rel="icon" type="image/svg+xml" href="/assets/brand/all-konjac-favicon.svg"><link rel="stylesheet" href="/assets/site.css">' + STYLE + '<script src="/assets/site.js" defer></script><script type="application/ld+json">' + json.dumps(schema).replace('<','\\u003c') + '</script></head><body class="motion-enabled"><a class="skip-link" href="#main-content">Skip to content</a>' + header +
            '<main id="main-content"><section class="page-hero"><div class="wrap"><nav class="breadcrumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li><a href="/ingredients/">Ingredients</a></li><li aria-current="page">COA reference</li></ol></nav><div class="eyebrow">PRODUCT QUALITY DOCUMENTS</div><h1>Sample test results & COA reference.</h1><p>Historical sample records are presented separately from supplier-provided updates. Use them to discuss the grade and documents needed for your application.</p><div class="document-notice">This reference page is not a manufacturer-issued batch COA. Source identities are retained in internal records; traceability details are available with corresponding documents on request.</div></div></section><section class="quality-detail"><div class="wrap"><nav class="quality-index" aria-label="On this page"><a href="#sample-2024">2024 sample</a><a href="#sample-2026">2026 sample + update</a><a href="#request-coa">Request a COA</a></nav><div class="pending-reference"><strong>Refined konjac flour · records pending</strong><p>The available report data relate to purified konjac powder / konjac gum. Corresponding test records for refined konjac flour have not yet been provided.</p></div>' + ''.join(articles) + '<div class="quality-request" id="request-coa"><div class="eyebrow">MATCH THE DOCUMENT TO THE LOT</div><h2>Request a batch-specific COA.</h2><p>Provide the product name, grade or model, and lot or order number. A formal batch COA should be issued by the actual manufacturer using the corresponding production records. A sample or report number is not automatically a production lot number.</p>' + enquiry('coa') + '<p><a class="text-link" href="/ingredients/#quality-documents">← Back to ingredients</a></p></div></div></section></main>' + footer + '</body></html>\n')

def validate_detail(output):
    if output.count('class="report-row"') != 17 or output.count('class="supplier-row"') != 1:
        raise ValueError('COA reference must retain 17 report rows and one separately sourced update')
    for forbidden in ['88.9', '惠葡', '天然星', 'Huipu', 'Tianranxing']:
        if forbidden.lower() in output.lower():
            raise ValueError('Unapproved public source identity or historical value: ' + forbidden)
    if DETAIL_URL not in output or 'Supplier-provided update' not in output:
        raise ValueError('Missing canonical or update provenance')
