.. _ref-device-tags:

Device Tags
===========

The Foundries.io™ version of aktualizr-lite includes a concept called "device tags".
This helps you maintain better control over your fleet.
Each device can subscribe to a single tag to obtain updates from.
If specified, a device will only apply updates from TUF which includes the tag.

Let us look at an example ``targets.json``::

 {
  ...
  "signed": {
    "targets": {
      "raspberrypi4-64-lmp-143" : {
        "custom" : {
          "createdAt" : "2019-08-12T22:18:16Z",
          "hardwareIds" : ["raspberrypi4-64"],
          "name" : "raspberrypi4-64-lmp",
          "targetFormat" : "OSTREE",
          "updatedAt" : "2019-08-12T22:18:16Z",
          "version" : "143",
          "tags": ["promoted", "postmerge"]
       },
       "hashes" : {
          "sha256" : "20ac4f7cd50cda6bfed0caa1f8231cc9a7e40bec60026c66df5f7e143af96942"
       },
       "length" : 0
      },
      "raspberrypi4-64-lmp-144" : {
        "custom" : {
          "createdAt" : "2019-08-12T22:18:16Z",
          "hardwareIds" : ["raspberrypi4-64"],
          "name" : "raspberrypi4-64-lmp",
          "targetFormat" : "OSTREE",
          "updatedAt" : "2019-08-12T22:18:16Z",
          "version" : "144",
          "tags": ["postmerge"]
       },
       "hashes" : {
          "sha256" : "20ac4f7cd50cda6bfed0caa1f8231cc9a7e40bec60026c66df5f7e143af96942"
       },
       "length" : 0
      }
    }
  }
 }

You may have two devices.
If Device #1 is used for integration testing, it would set the tags in its ``sota.toml`` as::

 [pacman]
 tags = "postmerge"

In this case, the aktualizr-lite daemon would pick the latest "postmerge" build for this device, version **144**.

Device #2 is used in production.
It would set its tag to only run "promoted" builds::

 [pacman]
 tags = "promoted"

In this case, the aktualizr-lite daemon would pick the latest "promoted" build for this device, version **143**.

Managing Tags
-------------

By default, LmP builds are triggered for your Factory after code has been merged to main will be tagged with "postmerge".
After doing QA on this build, it can be "promoted" using the Fioctl_ tool::

 fioctl targets tag -Tpostmerge,promoted raspberrypi4-64-lmp-144

This will kick off a CI job that will tag build 144 as promoted.
This would result in Device 2 (from the above example) in updating.

.. _Fioctl:
   https://github.com/foundriesio/fioctl/releases
