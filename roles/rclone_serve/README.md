# `famedly.base.rclone_serve` ansible role deploying rclone in a docker container

This role is intended to have rclone with the `serve` command permanently deployed inside a docker container to
translate from the supported protocols (eg. restic) to the supported backend storages (eg. Scaleway S3).

## Role Variables
For configuration consult the [official documentation](https://rclone.org/commands/rclone_serve/).
This role does not verify your config or flags as there are too many combinations.
Check the container logs for error messages.
By default the server will listen on all container addresses on port 8080.

### Required Variables
- `rclone_serve_protocol` has to be set to one of the supported protocols.
- `rclone_serve_backend_config` is a dict that contains the configuration of the storage backend.
  See the example playbook below

### Optional Variables
Use the `rclone_serve_flags` dict for adding or overriding default command line flags like so:

```yaml
rclone_serve_flags:
  addr: "172.35.1.1:8076"
  htpasswd: "{{ rclone_serve_htpasswd_file }}"
  private-repos:
  append-only:
```

For more variables see default/main.yml file.

## Dependencies
- sivel.toiletwater collection for ini templating
- Docker

## Example Playbook
```yaml
- hosts: ["my_rclone_host"]
  become: true
  roles:
    - role: rclone_serve
  vars:
    rclone_serve_protocol: "restic"
    rclone_serve_backend_path: "my_scw_bucket_name"
    rclone_serve_backend_config:
      type: "s3"
      provider: "Scaleway"
      env_auth: false
      endpoint: "s3.nl-ams.scw.cloud"
      access_key_id: "SCWXXXXXXXXXXXXXX"
      secret_access_key: "1111111-2222-3333-44444-55555555555555"
      region: "nl-ams"
    rclone_serve_flags:
      addr: "172.35.1.1:8076"
      htpasswd: "{{ rclone_serve_htpasswd_file }}"
      private-repos:
      append-only:
```
