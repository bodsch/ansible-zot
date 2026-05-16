
# Ansible Role:  `bodsch.zot`

Installs and configure a [zot](https://github.com/project-zot/zot) server on varoius linux systems.


[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-zot/main.yml?logo=github&branch=main)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-zot?logo=github)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-zot?logo=github)][releases]
[![Ansible Downloads](https://img.shields.io/ansible/role/d/bodsch/zot?logo=ansible)][galaxy]

[ci]: https://github.com/bodsch/ansible-zot/actions
[issues]: https://github.com/bodsch/ansible-zot/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-zot/releases
[galaxy]: https://galaxy.ansible.com/ui/standalone/roles/bodsch/zot/

If `latest` is set for `zot_version`, the role tries to install the latest release version.
**Please use this with caution, as incompatibilities between releases may occur!**

The binaries are installed below `/usr/local/opt/zot/${zot_version}` and later linked to `/usr/bin`.
This should make it possible to downgrade relatively safely.

The zot archive is stored on the Ansible controller, unpacked and then the binaries are copied to the target system.
The cache directory can be defined via the environment variable `CUSTOM_LOCAL_TMP_DIRECTORY`.
By default it is `${HOME}/.cache/ansible/zot`.
If this type of installation is not desired, the download can take place directly on the target system.
However, this must be explicitly activated by setting `zot_direct_download` to `true`.


## Requirements & Dependencies

Ansible Collections

- [bodsch.core](https://github.com/bodsch/ansible-collection-core)
- [bodsch.scm](https://github.com/bodsch/ansible-collection-scm)

```bash
ansible-galaxy collection install bodsch.core
ansible-galaxy collection install bodsch.scm
```
or
```bash
ansible-galaxy collection install --requirements-file collections.yml
```

### Operating systems

Tested on

* Arch Linux
* Debian based
    - Debian 12 / 13
    - Ubuntu 22.04 / 24.04

> **RedHat-based systems are no longer officially supported! May work, but does not have to.**


## usage

**Currently, only `local` storage is supported.**


```yaml
zot_version: '2.1.16'

zot_system_user: root
zot_system_group: zot
zot_config_dir: /etc/zot

zot_direct_download: false

zot_systemd:
  unit:
    after:
      - syslog.target
      - network.target
    wants: []
    requires: []
  service:
    limits:
      nofile:
        soft: ""
        hard: ""

# ---------------------------------------------------------------------------
# zot registry configuration
# All parameters below are rendered into /etc/zot/config.json
# See: https://github.com/project-zot/zot/blob/main/examples/README.md
# ---------------------------------------------------------------------------

zot_config:
  # Distribution spec version
  distSpecVersion: "1.1.1"

  # --- Storage ---------------------------------------------------------------
  storage:
    rootDirectory: /var/lib/zot
    # dedupe: true
    # gc: true
    # gcDelay: "2h"
    # gcInterval: "1h"
    # maxRepos: 0
    # remoteCache: false
    #
    # cacheDriver:
    #   # boltdb (default, local) | dynamodb | redis
    #   name: boltdb
    #   ## DynamoDB options:
    #   # endpoint: "http://localhost:4566"
    #   # region: "us-east-2"
    #   # cacheTablename: "ZotBlobTable"
    #   # userDataTablename: "ZotUserDataTable"
    #   # apiKeyTablename: "ZotApiKeyDataTable"
    #   # repoMetaTablename: "ZotRepoMetadataTable"
    #   # imageMetaTablename: "ZotImageMetaTable"
    #   # repoBlobsInfoTablename: "ZotRepoBlobsInfoTable"
    #   # versionTablename: "ZotVersion"
    #   ## Redis options:
    #   # url: "redis://localhost:6379"
    #   # keyprefix: "zot"
    #
    # storageDriver:
    #   # S3 backend
    #   name: s3
    #   rootdirectory: /zot
    #   region: us-east-2
    #   bucket: zot-storage
    #   forcepathstyle: true
    #   secure: true
    #   skipverify: false
    #   # accesskey: ""
    #   # secretkey: ""
    #
    # retention:
    #   dryRun: false
    #   delay: "24h"
    #   policies:
    #     - repositories:
    #         - "infra/*"
    #         - "prod/*"
    #       deleteReferrers: false
    #       deleteUntagged: true
    #       keepTags:
    #         - patterns:
    #             - "v2.*"
    #             - ".*-prod"
    #         - patterns:
    #             - "v3.*"
    #           pulledWithin: "168h"
    #     - repositories:
    #         - "**"
    #       deleteReferrers: true
    #       deleteUntagged: true
    #       keepTags:
    #         - mostRecentlyPushedCount: 10
    #           mostRecentlyPulledCount: 10
    #           pulledWithin: "720h"
    #           pushedWithin: "720h"
    #
    # subPaths:
    #   /a:
    #     rootDirectory: /tmp/zot1
    #     dedupe: true
    #     gc: true
    #   /b:
    #     rootDirectory: /tmp/zot2
    #     dedupe: true

  # --- HTTP / Network --------------------------------------------------------
  http:
    address: "0.0.0.0"
    port: "5000"
    # realm: "zot"
    # externalUrl: "https://zot.example.com"
    #
    # tls:
    #   cert: /etc/zot/server.cert
    #   key: /etc/zot/server.key
    #   cacert: /etc/zot/ca.cert     # enables mTLS
    #
    # ratelimit:
    #   rate: 10
    #   methods:
    #     - method: GET
    #       rate: 5
    #
    # auth:
    #   htpasswd:
    #     path: /etc/zot/htpasswd
    #
    #   ldap:
    #     address: "ldap.example.org"
    #     port: 389
    #     startTLS: false
    #     baseDN: "ou=Users,dc=example,dc=org"
    #     userAttribute: "uid"
    #     credentialsFile: "/etc/zot/ldap-credentials.json"
    #     skipVerify: false
    #     subtreeSearch: true
    #
    #   bearer:
    #     realm: "https://auth.myreg.io/auth/token"
    #     service: "myauth"
    #     cert: "/etc/zot/auth.crt"
    #
    #   mtls:
    #     identityAttributes:
    #       - CommonName
    #       - Subject
    #       - Email
    #       - URI
    #       - DNSName
    #     uriSanPattern: "spiffe://example.org/workload/(.*)"
    #     uriSanIndex: 0
    #     dnsSanIndex: 0
    #     emailSanIndex: 0
    #
    #   openid:
    #     callbackAllowOrigins:
    #       - "http://127.0.0.1:3000"
    #     providers:
    #       github:
    #         clientid: ""
    #         clientsecret: ""
    #         scopes:
    #           - "read:org"
    #           - "user"
    #           - "repo"
    #         # authurl: ""       # custom URL (for GHE)
    #         # tokenurl: ""      # custom URL (for GHE)
    #       google:
    #         issuer: "https://accounts.google.com"
    #         clientid: ""
    #         clientsecret: ""
    #         scopes:
    #           - "openid"
    #           - "email"
    #       gitlab:
    #         issuer: "https://gitlab.com"
    #         clientid: ""
    #         clientsecret: ""
    #         scopes:
    #           - "openid"
    #           - "read_api"
    #           - "read_user"
    #           - "profile"
    #           - "email"
    #       oidc:
    #         name: "Corporate SSO"
    #         clientid: "zot-client"
    #         clientsecret: ""
    #         keypath: ""
    #         issuer: "http://127.0.0.1:5556/dex"
    #         scopes:
    #           - "openid"
    #           - "profile"
    #           - "email"
    #           - "groups"
    #         claimMapping:
    #           username: "preferred_username"
    #           groups: "groups"
    #
    #   sessionKeysFile: "/etc/zot/session-keys.json"
    #   sessionDriver:
    #     name: local              # local | redis
    #     # url: "redis://localhost:6379"
    #     # keyprefix: "zotsession"
    #
    #   apikey: true
    #   failDelay: 5
    #
    # accessControl:
    #   groups:
    #     group1:
    #       users:
    #         - jack
    #         - john
    #   repositories:
    #     "**":
    #       policies:
    #         - users:
    #             - charlie
    #           groups:
    #             - group1
    #           actions:
    #             - read
    #             - create
    #             - update
    #           # conditions:
    #           #   - expression: 'req.time < timestamp("2099-12-31T23:59:59Z")'
    #           #     message: "access expires end of 2099"
    #       defaultPolicy:
    #         - read
    #         - create
    #       anonymousPolicy:
    #         - read
    #   adminPolicy:
    #     users:
    #       - admin
    #     actions:
    #       - read
    #       - create
    #       - update
    #       - delete

  # --- Logging ---------------------------------------------------------------
  log:
    level: "info"
    # output: "/var/log/zot/zot.log"
    # audit: "/var/log/zot/zot-audit.log"

  # --- Extensions ------------------------------------------------------------
  # extensions:
  #   metrics:
  #     enable: true
  #     prometheus:
  #       path: /metrics
  #
  #   search:
  #     enable: true
  #     cve:
  #       updateInterval: "24h"
  #       # trivy:
  #       #   dbRepository: "ghcr.io/aquasecurity/trivy-db"
  #       #   javaDBRepository: "ghcr.io/aquasecurity/trivy-java-db"
  #       #   vulnSeveritySources:
  #       #     - auto
  #
  #   ui:
  #     enable: true
  #
  #   scrub:
  #     enable: true
  #     interval: "24h"
  #
  #   lint:
  #     enable: true
  #     mandatoryAnnotations:
  #       - "org.opencontainers.image.authors"
  #       - "org.opencontainers.image.source"
  #
  #   sync:
  #     enable: true
  #     credentialsFile: "/etc/zot/sync-credentials.json"
  #     registries:
  #       - urls:
  #           - "https://registry1:5000"
  #         onDemand: false
  #         pollInterval: "6h"
  #         tlsVerify: true
  #         certDir: "/etc/zot/certs"
  #         maxRetries: 3
  #         retryDelay: "5m"
  #         syncTimeout: "10m"
  #         onlySigned: true
  #         content:
  #           - prefix: "/repo1/repo"
  #             tags:
  #               regex: "4.*"
  #               semver: true
  #               # excludeRegex: ".*-dev$"
  #           - prefix: "/repo2/**"
  #             destination: "/localrepo"
  #             stripPrefix: true
  #       - urls:
  #           - "https://index.docker.io"
  #         onDemand: true
  #         tlsVerify: true
  #         maxRetries: 5
  #         retryDelay: "30s"
  #
  #   events:
  #     enable: true
  #     sinks:
  #       - type: nats
  #         address: "nats://127.0.0.1:4222"
  #         timeout: "10s"
  #         channel: "alerts"
  #
  #   trust:
  #     enable: true
  #     cosign: true
  #     notation: true

  # --- Scheduler -------------------------------------------------------------
  # scheduler:
  #   numWorkers: 3

  # --- Cluster (scale-out) ---------------------------------------------------
  # cluster:
  #   members:
  #     - "zot1:5000"
  #     - "zot2:5000"
  #     - "zot3:5000"
  #   hashKey: "cluster-secret"
  #   tls:
  #     cert: /etc/zot/cluster.cert
  #     key: /etc/zot/cluster.key
  #     cacert: /etc/zot/cluster-ca.cert
```


## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://github.com/bodsch/ansible-zot/tags)!


## Author

- Bodo Schulz

## License

[Apache](LICENSE)

**FREE SOFTWARE, HELL YEAH!**
