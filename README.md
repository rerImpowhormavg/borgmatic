---
title: borgmatic
permalink: index.html
---

## It's your data. Keep it that way.

<img src="docs/static/borgmatic.png" alt="borgmatic logo" width="150px" style="float: right; padding-left: 1em;">

borgmatic is simple, configuration-driven backup software for servers and
workstations. Protect your files with client-side encryption. Backup your
databases too. Monitor it all with integrated third-party services.

Here's an example configuration file:

```yaml
location:
    # List of source directories to backup.
    source_directories:
        - /home
        - /etc

    # Paths of local or remote repositories to backup to.
    repositories:
        - 1234@usw-s001.rsync.net:backups.borg
        - k8pDxu32@k8pDxu32.repo.borgbase.com:repo
        - user1@scp2.cdn.lima-labs.com:repo
        - /var/lib/backups/local.borg

retention:
    # Retention policy for how many backups to keep.
    keep_daily: 7
    keep_weekly: 4
    keep_monthly: 6

consistency:
    # List of checks to run to validate your backups.
    checks:
        - repository
        - archives

hooks:
    # Custom preparation scripts to run.
    before_backup:
        - prepare-for-backup.sh

    # Databases to dump and include in backups.
    postgresql_databases:
        - name: users

    # Third-party services to notify you if backups aren't happening.
    healthchecks: https://hc-ping.com/be067061-cf96-4412-8eae-62b0c50d6a8c
```

Want to see borgmatic in action? Check out the <a
href="https://asciinema.org/a/203761" target="_blank">screencast</a>.

<script src="https://asciinema.org/a/203761.js" id="asciicast-203761" async></script>

borgmatic is powered by [Borg Backup](https://www.borgbackup.org/).

## Integrations

<a href="https://www.postgresql.org/"><img src="docs/static/postgresql.png" alt="PostgreSQL" height="60px" style="margin-bottom:20px;"></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://www.mysql.com/"><img src="docs/static/mysql.png" alt="MySQL" height="60px" style="margin-bottom:20px;"></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://mariadb.com/"><img src="docs/static/mariadb.png" alt="MariaDB" height="60px" style="margin-bottom:20px;"></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://healthchecks.io/"><img src="docs/static/healthchecks.png" alt="Healthchecks" height="60px" style="margin-bottom:20px;"></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://cronitor.io/"><img src="docs/static/cronitor.png" alt="Cronitor" height="60px" style="margin-bottom:20px;"></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://cronhub.io/"><img src="docs/static/cronhub.png" alt="Cronhub" height="60px" style="margin-bottom:20px;"></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://www.pagerduty.com/"><img src="docs/static/pagerduty.png" alt="PagerDuty" height="60px" style="margin-bottom:20px;"></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://www.rsync.net/cgi-bin/borg.cgi?campaign=borg&adgroup=borgmatic"><img src="docs/static/rsyncnet.png" alt="rsync.net" height="60px" style="margin-bottom:20px;"></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://www.borgbase.com/?utm_source=borgmatic"><img src="docs/static/borgbase.png" alt="BorgBase" height="60px" style="margin-bottom:20px;"></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;


## Getting started

Your first step is to [install and configure
borgmatic](https://torsion.org/borgmatic/docs/how-to/set-up-backups/).

For additional documentation, check out the links above for <a
href="https://torsion.org/borgmatic/#documentation">borgmatic how-to and
reference guides</a>.


## Hosting providers

Need somewhere to store your encrypted offsite backups? The following hosting
providers include specific support for Borg/borgmatic. Using these links and
services helps support borgmatic development and hosting. (These are referral
links, but without any tracking scripts or cookies.)

<ul>
 <li class="referral"><a href="https://www.rsync.net/cgi-bin/borg.cgi?campaign=borg&adgroup=borgmatic">rsync.net</a>: Cloud Storage provider with full support for borg and any other SSH/SFTP tool</li>
 <li class="referral"><a href="https://www.borgbase.com/?utm_source=borgmatic">BorgBase</a>: Borg hosting service with support for monitoring, 2FA, and append-only repos</li>
 <li class="referral"><a href="https://storage.lima-labs.com/special-pricing-offer-for-borgmatic-users/">Lima-Labs</a>: Affordable, reliable cloud data storage accessable via SSH/SCP/FTP for Borg backups or any other bulk storage needs</li>
</ul>

## Support and contributing

### Issues

You've got issues? Or an idea for a feature enhancement? We've got an [issue
tracker](https://projects.torsion.org/witten/borgmatic/issues). In order to
create a new issue or comment on an issue, you'll need to [login
first](https://projects.torsion.org/user/login). Note that you can login with
an existing GitHub account if you prefer.

If you'd like to chat with borgmatic developers or users, head on over to the
`#borgmatic` IRC channel on Freenode, either via <a
href="https://webchat.freenode.net/?channels=borgmatic">web chat</a> or a
native <a href="irc://chat.freenode.net:6697">IRC client</a>.

Also see the [security
policy](https://torsion.org/borgmatic/docs/security-policy/) for any security
issues.

Other questions or comments? Contact
[witten@torsion.org](mailto:witten@torsion.org).


### Contributing

borgmatic is hosted at <https://torsion.org/borgmatic> with [source code
available](https://projects.torsion.org/witten/borgmatic), and is also
mirrored on [GitHub](https://github.com/witten/borgmatic) for convenience.

borgmatic is licensed under the GNU General Public License version 3 or any
later version.

If you'd like to contribute to borgmatic development, please feel free to
submit a [Pull Request](https://projects.torsion.org/witten/borgmatic/pulls)
or open an [issue](https://projects.torsion.org/witten/borgmatic/issues) first
to discuss your idea. We also accept Pull Requests on GitHub, if that's more
your thing. In general, contributions are very welcome. We don't bite! 

Also, please check out the [borgmatic development
how-to](https://torsion.org/borgmatic/docs/how-to/develop-on-borgmatic/) for
info on cloning source code, running tests, etc.

<a href="https://build.torsion.org/witten/borgmatic" alt="build status">![Build Status](https://build.torsion.org/api/badges/witten/borgmatic/status.svg?ref=refs/heads/master)</a>

