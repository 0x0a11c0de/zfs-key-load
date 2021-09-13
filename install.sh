#!/usr/bin/env bash

mkdir -p /etc/sysconfig
cp etc/sysconfig/* /etc/sysconfig

mkdir -p /etc/systemd/system
cp etc/systemd/system/* /etc/systemd/system

systemctl daemon-reload
systemctl enable zfs-key-load

mkdir -p /usr/local/bin
cp zfs_key_load.py /usr/local/bin/zfs-key-load
chmod +x /usr/local/bin/zfs-key-load
