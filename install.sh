#!/usr/bin/env bash

mkdir -p /etc/sysconfig
if [ ! -f /etc/sysconfig/zfs-key-load ]; then
  cp etc/sysconfig/zfs-key-load /etc/sysconfig
fi

mkdir -p /etc/systemd/system
cp etc/systemd/system/zfs-key-load.service /etc/systemd/system

systemctl daemon-reload
systemctl enable zfs-key-load

mkdir -p /usr/local/bin
cp zfs_key_load.py /usr/local/bin/zfs-key-load
chmod +x /usr/local/bin/zfs-key-load
