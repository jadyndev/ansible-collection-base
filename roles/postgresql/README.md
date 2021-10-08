# `famedly.base.postgresql` ansible role for deploying PostgreSQL inside a docker container
This role supports both PostgreSQL listening on a
- UNIX socket on the host (mountable into other containers)
- a TCP socket on a configurable port on the host
at the same time.

It does not support changing the listening TCP port inside the container to anything other than the standard `5432`.

If both UNIX and TCP sockets are activated, the configuration of global options is done via UNIX socket.

Since the container sets the permissions of the UNIX socket to `0777`, we do not allow `trust` as auth method for local connections in `pg_hba.conf`.

## Requirements
- psycopg2

## Role Variables
See `defaults/main.yml`.

The `postgresql_superuser_password` variable is required and sets the password for the default user `postgres`.

In `postgresql_global_config_options` you can specify global config options in the form of `{ option: "listen_addresses", value: "*" }.

In the optional `postgresql_host_port` variable you can provide an unused port on the host which will be forwarded to the container port 5432.

By default `postgresql_connect_socket` is set to `true`, which will mount `postgresql_socket_path` into the container and thus provide the PostgreSQL UNIX socket on the host.
You can disable this by setting the variable to `false`, PostgreSQL will still listen on the UNIX socket inside the container.

### Alternative docker image
You can specify an alternative container image to use, for example if you want PostGIS support.
If this image is based on the default `docker.io/postgres` image, this role should work as expected.
However, this is not guaranteed.

This is an example for specifying the official PostGIS image:
```yaml
postgresql_version: "13"
postgis_version: "3.1"
postgresql_container_image_name: "docker.io/postgis/postgis"
postgresql_container_image_tag: "{{ postgresql_version }}-{{ postgis_version }}-{{ postgresql_container_distro }}"
```

You could also override the entire `postgresql_container_image` variable.

## Dependencies
Docker needs to be installed and configured.

## Example Playbook
```yaml
---
- name: Install PostgreSQL in a docker container
  hosts: [ all ]
  become: true
  roles:
    - famedly.base.postgresql
  vars:
    postgresql_host_port: "2345"
    postgresql_superuser_password: "{{ vault_postgresql_superuser_password }}"
    postgresql_connect_socket: "false"
```

## License
GNU Affero General Public License v3

## Author Information
Famedly GmbH, famedly.de
