# `famedly.base.user` ansible role

This ansible role can be used to provision access to a server via SSH by
creating and configuring users and their SSH keys and sudo privileges.

## Role Variables

The role takes a dict of users to provision in the `users` variable in the following structure:

```yaml
users:
  username:
    root: <bool>  # Whether the user should be given root permissions by the role, default false
    active: <bool>  # Whether the user should be created or removed, default false
    gecos: "Full Name"  # not required
    ssh:  # defaults to an empty array
      - "ssh-ed25519 AAAA[...] comment-here"
      - [...]
  anotheruser: [...]
```

For more fine grained control of who has root access where and even which users
are to be deployed where, a structure like this is recommended in the
inventory:

```yaml
# In group_vars/all
users_base:
  username:
    gecos: "Full Name"
    ssh: [...]

users: >
  {{
    users_base
    | combine(users_group_acl, recursive=True)
    | combine(users_host_acl, recursive=True)
  }}

# In group_vars/prod

users_group_acl:
  username:
    active: true
    root: true

# In host_vars/weird-edge-case

users_host_acl:
  username:
    root: false
```

It allows keeping the user information in one central place, and having
overrides for specific groups or hosts.
