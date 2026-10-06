"""Render the ALL KONJAC static site using only Python's standard library.

Run `python scripts/build.py` after all three reviewed catalogs are available.
No network, deployment, dependencies, or English fallback is involved.
"""
from pathlib import Path
import argparse
import copy
import html
from html.parser import HTMLParser
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://allkonjac.com"
PAGES = ["", "ingredients", "equipment", "drying-lines", "technology"]
LANGUAGES = {
    "en": {"prefix": "", "label": "English", "short": "EN", "og": "en_US", "flag": "gb"},
    "th": {"prefix": "/th", "label": "ภาษาไทย", "short": "TH", "og": "th_TH", "flag": "th"},
    "id": {"prefix": "/id", "label": "Bahasa Indonesia", "short": "ID", "og": "id_ID", "flag": "id"},
}
TOKEN = re.compile(r"\{\{([^{}]+)\}\}")
GLOBAL_IDS = {BASE + "/#organization", BASE + "/#website"}


def page_path(page, lang):
    return LANGUAGES[lang]["prefix"] + "/" + (page + "/" if page else "")


def page_url(page, lang):
    return BASE + page_path(page, lang)


def read_json(path):
    try:
        # utf-8-sig accepts dictionaries saved with a Windows UTF-8 BOM.
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read {path.relative_to(ROOT)}: {exc}") from exc


def validate_catalog(catalog, language, english=None):
    if not isinstance(catalog, dict) or not catalog:
        raise ValueError(f"content/{language}.json must be a non-empty object of string IDs to strings")
    bad = [key for key, value in catalog.items()
           if not isinstance(key, str) or not isinstance(value, str) or not value.strip()]
    if bad:
        raise ValueError(f"content/{language}.json has invalid or empty strings: {', '.join(map(str, bad))}")
    if english is not None:
        missing = sorted(set(english) - set(catalog))
        extra = sorted(set(catalog) - set(english))
        if missing or extra:
            raise ValueError(f"content/{language}.json key mismatch; missing={missing}; extra={extra}")
        # Contact details and brand facts must survive translation verbatim.
        protected = ["ALL KONJAC", "WhatsApp", "WeChat", "583411495@qq.com",
                     "+86 15637136906", "+86 156 3713 6906"]
        changed = []
        for key, original in english.items():
            for fact in protected:
                if fact in original and fact not in catalog[key]:
                    changed.append(f"{key}: {fact}")
            if sorted(re.findall(r"(?<!\w)\d+(?!\w)", original)) != sorted(
                re.findall(r"(?<!\w)\d+(?!\w)", catalog[key])):
                changed.append(f"{key}: numeric facts")
        if changed:
            raise ValueError(f"content/{language}.json changed protected facts: " + "; ".join(changed))


def translated(value, catalog):
    if isinstance(value, dict):
        if set(value) == {"$t"}:
            return catalog[value["$t"]]
        return {key: translated(item, catalog) for key, item in value.items()}
    if isinstance(value, list):
        return [translated(item, catalog) for item in value]
    return value


def local_url(url, lang):
    if url in GLOBAL_IDS:
        return url
    for page in PAGES:
        source = page_url(page, "en")
        if url == source or url.startswith(source + "#"):
            return page_url(page, lang) + url[len(source):]
    return url


def local_schema(value, lang, global_node=False):
    if isinstance(value, dict):
        node_type = value.get("@type")
        keep_global = global_node or node_type in {"Organization", "WebSite"}
        result = {}
        for key, item in value.items():
            if key == "inLanguage":
                result[key] = list(LANGUAGES) if node_type == "WebSite" else lang
            elif isinstance(item, str) and key in {"@id", "url", "item"} and not keep_global:
                result[key] = local_url(item, lang)
            else:
                result[key] = local_schema(item, lang, keep_global)
        return result
    if isinstance(value, list):
        return [local_schema(item, lang, global_node) for item in value]
    return value


def json_for_script(value):
    # Escape '<' so a translated string cannot terminate the script element.
    return json.dumps(value, ensure_ascii=False, indent=2).replace("<", "\\u003c").replace(
        "\u2028", "\\u2028").replace("\u2029", "\\u2029")


def schema_for(page, lang, catalog):
    name = page or "home"
    schema = local_schema(translated(read_json(ROOT / "source/schema" / (name + ".json")), catalog), lang)
    graph = schema["@graph"]
    if not any(node.get("@type") == "WebSite" for node in graph):
        graph.append({"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/",
                      "name": "ALL KONJAC", "inLanguage": list(LANGUAGES),
                      "publisher": {"@id": BASE + "/#organization"}})
    return schema


def seo_links(page, lang):
    parts = [f'<link rel="canonical" href="{page_url(page, lang)}">']
    for variant in LANGUAGES:
        parts.append(f'<link rel="alternate" hreflang="{variant}" href="{page_url(page, variant)}">')
    parts.append(f'<link rel="alternate" hreflang="x-default" href="{page_url(page, "en")}">')
    for variant, info in LANGUAGES.items():
        if variant != lang:
            parts.append(f'<meta property="og:locale:alternate" content="{info["og"]}">')
    return "\n".join(parts)


def language_flag(info):
    # The adjacent language name supplies the accessible label; flags are decorative.
    return (f'<img class="language-flag" src="/assets/flags/{info["flag"]}.svg" '
            'alt="" aria-hidden="true" width="24" height="16">')


def language_switcher(page, lang, catalog):
    info = LANGUAGES[lang]
    label = html.escape(catalog["ui.language_choose"] + ": " + info["label"], quote=True)
    parts = ['<details class="language-switcher">',
             f'<summary class="language-summary" data-current-locale="{info["short"]}" aria-label="{label}">'
             + language_flag(info) + f'<span>{info["short"]}</span></summary>',
             '<div class="language-options">']
    for variant, variant_info in LANGUAGES.items():
        active = ' aria-current="page"' if variant == lang else ""
        check = '<span class="language-check" aria-hidden="true">✓</span>' if variant == lang else ""
        parts.append(f'<a href="{page_path(page, variant)}" lang="{variant}" hreflang="{variant}"{active}>'
                     + language_flag(variant_info) + f'<span class="language-label">{variant_info["label"]}</span>'
                     + check + '</a>')
    parts.append("</div></details>")
    return "".join(parts)


def localized_internal_links(source, lang):
    def replace(match):
        target = match.group(1)
        for page in PAGES:
            english_path = page_path(page, "en")
            if target == english_path or target.startswith(english_path + "#"):
                return 'href="' + page_path(page, lang) + target[len(english_path):] + '"'
        return match.group(0)
    return re.sub(r'href="([^"]+)"', replace, source)


def render_page(page, lang, catalog):
    source = (ROOT / "source/templates" / ((page or "home") + ".html")).read_text(encoding="utf-8")
    source = localized_internal_links(source, lang)
    dynamic = {
        "lang": lang, "og_locale": LANGUAGES[lang]["og"], "canonical": page_url(page, lang),
        "seo_links": seo_links(page, lang), "language_switcher": language_switcher(page, lang, catalog),
        "motion_attributes": ' class="motion-enabled"',
        "jsonld": '<script type="application/ld+json">' + json_for_script(schema_for(page, lang, catalog)) + '</script>',
    }
    def substitute(match):
        token = match.group(1)
        if token.startswith(("t:", "a:")):
            mode, key = token.split(":", 1)
            if key not in catalog:
                raise ValueError(f"{lang}/{page or 'home'}: missing translation key {key}")
            return html.escape(catalog[key], quote=mode == "a")
        if token not in dynamic:
            raise ValueError(f"Unknown template token {token}")
        return dynamic[token]
    output = TOKEN.sub(substitute, source)
    if TOKEN.search(output):
        raise ValueError(f"Unresolved template token in {lang}/{page or 'home'}")
    return output.rstrip() + "\n"


def render_404(catalogs):
    title = " / ".join(catalogs[lang]["error.title"] for lang in LANGUAGES)
    parts = ['<!doctype html>', '<html lang="en"><head><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width,initial-scale=1">',
             '<meta name="robots" content="noindex,follow">',
             '<title>' + html.escape(title) + '</title>', '<link rel="stylesheet" href="/assets/site.css">',
             '</head><body><main class="wrap page-hero error-page"><div class="brand">ALL <span>KONJAC</span></div>']
    for lang, info in LANGUAGES.items():
        catalog = catalogs[lang]
        parts.extend([f'<section lang="{lang}" class="error-language">',
                      '<div class="eyebrow">' + info["label"] + '</div>',
                      '<h1>' + html.escape(catalog["error.heading"]) + '</h1>',
                      '<p>' + html.escape(catalog["error.description"]) + '</p>',
                      f'<a class="text-link" href="{page_path("", lang)}">' + html.escape(catalog["error.return"]) + '</a>',
                      '</section>'])
    parts.append('</main></body></html>')
    return "\n".join(parts) + "\n"


def render_sitemap():
    ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
    ET.register_namespace("xhtml", "http://www.w3.org/1999/xhtml")
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    xhtml = "{http://www.w3.org/1999/xhtml}"
    root = ET.Element(namespace + "urlset")
    for lang in LANGUAGES:
        for page in PAGES:
            node = ET.SubElement(root, namespace + "url")
            ET.SubElement(node, namespace + "loc").text = page_url(page, lang)
            for variant in LANGUAGES:
                ET.SubElement(node, xhtml + "link", {"rel": "alternate", "hreflang": variant, "href": page_url(page, variant)})
            ET.SubElement(node, xhtml + "link", {"rel": "alternate", "hreflang": "x-default", "href": page_url(page, "en")})
    ET.indent(root, space="  ")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode") + "\n"


def render_llms(catalogs):
    english = catalogs["en"]
    home = schema_for("", "en", english)
    organization = next(node for node in home["@graph"] if node.get("@type") == "Organization")
    parts = ["# ALL KONJAC", "", "> " + organization["description"], "",
             "The canonical website is https://allkonjac.com/. Public business pages are available in English, Thai and Indonesian. Each language section links to the equivalent business pages. Project specifications and supply or development scope are confirmed through an enquiry.", ""]
    for lang, info in LANGUAGES.items():
        parts.extend(["## " + info["label"],
                      f'- [ALL KONJAC]({page_url("", lang)}): Business overview and buyer questions.'])
        for page in PAGES[1:]:
            service = next(node for node in schema_for(page, lang, catalogs[lang])["@graph"] if node.get("@type") == "Service")
            parts.append(f'- [{service["name"]}]({page_url(page, lang)}): {service["description"]}')
        parts.append("")
    parts.extend(["## Contact", "- [Project enquiries](https://allkonjac.com/#contact): Email 583411495@qq.com; WhatsApp +86 15637136906.", "",
                  "## Website discovery", "- [Sitemap](https://allkonjac.com/sitemap.xml): The 15 canonical business pages and their language alternates.", "",
                  "This optional summary helps tools that choose to read it. It does not replace the visible website content, robots.txt, or sitemap, and does not guarantee search rankings or AI citations.", ""])
    return "\n".join(parts)


class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def validate_output(output, page, lang):
    parser = AuditParser()
    parser.feed(output)
    tags = parser.tags
    root = next(attrs for tag, attrs in tags if tag == "html")
    if root.get("lang") != lang:
        raise ValueError("Incorrect html lang")
    body = next(attrs for tag, attrs in tags if tag == "body")
    if "motion-enabled" not in body.get("class", "").split():
        raise ValueError("Motion must be enabled on every business page")
    links = [attrs for tag, attrs in tags if tag == "link"]
    canonical = [link["href"] for link in links if link.get("rel") == "canonical"]
    if canonical != [page_url(page, lang)]:
        raise ValueError(f"Invalid canonical for {page}/{lang}")
    alternates = {link.get("hreflang"): link.get("href") for link in links if link.get("rel") == "alternate"}
    expected = {variant: page_url(page, variant) for variant in LANGUAGES}
    expected["x-default"] = page_url(page, "en")
    if alternates != expected:
        raise ValueError(f"Invalid language alternates for {page}/{lang}")
    language_links = [attrs for tag, attrs in tags if tag == "a" and "hreflang" in attrs]
    if len(language_links) != 3 or sum(link.get("aria-current") == "page" for link in language_links) != 1:
        raise ValueError("Language switch must have three links and one current link")
    for tag, attrs in tags:
        if "src" in attrs and tag in {"img", "script"} and not attrs["src"].startswith("/assets/"):
            raise ValueError(f"Non-root asset URL: {attrs['src']}")
    schema_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', output, re.S)
    schema = json.loads(schema_match.group(1))
    for node in schema["@graph"]:
        kind = node.get("@type")
        if kind in {"WebPage", "Service", "ItemList", "BreadcrumbList"} and not node["@id"].startswith(page_url(page, lang)):
            raise ValueError(f"Unlocalized {kind} identity")
        if kind == "WebPage" and (node.get("url") != page_url(page, lang) or node.get("inLanguage") != lang):
            raise ValueError("Unlocalized WebPage")
        if kind == "Organization" and (node.get("@id") != BASE + "/#organization" or node.get("url") != BASE + "/"):
            raise ValueError("Global Organization identity changed")
        if kind == "WebSite" and (node.get("@id") != BASE + "/#website" or node.get("inLanguage") != list(LANGUAGES)):
            raise ValueError("Global WebSite identity or language set changed")


def self_test(english):
    # Check every template/URL transformation before translations are available;
    # rendering stays in memory and does not create English placeholder locales.
    for lang in LANGUAGES:
        for page in PAGES:
            validate_output(render_page(page, lang, english), page, lang)
    hostile = 'A "quote" & <tag> </script> ภาษาไทย Bahasa Indonesia'
    probe = copy.deepcopy(english)
    title_key = re.search(r'<title>\{\{t:([^}]+)\}\}</title>', (ROOT / "source/templates/home.html").read_text(encoding="utf-8")).group(1)
    probe[title_key] = hostile
    output = render_page("", "th", probe)
    validate_output(output, "", "th")
    if '<title>' + html.escape(hostile, quote=False) + '</title>' not in output:
        raise ValueError("Text escaping test failed")
    if 'content="' + html.escape(hostile, quote=True) + '"' not in output:
        raise ValueError("Attribute escaping test failed")
    schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', output, re.S).group(1))
    if next(node for node in schema["@graph"] if node.get("@type") == "WebPage")["name"] != hostile:
        raise ValueError("JSON escaping round-trip test failed")
    bad = dict(english)
    bad.pop(next(iter(bad)))
    try:
        validate_catalog(bad, "test", english)
    except ValueError:
        pass
    else:
        raise ValueError("Missing-translation validation test failed")
    if len(ET.fromstring(render_sitemap()).findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")) != 15:
        raise ValueError("Sitemap page count test failed")


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("--check", action="store_true", help="validate all catalogs and render in memory without changing files")
    args.add_argument("--self-test", action="store_true", help="verify templates, links, schema, escaping and missing-key rejection using English in memory")
    options = args.parse_args()
    english = read_json(ROOT / "content/en.json")
    validate_catalog(english, "en")
    if options.self_test:
        self_test(english)
        print(f"Self-test passed: 15 template variants, escaping, strict key validation and sitemap ({len(english)} strings). No output written.")
        return
    catalogs = {"en": english}
    for lang in list(LANGUAGES)[1:]:
        catalogs[lang] = read_json(ROOT / "content" / (lang + ".json"))
        validate_catalog(catalogs[lang], lang, english)
    output = {}
    for lang in LANGUAGES:
        for page in PAGES:
            rendered = render_page(page, lang, catalogs[lang])
            validate_output(rendered, page, lang)
            output[page_path(page, lang).lstrip("/") + "index.html"] = rendered
    output["404.html"] = render_404(catalogs)
    output["sitemap.xml"] = render_sitemap()
    output["llms.txt"] = render_llms(catalogs)
    if not options.check:
        # Nothing writes until every language, template and schema passes.
        for relative, rendered in output.items():
            target = ROOT / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"{'Validated' if options.check else 'Generated'} 15 business pages, trilingual 404, sitemap and llms.txt; {len(english)} strings in each catalog.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError) as exc:
        print("Build failed: " + str(exc), file=sys.stderr)
        sys.exit(1)
