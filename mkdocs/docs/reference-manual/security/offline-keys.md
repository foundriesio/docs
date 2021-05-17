# Offline FoundriesFactory TUF Keys

FoundriesFactory uses TUF's multi-level key management strategy to
secure software updates. Part of this strategy utilizes roles to
separate software update responsibilities. By restricting each role's
responsibilities or actions it's trusted to perform, the impact of a
compromised role's key is minimized.

Even so, if a key were compromised, TUF provides a mechanism for
reliably revoking keys: the root role. The root role exists to delegate
trust to all other top-level roles used in the system. TUF allows
rotation of the root key in case it gets compromised. Since key rotation
is crucial to Factory security, it's important that the root key be
highly secure as well.

To increase a root key's security further, it is encouraged that the
Factory owner rotates it. Rotation will convert the root role's
online-key, generated during the bootstrap of a Factory, to an offline
key.

## Rotation

Key rotation updates the keys that a FoundriesFactory fleet will trust.
Every new Factory should have its keys rotated for offline storage. Key
rotation is also necessary in the event of a key compromise.
[fioctl](https://github.com/foundriesio/fioctl) includes commands for
managing TUF keys.

When a Factory is created, Foundries.io sends a notification with a link
to its TUF keys like:

    Your FoundriesFactory has been created and is ready for use.

    ...

    TUF key management requires that you keep a securely stored offline copy of
    your root credentials. In the event of an online key compromise, these offline
    keys will be used to securely rotate/replace the compromised key(s). You can
    download your keys *one time* from this URL:

       https://factory-keys.foundries.io/example/example.tgz

    Once downloaded, this file will be deleted from our system.

### Establishing a root key

The TUF root key is the most important key in TUF. The owner of this key
can sign the TUF `root.json` that defines what keys and roles devices
can trust. A new root key can be defined by doing a "key rotation". A
key rotation sets the new root key for the factory, but it also signs
the new root.json with the previous root key to demonstrate proper
ownership. This can be done in fioctl with:

    fioctl keys rotate-root /absolute/path/to/example.tgz

At this point the only copy of the Factory's root private key is in this
file. This file **cannot be lost** or it will be impossible to make
future key updates to the Factory.

!!! Note

    At this point, the tarball should be backed up as described below.

### Establishing an offline target key

TUF has the notion of a `targets.json` file which specifies what
updates(Targets) are available to a device. This file must be signed
with a target signing key and pushed to Foundries.io. Normal CI builds
sign the targets with a Foundries.io owned target signing key trusted by
the Factory.

In order to ensure customer control of updates, production devices
require their `targets.json` file to be signed by two parties:

- The Foundries.io online target signing key
- The customer's offline target signing key

A Factory can create its target signing key in fioctl with:

    fioctl keys rotate-targets /absolute/path/to/example.tgz

This will send 2 versions of `root.json` to Foundries.io. Both versions
will be identical except the one for production devices will specify a
targets signing threshold of 2 rather than 1.

The Factory's TUF metadata can be viewed with:

    # The normal "CI" root:
    fioctl get https://api.foundries.io/ota/repo/<FACTORY>/api/v1/user_repo/root.json

    # The production root. Note the target key role has:
    #   "threshold" : 2
    fioctl get https://api.foundries.io/ota/repo/<FACTORY>/api/v1/user_repo/root.json?production=1

Given the importance of the offline credentials file, it is recommended
to create a second file that can sign production targets for Waves but
lacks the root keys required to alter Factory root metadata:

    fioctl keys copy-targets /absolute/path/to/example.tgz /path/to/target-only.tgz

### How to backup offline keys

There are 3 recommend types of backups:

- The actual tarball - Basically
  `cp <tarball> <path to backup storage media>`
- A plain text file of the Factory's active root private key
- A print out of the Factory's active root private key

2-3 copies of these backups should be placed in safes in different
geographical locations. Finding the root private key requires
understanding the offline keys file format. The initial copy of the
offline keys will look like:

    # Most of the files aren't critical. They are used in the Factory's initial
    # CI run to setup credentials. They are kept around to help with debug.
    tufrepo
    |-- config.json
    |-- credentials.zip
    |-- keys
    |   |-- offline-root.pub     # Public root shown in root.json
    |   |-- offline-root.sec     # The Factory's first root private
    |   |-- offline-targets.pub  # The Foundries.io public target in root.json.
    |   |-- offline-targets.sec  # The Foundries.io target key used in CI.
    |   |-- root.pub
    |   |-- root.sec
    |   |-- targets.pub
    |   |-- targets.sec
    `-- roles |
        |-- root.json
        |-- targets.json
        |-- targets.json.checksum
        `-- unsigned
            `-- targets.json

The critical file to keep from this tarball is `offline-root.sec`. After
the first root key rotation the offline keys will include 2 new files
similar to:

    tufrepo
    `-- keys
        |-- fioctl-root-5d7397a7a9d62d4f89a39b77903831af12172abb8b9f483e7ad9638bacbc93b1.pub
        `-- fioctl-root-5d7397a7a9d62d4f89a39b77903831af12172abb8b9f483e7ad9638bacbc93b1.sec

The new root private key is named with the pattern
`fioctl-root-<keyid>.sec`. The key ID can be verified with:

    $ fioctl get https://api.foundries.io/ota/repo/<FACTORY>/api/v1/user_repo/root.json \
      | jq '.signed.roles["root"]["keyids"][0]'
    "5d7397a7a9d62d4f89a39b77903831af12172abb8b9f483e7ad9638bacbc93b1"

Every root key rotation will generate a new `.sec` file and **must** be
backed up.

It is recommended to back up the Factory offline target signing key.
However, losing this file isn't catastrophic - it's just inconvenient.
After doing a target key rotation the offline keys file will have two
new files like:

    tufrepo
    `-- keys
        |-- fioctl-targets-cb58f6b83e1e16276c64b19aef7fb07afe3227818f8511ac3ceb288965afdb65.pub
        `-- fioctl-targets-cb58f6b83e1e16276c64b19aef7fb07afe3227818f8511ac3ceb288965afdb65.sec

The new target signing key is named similar to the root key as:
`fioctl-targets-<keyid>.sec`. The key ID can be verified with:

    $ fioctl get https://api.foundries.io/ota/repo/<FACTORY>/api/v1/user_repo/root.json \
      | jq '.signed.roles["targets"]["keyids"][1]'
    "cb58f6b83e1e16276c64b19aef7fb07afe3227818f8511ac3ceb288965afdb65"
