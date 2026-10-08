"""English equipment reference configurations approved for public presentation."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]

def escape(value):
    return html.escape(str(value), quote=True)

def reference_specifications():
    specs = json.loads((ROOT / 'source/data/equipment-reference-en.json').read_text(encoding='utf-8'))
    fields = {'equipment_name', 'dimensions_mm', 'remarks', 'power_kw'}
    if len(specs) != 9 or any(set(item) != fields for item in specs):
        raise ValueError('Equipment reference data must contain nine four-field configurations')
    return specification_cards(specs)

def overview_images():
    return '''<div class="equipment-intro-media" id="equipment-overview">
<figure class="equipment-intro-figure"><div class="equipment-intro-frame motion-image"><img src="/assets/equipment/equipment-three-tank-studio-v1-960.webp" srcset="/assets/equipment/equipment-three-tank-studio-v1-480.webp 480w, /assets/equipment/equipment-three-tank-studio-v1-960.webp 960w, /assets/equipment/equipment-three-tank-studio-v1-1448.webp 1448w" sizes="(max-width:900px) 92vw, (max-width:1283px) 45vw, 565px" alt="Three stainless-steel mixing tanks on a raised platform with railings and stairs" width="1448" height="1086" loading="lazy" decoding="async"></div><figcaption><h3>Three-Tank Mixing Platform</h3><p>AI-enhanced equipment presentation based on a supplied reference photo.</p></figcaption></figure>
<figure class="equipment-intro-figure"><div class="equipment-intro-frame motion-image"><img src="/assets/food-equipment.jpg" alt="Conveyor and tank equipment in a workshop" width="1702" height="1276" loading="lazy" decoding="async"></div><figcaption><h3>Conveyor and Tank Equipment</h3><p>Workshop view of equipment and production-line connections.</p></figcaption></figure>
</div>'''

def specification_cards(specs):
    cards = []
    for index, item in enumerate(specs, 1):
        dimensions = ''.join('<span class="spec-dimension">' + escape(s) + '</span>' for s in item['dimensions_mm'])
        notes = '<ul class="spec-remarks">' + ''.join('<li>' + escape(s) + '</li>' for s in item['remarks']) + '</ul>'
        cards.append(f'''<article class="spec-card" data-spec-index="{index}" aria-labelledby="spec-equipment-{index}">
<div class="spec-card-heading"><span class="spec-card-label">Equipment name</span><h3 id="spec-equipment-{index}" data-spec-field="equipment_name">{escape(item['equipment_name'])}</h3></div>
<dl><div data-spec-field="dimensions_mm"><dt>Dimensions (mm)</dt><dd>{dimensions}</dd></div><div data-spec-field="power_kw"><dt>Listed power</dt><dd><span class="spec-power">{escape(item['power_kw'])}<small>kW</small></span></dd></div><div class="spec-card-remarks" data-spec-field="remarks"><dt>Remarks</dt><dd>{notes}</dd></div></dl></article>''')
    return '''<section class="equipment-specifications" id="equipment-specifications"><div class="wrap"><div class="section-top"><div><div class="eyebrow">REFERENCE CONFIGURATIONS</div><h2>Equipment Reference Specifications</h2></div><p>Explore individual equipment configurations, dimensions and features for your production project.</p></div><div class="spec-card-voltage">Reference configurations · 380 V</div><div class="spec-cards-grid">''' + ''.join(cards) + '''</div><p class="spec-note" id="spec-configuration-note">Dimensions can be customized and are shown in the order supplied. Power is shown as listed for each configuration. Final dimensions, materials and equipment specifications are confirmed for your project. Gallery images illustrate equipment categories; exact configurations are confirmed separately.</p><div class="actions spec-actions"><a class="btn primary" href="https://allkonjac.com/#contact">Discuss Your Configuration</a><a class="btn secondary" href="#equipment-gallery">Back to Equipment Gallery ↑</a></div></div></section>'''
