Clone this repository and run `install.sh`. Edit `/etc/sysconfig/zfs-key-load` and fill in the config values for your [zfs-key-api](https://github.com/0x0a11c0de/zfs-key-api/) instance.

Generate a key for your encrypted dataset:

```
/usr/local/bin/zfs-key-load -k
```

Create an encrypted dataset, and use the key from above:

```
zfs create -o encryption=on -o keylocation=prompt -o keyformat=hex <dataset>
```

[Set up a key vault and add the dataset and key as a secret.](https://docs.microsoft.com/en-us/azure/key-vault/secrets/quick-create-cli) The secret value format should be `dataset:key`.
