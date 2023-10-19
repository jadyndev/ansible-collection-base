# `famedly.base.restic` ansible role

Ansible role to download restic and install a systemd
service and timer to automatically create backups on
a schedule.

## Setting up backups

Set the restic (remote) repository by populating `restic_repository`
in the same form as the restic command line argument (f.ex.:
`s3:https://s3.server.tld/my-bucket/my-specific-restic-repo`).

Set the `restic_password` variable to the password the backup should
be encrypted with.

If your restic remote needs additional environment variables (like
`AWS_ACCESS_KEY_ID` etc for s3), set those as `{ENV_VAR_NAME: value}`
in `restic_environment`.

To control what and how data is backed up, see:

- `restic_backup_paths`: takes an array of paths that should
  be backed up.
- `restic_backup_commands`: takes an array of dictionaries of
  the form `{command, filename}`, where the output of `command`
  is fed into `restic backup --stdin --stdin-filename {{ filename }}`.

To control when backups are run, see `restic_systemd_timer_on_calendar`
and `restic_systemd_timer_accuray_sec`.

## Installing restic

The role will attempt to install restic from the github release by default,
afterwards restic will be available in `/usr/local/bin/restic`.

If restic is already installed or will be installed by another service,
`restic_install_binary: false` can be set. If the restic binary is not
located in `/usr/local/bin/restic`, set the full path in `restic_binary`.
