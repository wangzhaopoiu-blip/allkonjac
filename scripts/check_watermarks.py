"""Reject unwatermarked, unclassified or modified public images before a site build."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.svg'}


def verify_watermarks(root=ROOT):
    assets = root / 'assets'
    manifest = json.loads((root / 'source/image-watermark.json').read_text(encoding='utf-8'))
    records = manifest['images'] + manifest['exempt']
    expected = {record['path'] for record in records}
    actual = {file.relative_to(assets).as_posix() for file in assets.rglob('*') if file.is_file() and file.suffix.lower() in EXTENSIONS}
    if len(expected) != len(records) or actual != expected:
        raise ValueError(f'Watermark image inventory mismatch; new={sorted(actual - expected)}, missing={sorted(expected - actual)}')
    for record in records:
        file = assets / record['path']
        if file.resolve().parent != assets.resolve() and assets.resolve() not in file.resolve().parents:
            raise ValueError('Image path escapes assets directory')
        data = file.read_bytes()
        # Git may check SVG text out with CRLF on Windows and LF on Linux.
        if file.suffix.lower() == '.svg':
            data = data.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
        digest = hashlib.sha256(data).hexdigest()
        if digest != record.get('watermarkedSha256', record.get('sha256')):
            raise ValueError('Unapproved or unwatermarked public image: ' + record['path'])
    logo = next(record for record in manifest['exempt'] if record['path'] == manifest.get('logoPath', 'company-mark.jpg'))
    if logo['sha256'] != manifest['logoSha256']:
        raise ValueError('Approved logo hash differs')
    if any(record['watermarkedSha256'] == record['originalSha256'] or record['changedPixelRatio'] < manifest.get('minimumChangedPixelRatio', 0.01) for record in manifest['images']):
        raise ValueError('An image has no verified watermark')
    return {'business_images': len(manifest['images']), 'exempt_images': len(manifest['exempt']), 'passed': True}


if __name__ == '__main__':
    print(json.dumps(verify_watermarks(), ensure_ascii=False))
