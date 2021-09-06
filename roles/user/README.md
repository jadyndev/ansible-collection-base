# `famedly.base.user` ansible role

This ansible role can be used to provision access to a server via SSH by
creating and configuring users and their SSH keys and sudo privileges.

## Role Variables

The role takes a list of users to provision in the `users` variable in the following structure:

```yaml
users:
  - name: username
    root: true|false
    gecos: "Full Name"
    ssh:
      - key: "ssh key"
        active: true|false
      - [...]
  - [...]
```

The  [`gecos` field](https://en.wikipedia.org/wiki/Gecos_field) of a user is optional,
and can be used to provide a full name for a user.
