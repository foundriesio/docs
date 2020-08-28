Create a Docker-Compose App
===========================

In the :ref:`ref-git-config` section, you should have set up ``git`` with your
auth token, meaning you can clone your Factory repositories from
``https://source.foundries.io/factories/<factory>/`` and begin creating new
targets for your devices to update to.

Default Example
---------------

1. Clone your containers.git repo and enter it::

     git clone https://source.foundries.io/factories/<factory>/containers.git
     cd containers.git

  We initialise your ``containers.git`` repository with a simple compose app
  example in ``shellhttpd.disabled/``

  .. tip:: Directory names ending with ``.disabled`` in containers.git are
     ignored by our CI system.

2. Enable the ``shellhttpd`` example app::

     mv shellhttpd.disabled shellhttpd

3. Add, commit and push::

     git add .
     git commit -m "shellhttpd: enable shellhttpd app"
     git push

4. :ref:`ref-watch-build`

   When changes are made to ``containers.git`` in your Factory sources, a new target is
   built by our CI system. Devices that are registered to your Factory will be
   able to see this target and conditionally update to it, depending on their
   :ref:`device configuration <ref-configuring-devices>`.

Device Configuration
--------------------

Now that a target is being built, we want to tell our device(s) to update to
this new target. This is done using :ref:`ref-fioctl`.

1. Determine the device you want to configure to use ``shellhttpd``::

     fioctl devices list

   your output should look like this::

     NAME  FACTORY  OWNER           TARGET                  STATUS  APPS        UP TO DATE
     ----  -------  -----           ------                  ------  ----        ----------
     gavin stetson  <unconfigured>  raspberrypi3-64-lmp-19  OK      simple-app  true

2. Configure the device to run the ``shellhttpd`` app::

     fioctl devices config updates <device> --apps shellhttpd

About Targets
-------------

You can see the available targets your Factory has produced::

  fioctl targets list

**CLI Output**::

  VERSION  TAGS    APPS        HARDWARE IDs
  -------  ----    ----        ------------
  2        devel               raspberrypi3-64
  3        master              raspberrypi3-64
  4        master  shellhttpd  raspberrypi3-64

details about target can be printed by passing its version number to the
``show`` subcommand::

  fioctl targets show 4

**CLI Output**::

  Tags:   master
  CI:     https://ci.foundries.io/projects/stetson/lmp/builds/4/
  Source:
          https://source.foundries.io/factories/stetson/lmp-manifest.git/commit/?id=2aaebc4b16c1027c9aae167d6178a8f248027a73
          https://source.foundries.io/factories/stetson/meta-subscriber-overrides.git/commit/?id=19cbbe7b890eafed4d88e1fb13d2d61ecef8f3e5
          https://source.foundries.io/factories/stetson/containers.git/commit/?id=6a2ef8d1dbab0db634c52950ae4a7c18494021b2

  TARGET NAME            OSTREE HASH - SHA256
  -----------            --------------------
  raspberrypi3-64-lmp-4  1b0df36794efc32f1c569c8d61f115b04c4d51caa2fa99c17ec85384ae06518d

  DOCKER APP  VERSION
  ----------  -------
  shellhttpd  shellhttpd.dockerapp-4

.. todo::
   This section links to the flash-target section, yet to be submitted, which
   details how to install the LmP on a device, it makes the assumption that the
   device is registered

.. todo::
   reference unreferenced keywords

.. todo::
   add :ref: to
   https://docs.foundries.io/latest/customer-factory/configuring.html in
   'configuration', will have to pull this in from master.

.. todo::
   Give more complex example such as mosquitto, homeassistant, netdata that the
   user has to recreate rather than just enable with an 'mv' command.
