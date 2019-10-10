.. highlight:: sh
.. _tutorial-using:

Use Linux microPlatform
=======================

Aktualizr-lite
--------------

Aktualizr-lite is the update agent included with the Linux microPlatform. It
runs as a system daemon periodically looking for new updates to apply to
your device. There are a few interesting things you can do with aktualizr-lite:

Configuration
~~~~~~~~~~~~~
Each device running the Linux microPlatform can be configured with a couple
of important options.  This is defined by creating/updating the device's
``/var/sota/sota.toml`` configuration file.::

 [pacman]
 # tags is a comma separated list of TUF Target tags a device will accept
 # updates for. By default this will be "promoted" which means it only takes
 # Foundries.io official updates. This field could also be changed to do
 # something like promoted and "post-merge" builds (in master but not promoted)
 # tags = "promoted, post-merge"
 #
 # By default a device won't run any Docker Apps. This field allows you to
 # run applications from the FoundriesFactory App Store.
 # docker_apps = "shellhttpd,x-kiosk"

Controlling Incoming Updates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
aktualizr-lite's default functionality is to download new updates, apply
them, and reboot the device as soon as it sees a new update. Its possible
to customize some of this behavior.

The command aktualizr-lite reboots the device with defaults ``/bin/reboot``.
This can be overridden in your sota.toml with::

 [bootloader]
 reboot_command = "/my-custom-command"

This reboot command could do things like checking for outstanding work in your
system before doing the reboot, etc.

By default the aktualizr-lite daemon will check for updates every 5 minutes.
This value can be updated in sota.toml with::

 [uptane]
 # check once an hour
 polling_sec = 600

Before applying an update, aktualizr-lite will attempt to acquire a lock on
``/run/lock/aktualizr-lite-update`` using flock_. You can have custom code
in your application(s) that acquire and release this lock to help control
when updates are applied.

.. _flock:
   https://linux.die.net/man/2/flock

Other advanced topics
---------------------

 * :ref:`ref-device-tags`
 * :ref:`ref-docker-apps`
