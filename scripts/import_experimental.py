#!/usr/bin/env python3
"""Import audited upstream JSONC examples into the opt-in Behify test subscription.

No dependencies outside Python 3 stdlib. Upstream Git blob SHA-1 is verified
before any file is changed. Review pin changes intentionally; never auto-update.
"""
import hashlib
import json
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPERIMENTAL = ROOT / 'experimental'
LICENSES = ROOT / 'licenses'

SOURCES = (
    {
        'owner': 'patterniha', 'repo': 'Serverless-for-Iran',
        'path': 'Serverless-fragA.jsonc',
        'blob': '7aea3fa58c302077bc4fe6a9c274560acaae02c3',
        'output': 'behify-08-fraga.json', 'remarks': 'Behify 08 | Patterniha fragA (test)',
    },
    {
        'owner': 'patterniha', 'repo': 'Serverless-for-Iran',
        'path': 'Serverless-fragB.jsonc',
        'blob': '4da540fab73e67649c3145c13782154ae0c5feb0',
        'output': 'behify-09-fragb.json', 'remarks': 'Behify 09 | Patterniha fragB (test)',
    },
    {
        'owner': 'XTLS', 'repo': 'Xray-examples',
        'path': 'Serverless-for-Iran/serverless_for_Iran.jsonc',
        'blob': '56a6c0e9b5c6f637d4ffa9655373e78bb9445ef7',
        'output': 'behify-10-xtls.json', 'remarks': 'Behify 10 | XTLS Serverless (test)',
    },
)

LICENSE_SOURCES = (
    ('patterniha', 'Serverless-for-Iran', 'LICENSE',
     'f288702d2fa16d3cdf0035b15a9fcbc552cd88e7',
     'Patterniha-GPL-3.0.txt'),
    ('XTLS', 'Xray-examples', 'LICENSE',
     'a73481c4be14b761eddf04cb18317cbc63416dc6',
     'XTLS-CC-BY-SA-4.0.txt'),
)


def source_url(owner, repo, path):
    return f'https://raw.githubusercontent.com/{owner}/{repo}/main/{path}'


def download_pinned(owner, repo, path, expected_blob):
    url = source_url(owner, repo, path)
    request = urllib.request.Request(url, headers={
        'User-Agent': 'Behify-configs-source-import/1.0',
    })
    with urllib.request.urlopen(request, timeout=30) as response:
        content = response.read()
    actual = hashlib.sha1(f'blob {len(content)}\0'.encode('ascii') + content).hexdigest()
    if actual != expected_blob:
        raise ValueError(
            f'Source changed (or wrong download): {url}\n'
            f'Expected Git blob {expected_blob}, got {actual}. No files written. '
            'Review upstream before updating any pin.'
        )
    return content


def strip_jsonc(text):
    """Remove JSONC line/block comments and trailing commas, preserving strings."""
    out = []
    i = 0
    quoted = False
    escaped = False
    while i < len(text):
        c = text[i]
        n = text[i + 1] if i + 1 < len(text) else ''
        if quoted:
            out.append(c)
            if escaped:
                escaped = False
            elif c == '\\':
                escaped = True
            elif c == '"':
                quoted = False
            i += 1
        elif c == '"':
            quoted = True
            out.append(c)
            i += 1
        elif c == '/' and n == '/':
            i += 2
            while i < len(text) and text[i] not in '\r\n':
                i += 1
        elif c == '/' and n == '*':
            i += 2
            end = text.find('*/', i)
            if end < 0:
                raise ValueError('Unterminated JSONC block comment')
            out.extend('\n' for c in text[i:end] if c == '\n')
            i = end + 2
        else:
            out.append(c)
            i += 1
    if quoted:
        raise ValueError('Unterminated JSONC string')
    uncommented = ''.join(out)
    # Trailing commas are permitted in JSONC but not JSON.
    # Only remove a comma when the next non-whitespace outside a string is ] or }.
    out = []
    quoted = False
    escaped = False
    for i, c in enumerate(uncommented):
        if quoted:
            out.append(c)
            if escaped:
                escaped = False
            elif c == '\\':
                escaped = True
            elif c == '"':
                quoted = False
            continue
        if c == '"':
            quoted = True
        if c == ',':
            following = uncommented[i + 1:].lstrip()
            if following.startswith(('}', ']')):
                continue
        out.append(c)
    return ''.join(out)


def adapt(content, label):
    profile = json.loads(strip_jsonc(content.decode('utf-8-sig')))
    if not isinstance(profile, dict):
        raise ValueError('Expected one Xray configuration object')
    # The author/donation metadata is documented in docs/experimental-sources.md.
    profile.pop('__Credits__', None)
    profile['remarks'] = label
    inbounds = profile.get('inbounds')
    if not isinstance(inbounds, list) or not inbounds:
        raise ValueError('Source has no inbounds')
    for inbound in inbounds:
        # Upstream omits 'listen'. Never expose local SOCKS/DNS ports publicly.
        if inbound.get('listen', '127.0.0.1') not in ('127.0.0.1', '::1'):
            raise ValueError('Source has a non-loopback inbound; manual review required')
        inbound['listen'] = '127.0.0.1'
    profile.setdefault('log', {})['loglevel'] = 'warning'
    profile['log']['dnsLog'] = False
    return profile


def main():
    # Stage downloads/transforms entirely in memory before writing anything.
    staged = []
    for spec in SOURCES:
        original = download_pinned(spec['owner'], spec['repo'], spec['path'], spec['blob'])
        profile = adapt(original, spec['remarks'])
        rendered = json.dumps(profile, ensure_ascii=False, indent=2) + '\n'
        staged.append((EXPERIMENTAL / spec['output'], rendered.encode('utf-8')))
    for owner, repo, path, blob, filename in LICENSE_SOURCES:
        license_bytes = download_pinned(owner, repo, path, blob)
        staged.append((LICENSES / filename, license_bytes))

    for target, content in staged:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        print(f'Wrote {target.relative_to(ROOT)}')
    print('Imported 3 pinned experimental profiles. Next: python scripts/build.py')


if __name__ == '__main__':
    main()
