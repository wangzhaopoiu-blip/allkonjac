"""Render the English-only editorial section for the static ALL KONJAC site."""
from datetime import date
from html import escape
import json
from pathlib import Path
import re

BASE = "https://allkonjac.com"
BLOG = "/blog/"
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
ARTICLE_LINKS = {
    "ingredients": "choose-konjac-powder-gum",
    "equipment": "konjac-equipment-project-brief",
    "drying-lines": "plan-konjac-dried-chip-drying-line",
}


def article_path(article):
    return BLOG + article["slug"] + "/"


def load_editorial(root):
    articles = json.loads((root / "source/blog/articles.json").read_text(encoding="utf-8"))
    evidence = json.loads((root / "source/blog/evidence.json").read_text(encoding="utf-8"))
    if not isinstance(articles, list) or len(articles) != 3:
        raise ValueError("Blog must contain the three reviewed launch articles")
    if not isinstance(evidence, dict) or not isinstance(evidence.get("sources"), dict):
        raise ValueError("Blog evidence registry is missing")
    seen = set()
    for article in articles:
        required = ("slug", "title", "description", "summary", "datePublished", "dateModified",
                    "category", "relatedPage", "relatedLabel", "sources", "sections")
        if any(not article.get(key) for key in required):
            raise ValueError("Incomplete blog article metadata")
        slug = article["slug"]
        if not SLUG.fullmatch(slug) or slug in seen:
            raise ValueError(f"Invalid or duplicate blog slug: {slug}")
        seen.add(slug)
        published = date.fromisoformat(article["datePublished"])
        modified = date.fromisoformat(article["dateModified"])
        if modified < published:
            raise ValueError(f"Blog modification precedes publication: {slug}")
        if article["relatedPage"] not in {"/ingredients/", "/equipment/", "/drying-lines/"}:
            raise ValueError(f"Invalid related business page: {slug}")
        if not isinstance(article["sections"], list) or not article["sections"]:
            raise ValueError(f"Blog article needs sections: {slug}")
        for section in article["sections"]:
            if not section.get("heading") or not (section.get("paragraphs") or section.get("bullets")):
                raise ValueError(f"Incomplete article section: {slug}")
        for source_id in article["sources"]:
            source = evidence["sources"].get(source_id)
            if not source or not source.get("label") or not source.get("supports"):
                raise ValueError(f"Missing evidence source {source_id}: {slug}")
            if source["url"] != BASE + "/" + source_id + "/":
                raise ValueError(f"Evidence URL must use an existing business page: {source_id}")
        claims = evidence.get("claims", {}).get(slug)
        if not isinstance(claims, list) or not claims:
            raise ValueError(f"Missing claim-level evidence for {slug}")
        for item in claims:
            if not item.get("claim") or item.get("source") not in article["sources"]:
                raise ValueError(f"Invalid claim-level evidence for {slug}")
    return articles, evidence


def add_business_links(source, page):
    """Keep the legacy templates untouched outside the English render."""
    contact_link = '<a href="/#contact">'
    if source.count(contact_link) != 2:
        raise ValueError(f"Cannot find English navigation and footer in {page or 'home'}")
    source = source.replace(contact_link, '<a href="/blog/">Blog</a>' + contact_link)
    if page in ARTICLE_LINKS:
        link = ('<a href="/blog/' + ARTICLE_LINKS[page] + '/">Read the buyer guide</a>')
        pattern = r'(<div class="related-links">.*?)(</div>)'
        source, count = re.subn(pattern, lambda match: match.group(1) + link + match.group(2), source,
                                count=1, flags=re.S)
        if count != 1:
            raise ValueError(f"Cannot find related links in {page}")
    return source


def json_script(schema):
    return json.dumps(schema, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def shared_header(current):
    nav = [("/ingredients/", "Ingredients"), ("/equipment/", "Equipment"),
           ("/drying-lines/", "Drying Lines"), ("/technology/", "Technology"),
           ("/blog/", "Blog"), ("/#contact", "Contact")]
    links = "".join('<a href="' + path + '"' + (' aria-current="page"' if path == current else '')
                    + '>' + label + '</a>' for path, label in nav)
    return ('<header><div class="wrap nav"><a class="brand" href="/" aria-label="ALL KONJAC home">'
            '<img src="/assets/brand/all-konjac-wordmark.svg" alt="ALL KONJAC" width="220" height="31"></a>'
            '<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-navigation" '
            'aria-label="Open menu" data-label-open="Open menu" data-label-close="Close menu">Menu</button>'
            '<nav class="navlinks" id="primary-navigation" aria-label="Primary navigation">' + links + '</nav></div></header>')


def shared_footer():
    return ('<footer><div class="wrap"><div class="foot"><div><div class="brand">'
            '<img src="/assets/brand/all-konjac-wordmark-white.svg" alt="ALL KONJAC" width="220" height="31"></div>'
            '<small>Konjac Ingredients · Equipment · Intelligent Manufacturing · Technology Solutions</small></div>'
            '<nav class="footlinks" aria-label="Footer"><a href="/ingredients/">Ingredients</a>'
            '<a href="/equipment/">Equipment</a><a href="/drying-lines/">Drying Lines</a>'
            '<a href="/technology/">Technology</a><a href="/blog/">Blog</a><a href="/#contact">Contact</a>'
            '</nav></div><div class="copyright">© 2026 ALL KONJAC.</div></div></footer>')


def document(path, title, description, main, schema, page_type="website"):
    canonical = BASE + path
    e = lambda value: escape(value, quote=True)
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>' + e(title) + ' | ALL KONJAC</title>'
            '<meta name="description" content="' + e(description) + '">'
            '<meta name="robots" content="index,follow,max-image-preview:large">'
            '<link rel="canonical" href="' + canonical + '">'
            '<meta property="og:type" content="' + page_type + '">'
            '<meta property="og:site_name" content="ALL KONJAC">'
            '<meta property="og:locale" content="en_US">'
            '<meta property="og:title" content="' + e(title) + ' | ALL KONJAC">'
            '<meta property="og:description" content="' + e(description) + '">'
            '<meta property="og:url" content="' + canonical + '">'
            '<link rel="icon" type="image/svg+xml" href="/assets/brand/all-konjac-favicon.svg">'
            '<link rel="icon" sizes="any" href="/favicon.ico">'
            '<link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon.png">'
            '<link rel="stylesheet" href="/assets/site.css">'
            '<script src="/assets/site.js" defer></script>'
            '<script type="application/ld+json">' + json_script(schema) + '</script>'
            '</head><body><a class="skip-link" href="#main-content">Skip to content</a>'
            + shared_header("/blog/") + '<main id="main-content">' + main + '</main>'
            + shared_footer() + '</body></html>\n')


def breadcrumb(items):
    visible = '<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>'
    entries = []
    for position, (label, path) in enumerate(items, 1):
        entries.append({"@type": "ListItem", "position": position, "name": label, "item": BASE + path})
        visible += ('<li><a href="' + path + '">' + escape(label) + '</a></li>' if position < len(items)
                    else '<li aria-current="page">' + escape(label) + '</li>')
    return visible + '</ol></nav>', entries


def render_index(articles):
    crumbs, entries = breadcrumb([("Home", "/"), ("Blog", BLOG)])
    cards = []
    for article in articles:
        cards.append('<article class="blog-card"><span class="eyebrow">' + escape(article["category"]) + '</span>'
                     '<h2><a href="' + article_path(article) + '">' + escape(article["title"]) + '</a></h2>'
                     '<p>' + escape(article["summary"]) + '</p><a class="text-link" href="'
                     + article_path(article) + '">Read the guide</a></article>')
    main = ('<section class="page-hero blog-hero"><div class="wrap">' + crumbs + '<div class="eyebrow">Buyer guides</div>'
            '<h1>Konjac project guides</h1><p>Practical starting points for ingredient selection, equipment enquiries and drying-line planning. Confirm grades, specifications and project scope before ordering.</p>'
            '</div></section><section class="blog-section"><div class="wrap"><div class="blog-grid">'
            + ''.join(cards) + '</div><p class="blog-scope">These guides use first-party ALL KONJAC business pages as sources. They are planning guidance, not independent product tests or project specifications.</p></div></section>')
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Blog", "@id": BASE + BLOG + "#blog", "url": BASE + BLOG,
         "name": "Konjac project guides", "description": "Buyer guides for konjac project planning.",
         "inLanguage": "en", "publisher": {"@id": BASE + "/#organization"},
         "blogPost": [{"@id": BASE + article_path(article) + "#article"} for article in articles]},
        {"@type": "BreadcrumbList", "@id": BASE + BLOG + "#breadcrumb", "itemListElement": entries}
    ]}
    return document(BLOG, "Konjac Project Guides", "Buyer guides for konjac ingredients, food equipment and dried-chip drying lines.", main, schema)


def render_article(article, evidence):
    path = article_path(article)
    crumbs, entries = breadcrumb([("Home", "/"), ("Blog", BLOG), (article["title"], path)])
    sections = []
    for section in article["sections"]:
        parts = ['<section class="blog-content-section"><h2>' + escape(section["heading"]) + '</h2>']
        if section.get("bullets"):
            parts.append('<ul>' + ''.join('<li>' + escape(item) + '</li>' for item in section["bullets"]) + '</ul>')
        parts.extend('<p>' + escape(paragraph) + '</p>' for paragraph in section.get("paragraphs", []))
        parts.append('</section>')
        sections.append(''.join(parts))
    source_items = []
    for source_id in article["sources"]:
        source = evidence["sources"][source_id]
        source_items.append('<li><a href="' + source["url"] + '">' + escape(source["label"])
                            + '</a> — ' + escape(source["supports"]) + '</li>')
    main = ('<section class="page-hero blog-hero"><div class="wrap">' + crumbs
            + '<div class="eyebrow">' + escape(article["category"]) + ' · Buyer guide</div><h1>'
            + escape(article["title"]) + '</h1><p>' + escape(article["summary"]) + '</p>'
            + '<p class="blog-date">Published <time datetime="' + article["datePublished"] + '">'
            + article["datePublished"] + '</time> · Updated <time datetime="' + article["dateModified"] + '">'
            + article["dateModified"] + '</time></p></div></section>'
            + '<article class="blog-article wrap">' + ''.join(sections)
            + '<section class="blog-content-section blog-sources"><h2>Sources and scope</h2><p>'
            + escape(evidence["basis"]) + '</p><ul>' + ''.join(source_items) + '</ul></section>'
            + '<div class="blog-next"><a class="btn primary" href="' + article["relatedPage"] + '">'
            + escape(article["relatedLabel"]) + '</a><a class="text-link" href="/blog/">All buyer guides</a>'
            + '</div></article>')
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "@id": BASE + path + "#article", "url": BASE + path,
         "headline": article["title"], "description": article["description"], "inLanguage": "en",
         "datePublished": article["datePublished"], "dateModified": article["dateModified"],
         "author": {"@id": BASE + "/#organization"}, "publisher": {"@id": BASE + "/#organization"},
         "mainEntityOfPage": {"@id": BASE + path + "#webpage"},
         "isPartOf": {"@id": BASE + BLOG + "#blog"}},
        {"@type": "WebPage", "@id": BASE + path + "#webpage", "url": BASE + path,
         "name": article["title"], "inLanguage": "en", "isPartOf": {"@id": BASE + "/#website"},
         "breadcrumb": {"@id": BASE + path + "#breadcrumb"}},
        {"@type": "BreadcrumbList", "@id": BASE + path + "#breadcrumb", "itemListElement": entries}
    ]}
    return document(path, article["title"], article["description"], main, schema, "article")
