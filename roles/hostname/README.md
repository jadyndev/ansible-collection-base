# Hostname management role

This role manages all hostnames of the target server,
both `/etc/hostname` and additional hostnames in
`/etc/hosts`.

## Usage

At the bare minimum, you need to specify `hostname_fqdn`,
this is the primary hostname of the target, which ends up
in `/etc/hostname`.

You can specify additional hostnames for `/etc/hosts` in
`hostname_extra_hosts` in the form of `{ip, fqdn, alias[] }`,
following conventions usual for `/etc/hosts` (single IP,
FQDN first and aliases as plain hostnames).

## Gotchas

This role uses the `hostnamectl` command installed by
default on debian-like distros in order to ensure the
new hostname is immediately set without needing to reboot.

