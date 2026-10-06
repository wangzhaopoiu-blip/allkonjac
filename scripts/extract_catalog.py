"""One-time extraction from the five approved English pages.

The resulting source/templates files are the editable generator inputs. Do not
rerun this bootstrap over generated output; it deliberately refuses to replace
an existing catalog. Stable IDs are content hashes, with explicit auxiliary IDs.
"""
from pathlib import Path
import hashlib
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = ["", "ingredients", "equipment", "drying-lines", "technology"]
catalog = {}
contexts = {}
values = {}
STATIC = {"ALL", "KONJAC", "ALL KONJAC", "EN", "WhatsApp", "WeChat",
          "+86 156 3713 6906", "583411495@qq.com", "© 2026 ALL KONJAC."}
TRANSLATE_JSON = {"name", "description", "serviceType", "contactType"}


def add(value, context, key=None):
    value = html.unescape(value).strip()
    if key is None:
        key = values.get(value) or "text_" + hashlib.sha256(value.encode()).hexdigest()[:12]
    if key in catalog and catalog[key] != value:
        raise ValueError("Translation ID collision: " + key)
    catalog[key] = value
    values[value] = key
    contexts.setdefault(key, []).append(context)
    return key


def translate_json(value, context, field=None):
    if isinstance(value, list):
        return [translate_json(item, f"{context}[{i}]") for i, item in enumerate(value)]
    if isinstance(value, dict):
        return {k: translate_json(v, f"{context}.{k}", k) for k, v in value.items()}
    if isinstance(value, str) and field in TRANSLATE_JSON and value not in STATIC:
        return {"$t": add(value, context)}
    return value


def template(page):
    path = ROOT / page / "index.html"
    name = page or "home"
    source = path.read_text(encoding="utf-8")
    original = ROOT / "source" / "original" / (name + ".html")
    original.parent.mkdir(parents=True, exist_ok=True)
    original.write_text(source, encoding="utf-8")
    schema_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)
    schema = translate_json(json.loads(schema_match.group(1)), name + ":JSON-LD")
    (ROOT / "source" / "schema" / (name + ".json")).write_text(
        json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    source = source[:schema_match.start()] + "{{jsonld}}" + source[schema_match.end():]
    source = re.sub(r'<span class="lang".*?</span>', "{{language_switcher}}", source)
    source = source.replace('<html lang="en"', '<html lang="{{lang}}"')
    source = re.sub(r'<link rel="canonical" href="[^"]+">', '{{seo_links}}', source)
    source = source.replace('property="og:locale" content="en_US"',
                            'property="og:locale" content="{{og_locale}}"')
    source = re.sub(r'(property="og:url" content=")[^"]+', r'\1{{canonical}}', source)
    source = source.replace('<div class="hero-photo"></div>',
                            '<div class="hero-photo"><span class="hero-photo-caption">{{t:ui.hero_caption}}</span></div>')
    source = source.replace('aria-controls="primary-navigation"',
                            'aria-controls="primary-navigation" aria-label="{{a:ui.menu_open}}" data-label-open="{{a:ui.menu_open}}" data-label-close="{{a:ui.menu_close}}"')
    # Each non-brand text node already contains a complete paragraph, question,
    # heading or short label. There are no sentences split by inline markup.
    pieces = re.split(r'(<[^>]*>|\{\{[^}]*\}\})', source)
    for i, piece in enumerate(pieces):
        if piece.startswith("<"):
            def attr(match):
                attr_name, raw = match.group(1), match.group(2)
                # Only descriptive metadata, alt and accessible labels translate.
                if "{{" in raw or html.unescape(raw).strip() in STATIC:
                    return match.group(0)
                if attr_name == "content" and not re.search(
                    r'(?:name="(?:description|twitter:(?:title|description))"|property="og:(?:title|description|image:alt)")', piece):
                    return match.group(0)
                return attr_name + '="{{a:' + add(raw, name + ":attribute:" + attr_name) + '}}"'
            pieces[i] = re.sub(r'\b(content|alt|aria-label)="([^"]*)"', attr, piece)
        elif piece.startswith("{{") or not piece.strip():
            continue
        else:
            decoded = html.unescape(piece).strip()
            if decoded in STATIC or re.fullmatch(r'\d+', decoded) or decoded.lower() == "<!doctype html>":
                continue
            leading = piece[:len(piece) - len(piece.lstrip())]
            trailing = piece[len(piece.rstrip()):]
            pieces[i] = leading + "{{t:" + add(decoded, name + ":visible") + "}}" + trailing
    result = "".join(pieces)
    result = re.sub(r'\b(src|href)="assets/', r'\1="/assets/', result)
    (ROOT / "source" / "templates" / (name + ".html")).write_text(result, encoding="utf-8")


def main():
    if (ROOT / "content" / "en.json").exists():
        raise SystemExit("Catalog already exists; edit source templates instead of re-extracting generated output.")
    for folder in ["content", "source/schema", "source/templates"]:
        (ROOT / folder).mkdir(parents=True, exist_ok=True)
    auxiliary = {
        "ui.hero_caption": "REAL EQUIPMENT • REAL PRODUCTION ENVIRONMENT",
        "ui.menu_open": "Open menu",
        "ui.menu_close": "Close menu",
        "ui.language_choose": "Choose page language",
        "error.title": "Page Not Found | ALL KONJAC",
        "error.heading": "Page not found",
        "error.description": "The requested page could not be found.",
        "error.return": "Return to ALL KONJAC",
    }
    for key, value in auxiliary.items():
        add(value, "auxiliary:" + key, key)
    for page in PAGES:
        template(page)
    (ROOT / "content" / "en.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "source" / "translation-context.json").write_text(json.dumps(contexts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(catalog)} unique translation strings: {ROOT / 'content' / 'en.json'}")


if __name__ == "__main__":
    main()
