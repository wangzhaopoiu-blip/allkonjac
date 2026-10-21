"""Translate only human-readable HTML fields; retain numbers, links and markup."""
from html.parser import HTMLParser
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
import html
import json
import re

TRANSLATED_ATTRIBUTES = {'alt', 'title', 'aria-label', 'data-label', 'data-title'}


def human_text(value):
    return bool(re.search(r'[A-Za-z\u4e00-\u9fff]', value)) and not (
        re.fullmatch(r'(?:ALL KONJAC|COA|EN|mPa·s|g/kg|mg/kg|pH|KGM|GB[^<]*|NY/T[^<]*|SP2605-0728-001|XSP202410483)', value))


class Localizer(HTMLParser):
    def __init__(self, mapping=None):
        super().__init__(convert_charrefs=True)
        self.mapping = mapping
        self.texts = set()
        self.parts = []
        self.script = False

    def translate(self, value):
        text = value.strip()
        if not human_text(text):
            return value
        self.texts.add(text)
        if self.mapping is None:
            return value
        if text not in self.mapping:
            raise ValueError('Missing quality translation: ' + text)
        return value.replace(text, self.mapping[text])

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.script = tag == 'script'
        for key, value in attrs.items():
            if value is None:
                continue
            if key in TRANSLATED_ATTRIBUTES or (tag == 'meta' and key == 'content' and
                    (attrs.get('name') == 'description' or attrs.get('property') == 'og:title')):
                attrs[key] = self.translate(value)
            elif key == 'href' and (value.startswith('https://wa.me/') or value.startswith('mailto:')):
                parsed = urlsplit(value)
                query = [(k, self.translate(v) if k in {'text', 'subject', 'body'} else v)
                         for k, v in parse_qsl(parsed.query)]
                attrs[key] = urlunsplit(parsed._replace(query=urlencode(query)))
        self.parts.append('<' + tag + ''.join(' ' + key + ('' if value is None else
                          '="' + html.escape(value, quote=True) + '"') for key, value in attrs.items()) + '>')

    def handle_endtag(self, tag):
        self.parts.append('</' + tag + '>')
        if tag == 'script':
            self.script = False

    def handle_data(self, text):
        self.parts.append(text if self.script else html.escape(self.translate(text), quote=False))

    def handle_decl(self, decl):
        self.parts.append('<!' + decl + '>')

    def handle_comment(self, text):
        self.parts.append('<!--' + text + '-->')


def localize(source, lang, root):
    if lang == 'en':
        return source
    mapping = json.loads((root / 'source/data/quality-translations.json').read_text(encoding='utf-8'))[lang]
    for original, translated in mapping.items():
        if re.findall(r'\d+(?:\.\d+)?', original) != re.findall(r'\d+(?:\.\d+)?', translated):
            raise ValueError('Quality translation changed a number: ' + original)
        if 'ALL KONJAC' in original and 'ALL KONJAC' not in translated:
            raise ValueError('Quality translation changed the brand: ' + original)
    parser = Localizer(mapping)
    parser.feed(source)
    result = ''.join(parser.parts)
    result = result.replace('href="/ingredients/', f'href="/{lang}/ingredients/')
    return result
