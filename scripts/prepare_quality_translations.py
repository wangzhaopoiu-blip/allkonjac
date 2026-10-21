"""One-time translation preparation; not used during reproducible builds."""
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from pathlib import Path
import json
import time
import subprocess
from quality_content import english_summary, english_materials, english_detail_page
from quality_localization import Localizer

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'source/data/quality-google-raw.json'


def translate(text, language, source='en'):
    url = 'https://translate.googleapis.com/translate_a/single?' + urlencode(
        {'client': 'gtx', 'sl': source, 'tl': language, 'dt': 't', 'q': text})
    for attempt in range(3):
        try:
            response = subprocess.run(['curl.exe', '-f', '-sS', '--max-time', '20', url], capture_output=True, encoding='utf-8', check=True)
            result = json.loads(response.stdout)
            return ''.join(item[0] for item in result[0] if item[0])
        except Exception:
            if attempt == 2:
                raise
            time.sleep(1)


if __name__ == '__main__':
    parser = Localizer()
    parser.feed(english_summary() + english_materials() + english_detail_page('<header></header><footer></footer>'))
    raw = json.loads(CACHE.read_text(encoding='utf-8')) if CACHE.exists() else {'en': {}, 'th': {}, 'id': {}}
    # Retain the original Google result for Chinese labels before terminology calibration.
    jobs = [('en', value, 'zh-CN') for value in ['魔芋胶', '特级', '纯化魔芋粉'] if value not in raw['en']]
    jobs += [(lang, value, 'en') for lang in ['th', 'id'] for value in sorted(parser.texts) if value not in raw[lang]]

    def work(job):
        lang, value, source = job
        return lang, value, translate(value, lang, source)

    with ThreadPoolExecutor(max_workers=6) as pool:
        for index, (lang, key, value) in enumerate(pool.map(work, jobs), 1):
            raw[lang][key] = value
            CACHE.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            if index % 40 == 0:
                print(f'Translated {index}/{len(jobs)} strings', flush=True)
    # Keep raw output separate; apply auditable terminology corrections here.
    replacements = {
        'th': [('หมากฝรั่งบุก', 'กัมบุก'), ('แป้งบุกบริสุทธิ์', 'ผงบุกบริสุทธิ์'),
               ('เครื่องอบผ้า', 'เครื่องอบแห้ง'), ('แอปพลิเคชัน', 'การใช้งาน')],
        'id': [('permen karet konjak', 'gom konjak'), ('permen karet konjac', 'gom konjak'),
               ('Permen karet konjak', 'Gom konjak'), ('Permen karet konjac', 'Gom konjak'),
               ('jalur pengering', 'lini pengering'), ('aplikasi Anda', 'aplikasi pangan Anda')]
    }
    reviewed = {}
    for lang in ['th', 'id']:
        reviewed[lang] = {}
        for key, value in raw[lang].items():
            for old, new in replacements[lang]:
                value = value.replace(old, new)
            reviewed[lang][key] = value
    overrides = json.loads((ROOT / 'source/data/quality-editorial-overrides.json').read_text(encoding='utf-8'))
    for lang in reviewed:
        reviewed[lang].update(overrides[lang])
    (ROOT / 'source/data/quality-translations.json').write_text(
        json.dumps(reviewed, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Prepared {len(parser.texts)} strings for each language.')
