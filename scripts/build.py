#!/usr/bin/env python3
"""Validate Xray JSON profile lists and generate separate stable/test subscriptions."""
import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
GROUPS = (
    (ROOT / 'profiles', 'behify-*.json', ROOT / 'sub' / 'v2rayng.json', None),
    (ROOT / 'experimental', 'behify-*.json',
     ROOT / 'sub' / 'experimental-v2rayng.json',
     {'behify-08-fraga.json', 'behify-09-fragb.json', 'behify-10-xtls.json'}),
)


def load_and_validate(folder, pattern, expected_names=None):
    files = sorted(folder.glob(pattern))
    if not files:
        raise ValueError(f'{folder.relative_to(ROOT)}: no profiles found')
    if expected_names is not None and not expected_names.issubset({p.name for p in files}):
        raise ValueError(f'{folder.relative_to(ROOT)}: missing required profiles {sorted(expected_names - {p.name for p in files})}')
    profiles, names = [], set()
    for filename in files:
        cfg = json.loads(filename.read_text(encoding='utf-8'))
        label = cfg.get('remarks')
        if not isinstance(label, str) or not label.strip() or label in names:
            raise ValueError(f'{filename.name}: empty or duplicate remarks')
        names.add(label)
        inbounds, outbounds = cfg.get('inbounds', []), cfg.get('outbounds', [])
        if not inbounds or not outbounds:
            raise ValueError(f'{filename.name}: missing inbounds/outbounds')
        outbound_tags = [p.get('tag') for p in outbounds]
        if len(set(outbound_tags)) != len(outbound_tags) or None in outbound_tags:
            raise ValueError(f'{filename.name}: duplicate/missing outbound tag')
        for inbound in inbounds:
            if inbound.get('listen') not in ('127.0.0.1', '::1'):
                raise ValueError(f'{filename.name}: unsafe/broad inbound listen at port {inbound.get("port")}')
        for rule in cfg.get('routing', {}).get('rules', []):
            out_tag = rule.get('outboundTag')
            if out_tag is not None and out_tag not in outbound_tags:
                raise ValueError(f'{filename.name}: routing references missing outbound {out_tag}')
        for dns in cfg.get('dns', {}).get('servers', []):
            if isinstance(dns, dict):
                out_tag = dns.get('proxyOutboundTag')
                if out_tag is not None and out_tag not in outbound_tags:
                    raise ValueError(f'{filename.name}: DNS references missing outbound {out_tag}')
        profiles.append(cfg)
    return profiles


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Check generated outputs are up to date')
    args = parser.parse_args()
    count = 0
    for folder, pattern, output_path, expected_names in GROUPS:
        profiles = load_and_validate(folder, pattern, expected_names)
        count += len(profiles)
        output = json.dumps(profiles, ensure_ascii=False, indent=2) + '\n'
        if args.check:
            if not output_path.exists() or output_path.read_text(encoding='utf-8') != output:
                print(f'FAIL: {output_path.relative_to(ROOT)} missing/out of sync; run python scripts/build.py', file=sys.stderr)
                return 1
            print(f'OK: {len(profiles)} {folder.name} profiles validated; output in sync')
        else:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(output, encoding='utf-8')
            print(f'Built {output_path.relative_to(ROOT)} ({len(profiles)} profiles)')
    print(f'OK: {count} total profiles')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, json.JSONDecodeError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        sys.exit(1)
