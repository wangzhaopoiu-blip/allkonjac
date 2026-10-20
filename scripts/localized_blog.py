"""Render the Thai and Indonesian Blog from reviewed source facts.

Translations are editorial drafts. A native industry-language review remains pending.
"""
from html import escape
import json
from pathlib import Path

BASE = "https://allkonjac.com"
RESEARCH = (
    "konjac-glucomannan-ingredient-selection-hydration-viscosity",
    "konjac-glucomannan-food-applications-research-guide",
)
GUIDES = (
    "choose-konjac-powder-gum",
    "konjac-equipment-project-brief",
    "plan-konjac-dried-chip-drying-line",
)
SLUGS = RESEARCH + GUIDES
REFERENCES = {
    RESEARCH[0]: [
        "https://doi.org/10.3390/polym15081852",
        "https://doi.org/10.1016/j.foodhyd.2021.106818",
        "https://www.sciencedirect.com/science/article/abs/pii/S0308814624040767",
        "https://pubmed.ncbi.nlm.nih.gov/34425337/",
    ],
    RESEARCH[1]: [
        "https://pubmed.ncbi.nlm.nih.gov/34425337/",
        "https://pubmed.ncbi.nlm.nih.gov/22062231/",
        "https://pubmed.ncbi.nlm.nih.gov/35954129/",
        "https://pubmed.ncbi.nlm.nih.gov/40058258/",
    ],
}
BUSINESS = ("ingredients", "equipment", "drying-lines", "technology")
FLAGS = {"en": "gb", "th": "th", "id": "id"}
NAMES = {"en": "English", "th": "ภาษาไทย", "id": "Bahasa Indonesia"}
ACCESS = {
    "en": {"home": "ALL KONJAC home", "menu": "Menu", "close": "Close menu", "language": "Choose language", "skip": "Skip to content", "primary": "Primary", "footer": "Footer", "breadcrumb": "Breadcrumb"},
    "th": {"home": "หน้าหลัก ALL KONJAC", "menu": "เมนู", "close": "ปิดเมนู", "language": "เลือกภาษา", "skip": "ข้ามไปยังเนื้อหา", "primary": "เมนูหลัก", "footer": "เมนูส่วนท้าย", "breadcrumb": "เส้นทางหน้า"},
    "id": {"home": "Beranda ALL KONJAC", "menu": "Menu", "close": "Tutup menu", "language": "Pilih bahasa", "skip": "Langsung ke konten", "primary": "Navigasi utama", "footer": "Navigasi kaki halaman", "breadcrumb": "Jejak navigasi"},
}


def blog_path(slug="", lang="en"):
    prefix = "" if lang == "en" else "/" + lang
    return prefix + "/blog/" + (slug + "/" if slug else "")


def alternates(slug=""):
    return [(lang, BASE + blog_path(slug, lang)) for lang in ("en", "th", "id")]


def alternate_links(slug=""):
    links = [f'<link rel="alternate" hreflang="{lang}" href="{url}">' for lang, url in alternates(slug)]
    links.append(f'<link rel="alternate" hreflang="x-default" href="{BASE + blog_path(slug)}">')
    return "".join(links)


def language_switcher(slug="", current="en"):
    options = []
    for lang, url in alternates(slug):
        active = ' aria-current="page"' if lang == current else ""
        options.append(f'<a href="{escape(url, quote=True)}" lang="{lang}" hreflang="{lang}"{active}>'
                       f'<img class="language-flag" src="/assets/flags/{FLAGS[lang]}.svg" alt="" '
                       f'aria-hidden="true" width="24" height="16">'
                       f'<span class="language-label">{NAMES[lang]}</span>'
                       + ('<span class="language-check" aria-hidden="true">✓</span>' if active else "") + '</a>')
    return ('<details class="language-switcher"><summary class="language-summary" aria-label="' + ACCESS[current]["language"] + '">'
            f'<img class="language-flag" src="/assets/flags/{FLAGS[current]}.svg" alt="" '
            f'aria-hidden="true" width="24" height="16"><span>{current.upper()}</span></summary>'
            '<div class="language-options">' + ''.join(options) + '</div></details>')


def load_localized(root):
    data = json.loads((root / "source/blog/localized.json").read_text(encoding="utf-8"))
    if set(data) != {"th", "id"}:
        raise ValueError("Localized Blog must have Thai and Indonesian content")
    for lang, item in data.items():
        if set(item.get("articles", {})) != set(SLUGS):
            raise ValueError(f"Localized Blog article set differs for {lang}")
        if len(item.get("ui", {}).get("nav", [])) != len(BUSINESS):
            raise ValueError(f"Localized Blog navigation is incomplete for {lang}")
        for slug, article in item["articles"].items():
            if not all(article.get(key) for key in ("title", "description", "summary", "relatedPage", "sections")):
                raise ValueError(f"Incomplete localized article {lang}/{slug}")
            if any(not section.get("heading") or not (section.get("paragraphs") or section.get("bullets"))
                   for section in article["sections"]):
                raise ValueError(f"Incomplete localized sections {lang}/{slug}")
    return data


def nav(lang, ui, slug=""):
    labels = ACCESS[lang]
    links = ''.join(f'<a href="/{lang}/{page}/">{escape(label)}</a>'
                    for page, label in zip(BUSINESS, ui["nav"]))
    return ('<header><div class="wrap nav"><a class="brand" href="/' + lang + '/" '
            'aria-label="' + labels["home"] + '"><img src="/assets/brand/all-konjac-wordmark.svg" '
            'alt="ALL KONJAC" width="220" height="31"></a>'
            '<button class="menu-toggle" type="button" aria-expanded="false" '
            'aria-controls="primary-navigation" aria-label="' + labels["menu"] + '" data-label-open="' + labels["menu"] + '" '
            'data-label-close="' + labels["close"] + '">' + labels["menu"] + '</button>'
            '<nav class="navlinks" id="primary-navigation" aria-label="' + labels["primary"] + '">' + links
            + f'<a href="{blog_path(lang=lang)}" aria-current="page">{escape(ui["blog"])}</a>'
            + f'<a href="/{lang}/#contact">{escape(ui["contact"])}</a></nav>'
            + language_switcher(slug, lang) + '</div></header>')


def footer(lang, ui):
    labels = ACCESS[lang]
    links = ''.join(f'<a href="/{lang}/{page}/">{escape(label)}</a>'
                    for page, label in zip(BUSINESS, ui["nav"]))
    return ('<footer><div class="wrap"><div class="foot"><div class="brand">'
            '<img src="/assets/brand/all-konjac-wordmark-white.svg" alt="ALL KONJAC" '
            'width="220" height="31"></div><nav class="footlinks" aria-label="' + labels["footer"] + '">'
            + links + f'<a href="{blog_path(lang=lang)}">{escape(ui["blog"])}</a>'
            + f'<a href="/{lang}/#contact">{escape(ui["contact"])}</a>'
            + '</nav></div><div class="copyright">© 2026 ALL KONJAC.</div></div></footer>')


def document(lang, slug, title, description, main, schema, ui):
    path = blog_path(slug, lang)
    e = lambda value: escape(value, quote=True)
    return ('<!doctype html>\n<html lang="' + lang + '"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="robots" content="index,follow,max-image-preview:large">'
            '<title>' + escape(title) + ' | ALL KONJAC</title>'
            '<meta name="description" content="' + e(description) + '">'
            '<link rel="canonical" href="' + BASE + path + '">' + alternate_links(slug)
            + '<meta property="og:type" content="' + ('article' if slug else 'website') + '">'
            '<meta property="og:site_name" content="ALL KONJAC">'
            '<meta property="og:title" content="' + e(title) + ' | ALL KONJAC">'
            '<meta property="og:description" content="' + e(description) + '">'
            '<meta property="og:url" content="' + BASE + path + '">'
            '<link rel="icon" type="image/svg+xml" href="/assets/brand/all-konjac-favicon.svg">'
            '<link rel="stylesheet" href="/assets/site.css">'
            '<script src="/assets/site.js" defer></script><script type="application/ld+json">'
            + json.dumps(schema, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
            + '</script></head><body><a class="skip-link" href="#main-content">' + ACCESS[lang]["skip"] + '</a>'
            + nav(lang, ui, slug) + '<main id="main-content">' + main + '</main>'
            + footer(lang, ui) + '</body></html>\n')


def render_index(lang, localized):
    ui = localized["ui"]
    cards = []
    for slug in SLUGS:
        article = localized["articles"][slug]
        category = ui["research"] if slug in RESEARCH else ui["guides"]
        cards.append('<article class="blog-card"><span class="eyebrow">' + escape(category) + '</span>'
                     '<h2><a href="' + blog_path(slug, lang) + '">' + escape(article["title"]) + '</a></h2>'
                     '<p>' + escape(article["summary"]) + '</p><a class="text-link" href="'
                     + blog_path(slug, lang) + '">' + escape(ui["read"]) + '</a></article>')
    main = ('<section class="page-hero blog-hero"><div class="wrap"><div class="eyebrow">ALL KONJAC</div>'
            '<h1>' + escape(ui["indexTitle"]) + '</h1><p>' + escape(ui["indexDescription"])
            + '</p></div></section><section class="blog-section"><div class="wrap"><div class="blog-grid">'
            + ''.join(cards) + '</div></div></section>')
    path = blog_path(lang=lang)
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Blog", "@id": BASE + path + "#blog", "url": BASE + path,
         "name": ui["indexTitle"], "description": ui["indexDescription"], "inLanguage": lang,
         "publisher": {"@id": BASE + "/#organization"}},
        {"@type": "WebPage", "@id": BASE + path + "#webpage", "url": BASE + path,
         "name": ui["indexTitle"], "inLanguage": lang, "isPartOf": {"@id": BASE + "/#website"}}
    ]}
    return document(lang, "", ui["indexTitle"], ui["indexDescription"], main, schema, ui)


def render_article(lang, slug, localized, evidence):
    ui = localized["ui"]
    article = localized["articles"][slug]
    path = blog_path(slug, lang)
    is_research = slug in RESEARCH
    sections = []
    for section in article["sections"]:
        body = ''.join('<p>' + escape(p) + '</p>' for p in section.get("paragraphs", []))
        if section.get("bullets"):
            body += '<ul>' + ''.join('<li>' + escape(p) + '</li>' for p in section["bullets"]) + '</ul>'
        sections.append('<section class="blog-content-section"><h2>' + escape(section["heading"])
                        + '</h2>' + body + '</section>')
    if is_research:
        refs = REFERENCES[slug]
        items = ''.join(f'<li><a href="{escape(url, quote=True)}" rel="noopener">[{i}] {escape(url)}</a></li>'
                        for i, url in enumerate(refs, 1))
        sources = ('<section class="blog-content-section blog-sources"><h2>' + escape(ui["sources"])
                   + '</h2><p>' + escape(ui["researchScope"]) + '</p><ol>' + items + '</ol></section>')
    else:
        en_article = next(a for a in evidence["articles"] if a["slug"] == slug)
        items = ''.join('<li><a href="/' + lang + '/' + source_id + '/">'
                        + escape(ui["nav"][BUSINESS.index(source_id)]) + '</a></li>'
                        for source_id in en_article["sources"])
        sources = ('<section class="blog-content-section blog-sources"><h2>' + escape(ui["sources"])
                   + '</h2><p>' + escape(ui["firstParty"]) + '</p><ul>' + items + '</ul></section>')
    date = "2026-10-20"
    category = ui["research"] if is_research else ui["guides"]
    main = ('<section class="page-hero blog-hero"><div class="wrap"><nav class="breadcrumbs" aria-label="' + ACCESS[lang]["breadcrumb"] + '">'
            '<ol><li><a href="/' + lang + '/">' + escape(ui["home"]) + '</a></li><li><a href="'
            + blog_path(lang=lang) + '">' + escape(ui["blog"]) + '</a></li><li aria-current="page">'
            + escape(article["title"]) + '</li></ol></nav><div class="eyebrow">' + escape(category)
            + '</div><h1>' + escape(article["title"]) + '</h1><p>' + escape(article["summary"])
            + '</p><p class="blog-date">' + escape(ui["published"]) + ' <time datetime="' + date + '">'
            + date + '</time> · ' + escape(ui["updated"]) + ' <time datetime="' + date + '">'
            + date + '</time></p></div></section><article class="blog-article wrap">' + ''.join(sections)
            + sources + '<div class="blog-next"><a class="btn primary" href="' + article["relatedPage"] + '">'
            + escape(ui["next"]) + '</a><a class="btn secondary" href="/' + lang + '/#contact">'
            + escape(ui["enquire"]) + '</a><a class="text-link" href="' + blog_path(lang=lang) + '">'
            + escape(ui["all"]) + '</a></div></article>')
    schema_article = {"@type": "BlogPosting", "@id": BASE + path + "#article", "url": BASE + path,
                      "headline": article["title"], "description": article["description"], "inLanguage": lang,
                      "datePublished": date, "dateModified": date,
                      "author": {"@id": BASE + "/#organization"},
                      "publisher": {"@id": BASE + "/#organization"},
                      "mainEntityOfPage": {"@id": BASE + path + "#webpage"}}
    if is_research:
        schema_article["citation"] = REFERENCES[slug]
    schema = {"@context": "https://schema.org", "@graph": [schema_article,
        {"@type": "WebPage", "@id": BASE + path + "#webpage", "url": BASE + path,
         "name": article["title"], "inLanguage": lang,
         "isPartOf": {"@id": BASE + "/#website"}}]}
    return document(lang, slug, article["title"], article["description"], main, schema, ui)
