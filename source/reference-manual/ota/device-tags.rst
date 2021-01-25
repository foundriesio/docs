.. _ref-device-tags:

Device Tags
===========

The Foundries.io version of aktualizr-lite includes a concept called "device
tags" to help maintain better control of your fleet. Each device can subscribe
to a list of tags. If specified, a device will only apply updates from TUF that
include a tag from its list.

Lets look at an example targets.json to explain::

 {
  ...
  "signed": {
    "targets": {
      "raspberrypi3-64-lmp-143" : {
        "custom" : {
          "createdAt" : "2019-08-12T22:18:16Z",
          "hardwareIds" : ["raspberrypi3-64"],
          "name" : "raspberrypi3-64-lmp",
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
      "raspberrypi3-64-lmp-144" : {
        "custom" : {
          "createdAt" : "2019-08-12T22:18:16Z",
          "hardwareIds" : ["raspberrypi3-64"],
          "name" : "raspberrypi3-64-lmp",
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

You could have two devices. Device #1 might be used for integration testing. It
would set the tags in its sota.toml as::

 [pacman]
 tags = "postmerge"

In this case, the aktualizr-lite daemon would pick the latest "postmerge" build
for this device, version **144**.

Device #2 might be used in production. It would set its tag to only run
"promoted" builds::

 [pacman]
 tags = "promoted"

In this case, the aktualizr-lite daemon would pick the latest "promoted" build
for this device, version **143**.

Managing Tags
-------------

By default LMP builds triggered in your factory after code has been merged to
master will be tagged with "postmerge". After doing QA on this build, it can
be "promoted" using the fioctl_ tool::

 fioctl targets tag -Tpostmerge,promoted raspberrypi3-64-lmp-144 --factory <factory>

That will kick off a CI job that will tag build 144 as promoted. This would
result in the Device 2 from the example above in updating.

.. _fioctl:
   https://github.com/foundriesio/fioctl/releases
