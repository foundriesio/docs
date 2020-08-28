Create a Docker-Compose App |:cowboy:|
======================================

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

   When changes are made to containers.git in your Factory sources, a new target is
   built by our CI system. Devices that are registered to your Factory will be
   able to see this target and conditionally update to it, depending on their
   device configuration.

Device Configuration
--------------------

5. Determine the device you want to configure to use ``shellhttpd``::

     fioctl devices list

   your output should look like this::

     NAME  FACTORY  OWNER           TARGET                  STATUS  APPS        UP TO DATE
     ----  -------  -----           ------                  ------  ----        ----------
     gavin stetson  <unconfigured>  raspberrypi3-64-lmp-19  OK      simple-app  true

6. Configure the device to run the ``shellhttpd`` app::
   
     fioctl devices config updates <device> --apps shellhttpd
