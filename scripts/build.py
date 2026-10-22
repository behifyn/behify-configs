#!/usr/bin/env python3
"""Deterministically build and validate v2rayNG's full-Xray-JSON array subscription."""
import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROFILES = ROOT / "profiles"
OUTPUT = ROOT / "sub" / "v2rayng.json"

def load_and_validate():
    files = sorted(PROFILES.glob('behify-*.json'))
    if not files:
        raise ValueError('No profiles found')
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
            out_tag=rule.get('outboundTag')
            if out_tag is not None and out_tag not in outbound_tags:
                raise ValueError(f'{filename.name}: routing references missing outbound {out_tag}')
        for dns in cfg.get('dns', {}).get('servers', []):
            if isinstance(dns, dict):
                out_tag=dns.get('proxyOutboundTag')
                if out_tag is not None and out_tag not in outbound_tags:
                    raise ValueError(f'{filename.name}: DNS references missing outbound {out_tag}')
        profiles.append(cfg)
    return profiles

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true',help='Check generated output is up to date')
    args=parser.parse_args()
    profiles=load_and_validate()
    output=json.dumps(profiles,ensure_ascii=False,indent=2)+'\n'
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding='utf-8')!=output:
            print('FAIL: sub/v2rayng.json missing or out of sync; run python scripts/build.py', file=sys.stderr)
            return 1
        print(f'OK: {len(profiles)} validated JSON profiles; subscription is in sync')
    else:
        OUTPUT.parent.mkdir(parents=True,exist_ok=True)
        OUTPUT.write_text(output,encoding='utf-8')
        print(f'Built {OUTPUT.relative_to(ROOT)} with {len(profiles)} profiles')
    return 0

if __name__ == '__main__':
    sys.exit(main())
