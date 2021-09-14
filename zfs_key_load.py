#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import argparse
import secrets
import requests
import pexpect
import sys
import subprocess
from urllib.parse import urljoin


def _get_datasets(base_uri, token):
    try:
        resp = requests.get(urljoin(base_uri, '/datasets'), headers={'Authorization': f'Bearer {token}'})
        if resp.status_code != 200:
            print(f"ERROR: {resp.json()['detail']}", file=sys.stderr)
            raise SystemExit(1)
        return resp.json()
    except Exception as exc:
        print(f'ERROR: {str(exc)}', file=sys.stderr)
        raise SystemExit(1)


def _zfs_load_key(dataset, key):
    try:
        child = pexpect.spawn('zfs', ['load-key', dataset])
        child.expect(':', timeout=10)
        child.sendline(key)
        child.wait()
        child.close()
        if child.exitstatus != 0:
            print(
                f'Error: load-key for dataset "{dataset}" failed with exit status {child.exitstatus}',
                file=sys.stderr
            )
            raise SystemExit(2)
        else:
            print(f'Loaded key for dataset "{dataset}"')
    except Exception as exc:
        print(
            f'Error: load-key for dataset "{dataset}" failed: {str(exc)}',
            file=sys.stderr
        )
        raise SystemExit(3)


def _zfs_mount(dataset):
    proc = subprocess.run(['zfs', 'mount', dataset])
    if proc.returncode:
        print(
            f'Error: mount for dataset "{dataset}" failed with exit status {proc.returncode}',
            file=sys.stderr
        )
        raise SystemExit(4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ZFS integration with Azure Key Vault')
    parser.add_argument('-u', '--zfs-key-api-uri', default=os.environ.get('ZFS_KEY_API_URI'),
                        help='URI to the ZFS Key API')
    parser.add_argument('-t', '--zfs-key-api-token', default=os.environ.get('ZFS_KEY_API_TOKEN'),
                        help='Token to the ZFS Key API')
    parser.add_argument('-k', '--key', action='store_true',
                        help='Generate a cryptographically secure random key in hex and exit')
    args = parser.parse_args()
    if args.key:
        print(secrets.token_hex(32))
        raise SystemExit(0)

    datasets = _get_datasets(args.zfs_key_api_uri, args.zfs_key_api_token)
    for dataset in datasets:
        _zfs_load_key(dataset['dataset'], dataset['key'])
        _zfs_mount(dataset['dataset'])

    raise SystemExit(0)
