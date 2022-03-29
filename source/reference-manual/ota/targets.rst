.. _ref-targets:

Targets Overview
================

Perhaps the most important goal of a FoundriesFactory is to deliver
immutable software updates to devices. This is achieved by using the
`The Update Framework`_ (TUF). The central piece to TUF is the notion
of a Target. A Target defines a cryptographically verifiable
description of the software a device should run. A simplified example
could be::

 "raspberrypi3-64-lmp-42" : {
    "hashes" : {"sha256" : "0xdeadbeef"},
    "custom" : {
      "version" : "42"
      "docker_compose_apps" : {
        "shellhttpd" : {
          "uri" : "hub.foundries.io/andy-corp/shellhttpd@sha256:0xdeadbeef"
        }
      },
      "hardwareIds" : ["raspberrypi3-64"],
      "tags" : ["master"],
    }
  }

This Target specifies some important bits of information:

 * This is build ``42``
 * The immutable OSTree hash of the base image is ``0xdeadbeef``
 * The Compose App, ``shellhttpd``, is part of the Target.

The Target is the goal. Developers push changes to Git in hopes of
building a Target. Devices look to the OTA system for the latest
Target they should run. Operators oversee the intersection of these
goals.

The point of the Factory is to create Targets. The magic of the
Factory is how a simple ``git push`` can make this all happen and
is where you can start to visualize a Factory. The
:ref:`Factory Definition <ref-factory-definition>` file instructs
CI what it's supposed to build when changes hit source.foundries.io.
The default factory-definition.yml tell CI:

 * If an LmP change (lmp-manifest.git or meta-subscriber-overrides.git)
   comes in on the master branch, do a platform build and tag it with
   "master".

 * If a container change (containers.git) comes in on master branch,
   do a container build and tag it with master.

However, this can grow much :ref:`more complex <ref-advanced-tagging>`.

CI must also take into account that Targets require both an OSTree
image **and** Compose Apps. This turns out to be a fairly simple
calculation. CI looks at the previous Target for a given tag. In
the case of a platform build, it will copy the Compose Apps defined for it.
In the case of a container build, it will copy the OSTree hash. In
this way, there aren't "container targets" and "platform targets". There
are only Targets.

Visualizing a Factory
---------------------

Start with ``factory-config.yml``. The ``tagging`` and ``ref_options``
stanzas describe the intent. Then take a high-level view of the fleet:

.. code-block:: bash

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

This will show what Targets are active in the field. Then take a look
at a Target:

.. code-block:: bash

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

This command gives the exact details of the Target including the CI
change that produced it.

.. _The Update Framework:
   https://theupdateframework.com/
