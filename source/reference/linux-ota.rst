.. highlight:: sh

.. _ref-linux-ota:

Linux microPlatform Over-the-Air Updates
========================================

What is an Over-the-Air Update System?
--------------------------------------

Over-the-air (OTA) update systems provide a secure means of updating a device
remotely. The Linux microPlatform has choosen to support a framework based on
on the TUF_/Uptane_ specifications. This is implemented by using root
file systems managed with OSTree_ and the Aktualizr_ open source project.

This page describes OTA updates using the following framework
implementations:

- The Linux microPlatform subscriber demo server
- ATS Garage's system

Gotchas
-------

Both the subscriber demo server (which is based on OTA Community
Edition) and ATS Garage have a few caveats you should be aware of:

 * After the initial registration, the device's image "name" will appear to be
   unknown. Looking closely, you'll see its hash matches that of a known image.
   This is a known peculiarity and the image name will be correct after the
   first update is applied.

 * "Updating" a device only installs the image. It **does not** make that image
   active. A reboot is required for the image to become active, and that policy
   is up to the user to define.

 * If you enable auto-updates and aren't on the latest image, nothing
   will happen until a **new** image is released. Any updates before
   that time must be performed manually.

Updating Your Linux microPlatform Device
----------------------------------------

Choose a method:

.. content-tabs::

   .. tab-container:: lmp-server
      :title: Foundries.io Subscriber Demo Server

      Linux microPlatform subscribers have the easiest path to
      experimenting with OTAs. Subscribers have access to a `device
      management interface`_ for up to 5 devices. The Linux
      microPlatform image includes a program to register the device
      with the foundries.io OTA community edition
      server. Registering the device is as simple as::

          sudo lmp-device-register -n <name of your device as it should appear in UI>
          # Follow the instructions which appear in the terminal.

          # systemd will eventually restart aktualizr and the device will register.
          # To make it happen immediately run:
          sudo systemctl restart aktualizr

      Once registered, the device will show up under
      https://app.foundries.io/devices/ and you'll have the ability to
      start managing updates from there.

   .. tab-container:: ats-garage
      :title: ATS Garage

      All users are also free to use `ATS Garage`_ to manage their
      devices. Documentation can be found at
      https://docs.atsgarage.com/usage/devices.html. Once you have an
      account with ATS Garage you can follow these steps to get your device
      registered:

      **1. Upload Image to ATS Garage**

      This section contains an example for publishing a Raspberry Pi 3 image to
      ATS Garage. You can change the downloaded artifacts and ``ota-publish``
      arguments for other boards.

      First, create a directory to save the files to::

        mkdir lmp-bin && cd lmp-bin

      Next, download your ATS Garage credentials file to the newly created
      ``lmp-bin`` directory:

        https://app.atsgarage.com/#/profile/access-keys

      Then download and extract the following OSTree repository
      tarball to the ``lmp-bin`` directory:

      .. lmp-rpi3-ostree::

      Extract and upload the image using update |version| of the
      ``aktualizr`` container:

      .. parsed-literal::

         tar -jxvf raspberrypi3-64-ostree_repo.tar.bz2

         docker run --rm -it -v $PWD:/build --workdir=/build \\
                hub.foundries.io/aktualizr:|docker_tag| \\
                ota-publish -m raspberrypi3-64 -c credentials.zip \\
                            -r ostree_repo

      .. note::

         The first image published pushes every file in the system. Any
         following publish steps only push files which have changed.

      .. note::

         You can configure app.foundries.io to publish updates to your ATS
         Garage account automatically at https://app.foundries.io/settings/ota.

      **2. Verify Upload**

      Visit https://app.atsgarage.com/#/packages/ and verify the package is
      available.

      **3. Register Device**

      You'll now need to copy your ATS credentials to the device and
      register it. For example, if SSHing into a Raspberry Pi 3::

        # From host computer with credentials.zip:
        scp credentials.zip osf@raspberrypi3-64.local:~/

        # From target device:
        sudo mv credentials.zip /var/sota/sota_provisioning_credentials.zip
        sudo cp /usr/lib/sota/sota_autoprov.toml /var/sota/sota.toml

      Aktualizr will start automatically once it finds
      :file:`/var/sota/sota.toml`; you can also restart it with ``systemctl
      restart aktualizr`` if you are impatient.

Debugging OTA Issues
--------------------

The aktualizr logs are the best place to look for when trying to debug an
issue. The logs are managed via systemd, so they can be tailed with::

  sudo journalctl -f -u aktualizr

The default logging level used by aktualizr is "2". This can be lowered to
increase its verbosity by creating a file like::

  # /etc/sota/sota.env
  AKTUALIZR_CMDLINE_PARAMETERS=--config /var/sota/sota.toml --loglevel 1

Changes to this file won't be picked up by Aktualizr until it's restarted.

Another place to look for information is from the ``ostree`` program that's
installed on the device. You can find out which image is active and which
image will become active by running::

  $ ostree admin status
  lmp a624daeebc085381493ba9745a983e9c1f792751f99d75fd026fbc6eedcdc8c5.1 (pending)
    origin refspec: a624daeebc085381493ba9745a983e9c1f792751f99d75fd026fbc6eedcdc8c5
  * lmp 493b9c454b732ee221a015c6f4ce6bb5c3c5d767111bae94cc3b93aa9c89b64e.0
    origin refspec: 493b9c454b732ee221a015c6f4ce6bb5c3c5d767111bae94cc3b93aa9c89b64e

The output means that the *active* image on the device is ``493b...``,
and the ``a624...`` image is *pending*. That is, an update has been
successfully downloaded and applied to OSTree, but the device has not
yet been rebooted so that the image can become active.

Automatic Rebooting After Updates
---------------------------------

Aktualizr creates an empty file ``/var/run/aktualizr-session/need_reboot`` after
completing an OSTree update, and a `systemd timer`_ can be defined for the systemd
service file ``ostree-pending-reboot`` to automatically restart the device once
there is a pending update.

To create a systemd timer that activates the ``ostree-pending-reboot``
service every day at 5:00 AM UTC, create a file named
:file:`/etc/systemd/system/ostree-pending-reboot.timer` with the following
contents:

.. code-block:: ini

   [Unit]
   Description=Automatic OSTree Update Reboot Scheduling

   [Timer]
   OnCalendar=*-*-* 05:00:00

   [Install]
   WantedBy=multi-user.target

Then enable and start the timer by running:

.. code-block:: console

   sudo systemctl enable ostree-pending-reboot.timer
   sudo systemctl start ostree-pending-reboot.timer

.. _TUF: https://theupdateframework.github.io/
.. _Uptane: https://uptane.github.io/
.. _OSTree: https://ostree.readthedocs.io/en/latest/
.. _Aktualizr: https://github.com/advancedtelematic/aktualizr/
.. _OTA Community Edition: https://github.com/advancedtelematic/ota-community-edition
.. _device management interface: https://app.foundries.io/devices/
.. _ATS Garage: https://app.atsgarage.com
.. _supported offering: https://atsgarage.com/en/pricing.html
.. _systemd timer: https://www.freedesktop.org/software/systemd/man/systemd.timer.html
