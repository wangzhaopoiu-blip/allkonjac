"""Reviewed equipment reference configurations and labels in three languages."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]

def escape(value):
    return html.escape(str(value), quote=True)

def reference_labels(lang='en'):
    catalogs = json.loads((ROOT / 'source/translations/equipment-reference.json').read_text(encoding='utf-8'))
    if lang not in {'en', 'th', 'id'} or set(catalogs) != {'en', 'th', 'id'}:
        raise ValueError('Equipment reference labels require en, th and id')
    expected = {'equipment_name', 'dimensions', 'listed_power', 'remarks', 'eyebrow', 'heading',
                'description', 'voltage_note', 'configuration_note', 'discuss', 'back_gallery',
                'overview_tank_title', 'overview_tank_alt', 'overview_tank_note',
                'overview_workshop_title', 'overview_workshop_alt', 'overview_workshop_note'}
    for locale, labels in catalogs.items():
        if set(labels) != expected or any(not isinstance(value, str) or not value.strip() for value in labels.values()):
            raise ValueError(f'Incomplete equipment reference labels: {locale}')
    return {key: escape(value) for key, value in catalogs[lang].items()}

def reference_data(lang='en'):
    if lang not in {'en', 'th', 'id'}:
        raise ValueError('Unsupported equipment reference language')
    specs = json.loads((ROOT / f'source/data/equipment-reference-{lang}.json').read_text(encoding='utf-8'))
    fields = {'equipment_name', 'dimensions_mm', 'remarks', 'power_kw'}
    if not isinstance(specs, list) or len(specs) != 9 or any(not isinstance(item, dict) or set(item) != fields for item in specs):
        raise ValueError('Equipment reference data must contain nine four-field configurations')
    for item in specs:
        if any(not isinstance(item[key], str) or not item[key].strip() for key in ('equipment_name', 'power_kw')):
            raise ValueError('Empty equipment name or power')
        if any(not isinstance(item[key], list) or not item[key] or any(not isinstance(value, str) or not value.strip() for value in item[key]) for key in ('dimensions_mm', 'remarks')):
            raise ValueError('Invalid equipment dimensions or remarks')
    if lang != 'en':
        english = reference_data('en')
        for index, (original, translated) in enumerate(zip(english, specs), 1):
            if translated['power_kw'] != original['power_kw']:
                raise ValueError(f'{lang}: changed power for equipment {index}')
            for field in ('dimensions_mm', 'remarks'):
                if len(translated[field]) != len(original[field]):
                    raise ValueError(f'{lang}: missing {field} for equipment {index}')
                for source, target in zip(original[field], translated[field]):
                    if re.findall(r'\d+(?:\.\d+)?', source) != re.findall(r'\d+(?:\.\d+)?', target):
                        raise ValueError(f'{lang}: changed numeric facts for equipment {index}')
                    for token in ('PSS-3', 'K', 'CB7', 'NSK', 'pH', 'MPa', 'kW', 'mm', 'L'):
                        if re.search(r'(?<![A-Za-z0-9])' + re.escape(token) + r'(?![A-Za-z0-9])', source) and token not in target:
                            raise ValueError(f'{lang}: changed technical token {token} for equipment {index}')
    return specs

def reference_specifications(lang='en'):
    return specification_cards(reference_data(lang), lang)

def overview_images(lang='en'):
    labels = reference_labels(lang)
    return f'''<div class="equipment-intro-media" id="equipment-overview">
<figure class="equipment-intro-figure"><div class="equipment-intro-frame motion-image"><img src="/assets/equipment/equipment-three-tank-studio-v1-960.webp" srcset="/assets/equipment/equipment-three-tank-studio-v1-480.webp 480w, /assets/equipment/equipment-three-tank-studio-v1-960.webp 960w, /assets/equipment/equipment-three-tank-studio-v1-1448.webp 1448w" sizes="(max-width:900px) 92vw, (max-width:1283px) 45vw, 565px" alt="{labels['overview_tank_alt']}" width="1448" height="1086" loading="lazy" decoding="async"></div><figcaption><h3>{labels['overview_tank_title']}</h3><p>{labels['overview_tank_note']}</p></figcaption></figure>
<figure class="equipment-intro-figure"><div class="equipment-intro-frame motion-image"><img src="/assets/food-equipment.jpg" alt="{labels['overview_workshop_alt']}" width="1702" height="1276" loading="lazy" decoding="async"></div><figcaption><h3>{labels['overview_workshop_title']}</h3><p>{labels['overview_workshop_note']}</p></figcaption></figure>
</div>'''

def specification_cards(specs, lang='en'):
    labels = reference_labels(lang)
    contact_url = 'https://allkonjac.com' + ('' if lang == 'en' else '/' + lang) + '/#contact'
    cards = []
    for index, item in enumerate(specs, 1):
        dimensions = ''.join('<span class="spec-dimension">' + escape(s) + '</span>' for s in item['dimensions_mm'])
        notes = '<ul class="spec-remarks">' + ''.join('<li>' + escape(s) + '</li>' for s in item['remarks']) + '</ul>'
        cards.append(f'''<article class="spec-card" data-spec-index="{index}" aria-labelledby="spec-equipment-{index}">
<div class="spec-card-heading"><span class="spec-card-label">{labels['equipment_name']}</span><h3 id="spec-equipment-{index}" data-spec-field="equipment_name">{escape(item['equipment_name'])}</h3></div>
<dl><div data-spec-field="dimensions_mm"><dt>{labels['dimensions']}</dt><dd>{dimensions}</dd></div><div data-spec-field="power_kw"><dt>{labels['listed_power']}</dt><dd><span class="spec-power">{escape(item['power_kw'])}<small>kW</small></span></dd></div><div class="spec-card-remarks" data-spec-field="remarks"><dt>{labels['remarks']}</dt><dd>{notes}</dd></div></dl></article>''')
    return f'''<section class="equipment-specifications" id="equipment-specifications"><div class="wrap"><div class="section-top"><div><div class="eyebrow">{labels['eyebrow']}</div><h2>{labels['heading']}</h2></div><p>{labels['description']}</p></div><div class="spec-card-voltage">{labels['voltage_note']} · 380 V</div><div class="spec-cards-grid">''' + ''.join(cards) + f'''</div><p class="spec-note" id="spec-configuration-note">{labels['configuration_note']}</p><div class="actions spec-actions"><a class="btn primary" href="{contact_url}">{labels['discuss']}</a><a class="btn secondary" href="#equipment-gallery">{labels['back_gallery']}</a></div></div></section>'''
