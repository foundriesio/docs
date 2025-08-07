.. _ref-targets:

Targets Overview
================

Perhaps the most important goal of a Factory is to deliver immutable software updates to devices.
This is achieved by using the `The Update Framework`_ (TUF).
The central piece to TUF is the notion of a Target.
A Target defines a cryptographically verifiable description of the software a device should run.

For a simplified example:

.. code-block:: yaml

 "raspberrypi4-64-lmp-42" : {
    "hashes" : {"sha256" : "0xdeadbeef"},
    "custom" : {
      "version" : "42"
      "docker_compose_apps" : {
        "shellhttpd" : {
          "uri" : "hub.foundries.io/andy-corp/shellhttpd@sha256:0xdeadbeef"
        }
      },
      "hardwareIds" : ["raspberrypi4-64"],
      "tags" : ["master"],
    }
  }

This Target specifies some important bits of information:

 * This is build ``42``
 * The immutable OSTree hash of the base image is ``0xdeadbeef``
 * The Compose app, ``shellhttpd``, is part of the Target.

The Target is the goal.
Developers push changes to Git so as to build a Target.
Devices look to the OTA system for the latest Target they should run.
Operators oversee the intersection of these goals.

The point of a Factory is to create Targets.
The interesting thing about a Factory, is how with a ``git push``, you can make this all happen.
This is where you can start to visualize a Factory.
The :ref:`Factory Definition <ref-factory-definition>` file instructs CI what to build when changes hit ``source.foundries.io``.

The default ``factory-config.yml`` tells CI:

 * If an LmP change (``lmp-manifest.git`` or ``meta-subscriber-overrides.git``) is made to the default(i.e., "main") branch,
   do a platform build and tag it with "default".

 * If a container change (``containers.git``) is made to the default branch, do a container build and tag it with "default".

However, this can grow much :ref:`more complex <ref-advanced-tagging>`.

CI must also take into account that Targets require both an OSTree image **and** Compose apps.
This turns out to be a fairly simple calculation.
CI looks at the previous Target for a given tag.
In the case of a platform build, it will copy the Compose apps defined for it.
In the case of a container build, it will copy the OSTree hash.
In this way, there are not "container targets" and "platform targets"; there are only Targets.

Visualizing a Factory
---------------------

Start with ``factory-config.yml``.
The ``tagging`` and ``ref_options`` stanzas describe the intent.
Then take a high-level view of the fleet:

.. code-block:: console

  $ fioctl status
  Total number of devices: 2

  TAG     DEVICES  UP TO DATE  ONLINE
  ---     -------  ----------  ------
  master  2        1           1

  ## Tag: master
    TARGET  DEVICES  DETAILS
    ------  -------  -------
    46      1        `fioctl targets show 46`
    112     1        `fioctl targets show 112`

This will show all Targets active in the field.
Now take a look at a specific Target:

.. code-block:: console

 $ fioctl targets show 46
 CI:    https://ci.foundries.io/projects/andy-corp/lmp/builds/46/

 ## Target: intel-corei7-64-lmp-46-master
        Created:       2022-03-22T15:23:03Z
        Tags:          master
        OSTree Hash:   8f8a74e0fac31c1c3f43d737246e7320d453c377c6724c398a506b857d224e55

        Source:
            https://source.foundries.io/factories/andy-corp/lmp-manifest.git/commit/?id=aa36b74580d64f8754d42817e534004c05f80cf7
            https://source.foundries.io/factories/andy-corp/meta-subscriber-overrides.git/commit/?id=d56ae6a677316bf1c8544cf9228632a59fe3d991
            https://source.foundries.io/factories/andy-corp/containers.git/commit/?id=749aac2cc30c572769b702498373505dac1da7ed

        APP          HASH
        ---          ----
        shellhttpd   sha256:e4a7b3a31c0126d28aaf75e1b8b6e83c7afd160b110267530b8572ce192160da

This command gives the exact details of the Target, including the CI change that produced it.

.. _The Update Framework:
   https://theupdateframework.com/
