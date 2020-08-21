---
title: How to inspect your backups
eleventyNavigation:
  key: Inspect your backups
  parent: How-to guides
  order: 4
---
## Backup progress

By default, borgmatic runs proceed silently except in the case of errors. But
if you'd like to to get additional information about the progress of the
backup as it proceeds, use the verbosity option:

```bash
borgmatic --verbosity 1
```

This lists the files that borgmatic is archiving, which are those that are new
or changed since the last backup.

Or, for even more progress and debug spew:

```bash
borgmatic --verbosity 2
```

## Backup summary

If you're less concerned with progress during a backup, and you only want to
see the summary of archive statistics at the end, you can use the stats
option when performing a backup:

```bash
borgmatic --stats
```

## Existing backups

borgmatic provides convenient actions for Borg's
[list](https://borgbackup.readthedocs.io/en/stable/usage/list.html) and
[info](https://borgbackup.readthedocs.io/en/stable/usage/info.html)
functionality:


```bash
borgmatic list
borgmatic info
```

(No borgmatic `list` or `info` actions? Try the old-style `--list` or
`--info`. Or upgrade borgmatic!)


## Logging

By default, borgmatic logs to a local syslog-compatible daemon if one is
present and borgmatic is running in a non-interactive console. Where those
logs show up depends on your particular system. If you're using systemd, try
running `journalctl -xe`. Otherwise, try viewing `/var/log/syslog` or
similiar.

You can customize the log level used for syslog logging with the
`--syslog-verbosity` flag, and this is independent from the console logging
`--verbosity` flag described above. For instance, to get additional
information about the progress of the backup as it proceeds:

```bash
borgmatic --syslog-verbosity 1
```

Or to increase syslog logging to include debug spew:

```bash
borgmatic --syslog-verbosity 2
```

### Rate limiting

If you are using rsyslog or systemd's journal, be aware that by default they
both throttle the rate at which logging occurs. So you may need to change
either [the global rate
limit](https://www.rootusers.com/how-to-change-log-rate-limiting-in-linux/) or
[the per-service rate
limit](https://www.freedesktop.org/software/systemd/man/journald.conf.html#RateLimitIntervalSec=)
if you're finding that borgmatic logs are missing.

Note that the [sample borgmatic systemd service
file](https://torsion.org/borgmatic/docs/how-to/set-up-backups/#systemd)
already has this rate limit disabled for systemd's journal.


### Logging to file

If you don't want to use syslog, and you'd rather borgmatic log to a plain
file, use the `--log-file` flag:

```bash
borgmatic --log-file /path/to/file.log
```

Note that if you use the `--log-file` flag, you are responsible for rotating
the log file so it doesn't grow too large, for example with
[logrotate](https://wiki.archlinux.org/index.php/Logrotate). Also, there is a
`--log-file-verbosity` flag to customize the log file's log level.
