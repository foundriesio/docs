.. _gs-create-a-docker-compose-app:

Create a Docker-Compose App
===========================

In the :ref:`gs-git-config` section, you should have set up ``git`` with your
auth token, meaning you can clone your Factory repositories from
``https://source.foundries.io/factories/<factory>/`` and begin creating new
Targets for your devices to update to.

.. tip:: To help illustrate the update process, you can compare the output of
   some commands like ``fioctl devices list`` (on host machine) and ``docker ps``
   (on device) running before and after enabling an example app or demo. You can
   also check the :guilabel:`Devices` tab at https://app.foundries.io for the
   current target your device is running.

.. _gs-example-apps:

Example Apps
------------

.. tabs::

   .. tab:: Default Example (shellhttpd)

      This default example shows how apps are enabled. You should read the contents of
      the ``shellhttpd`` folder to see how this application has been defined, or read
      the other examples to learn how you can define an app from scratch.
      
      #. Clone your containers.git repo and enter it::
      
           git clone https://source.foundries.io/factories/<factory>/containers.git
           cd containers.git
      
         We initialise your ``containers.git`` repository with a simple compose app
         example in ``shellhttpd.disabled/``
      
         .. tip:: Directory names ending with ``.disabled`` in containers.git are
            ignored by our CI system.
      
      #. Enable the ``shellhttpd`` example app::
      
           mv shellhttpd.disabled shellhttpd
      
      #. Add, commit and push::
      
           git add .
           git commit -m "shellhttpd: enable shellhttpd app"
           git push
      
      #. :ref:`gs-watch-build`
      
         When changes are made to ``containers.git`` in your Factory sources, a new Target is
         built by our CI system. Devices that are registered to your Factory will be
         able to see this Target and conditionally update to it, depending on their
         :ref:`device configuration <ref-configuring-devices>`.
      
      **Device Configuration** 

      Once the Target is built successfully, any devices that are registered to
      the Factory will begin updating to this new Target. The app ``shellhttpd``
      that has been defined will be available for usage in this Target. This can
      be verified by running::

        fioctl targets list

      **By default** devices will run **all** applications that are defined in
      the :term:`containers.git` repository and therefore available in the
      latest Target. This behavior can be changed by enabling only specific
      applications. Read :ref:`ug-fioctl-enable-apps` to learn how.

   .. tab:: mosquitto

      This example describes how to create a docker-compose app for the
      `Mosquitto MQTT Broker <https://mosquitto.org/>`_ from scratch.
      
      #. Clone your containers.git repo and enter it. Make sure to replace
         ``<factory>`` in the example with the name of your Factory::
      
           git clone https://source.foundries.io/factories/<factory>/containers.git
           cd containers.git
      
      #. Create a directory named ``mosquitto`` and ``cd`` into it. This folder
         name defines the name of the
         container image that will be pulled on your device from
         ``hub.foundries.io``::
      
           mkdir mosquitto
           cd mosquitto

      #. Create a file named ``Dockerfile`` to describe your
         container, with the following contents::

           FROM eclipse-mosquitto:latest

      #. Create a file named ``docker-compose.yml`` to describe how you want
         this container to run, with the following contents. Make sure to
         replace ``<factory>`` in the example below with the name of your Factory::

           version: "3.2"

           services:
             mosquitto:
               restart: always
               image: hub.foundries.io/<factory>/mosquitto:latest
               ports:
                 - "1883:1883"
 
      #. Add, commit and push::
      
           git add .
           git commit -m "mosquitto: create mosquitto container"
           git push
      
      #. :ref:`gs-watch-build`
      
         When changes are made to ``containers.git`` in your Factory sources, a new Target is
         built by our CI system. Devices that are registered to your Factory will be
         able to see this Target and conditionally update to it, depending on their
         :ref:`device configuration <ref-configuring-devices>`.
      
      **Device Configuration** 

      Once the Target is built successfully, any devices that are registered to
      the Factory will begin updating to this new Target. The app ``mosquitto``
      that has been defined will be available for usage in this Target. This can
      be verified by running::

        fioctl targets list

      **By default** devices will run **all** applications that are defined in
      the :term:`containers.git` repository and therefore available in the
      latest Target. This behavior can be changed by enabling only specific
      applications. Read :ref:`ug-fioctl-enable-apps` to learn how.

.. _gs-about-targets:

About Targets
-------------

You can see the available Targets your Factory has produced::

  fioctl targets list

**CLI Output**::

  VERSION  TAGS    APPS        HARDWARE IDs
  -------  ----    ----        ------------
  2        devel               raspberrypi3-64
  3        master              raspberrypi3-64
  4        master  shellhttpd  raspberrypi3-64

details about Target can be printed by passing its version number to the
``show`` subcommand::

  fioctl targets show 4

**CLI Output**::

  Tags:   master
  CI:     https://ci.foundries.io/projects/gavin/lmp/builds/4/
  Source:
          https://source.foundries.io/factories/gavin/lmp-manifest.git/commit/?id=2aaebc4b16c1027c9aae167d6178a8f248027a73
          https://source.foundries.io/factories/gavin/meta-subscriber-overrides.git/commit/?id=19cbbe7b890eafed4d88e1fb13d2d61ecef8f3e5
          https://source.foundries.io/factories/gavin/containers.git/commit/?id=6a2ef8d1dbab0db634c52950ae4a7c18494021b2

  TARGET NAME            OSTREE HASH - SHA256
  -----------            --------------------
  raspberrypi3-64-lmp-4  1b0df36794efc32f1c569c8d61f115b04c4d51caa2fa99c17ec85384ae06518d

  DOCKER APP  VERSION
  ----------  -------
  shellhttpd  shellhttpd.dockerapp-4

.. _gs-completion:

Completion
----------

Now that you're done, you might want to read :ref:`sec-tutorials` to see some
examples of the things that can be done with your Factory. Additionally, you can
read the :ref:`sec-manual` to learn more about the architecture of
FoundriesFactory and the Linux microPlatform.

.. todo::
   reference unreferenced keywords

.. todo::
   Give more complex example such as mosquitto, homeassistant, netdata that the
   user has to recreate rather than just enable with an 'mv' command.
