.. _ref-aktualizr-lite:

aktualizr-lite
==============

The default OTA client shipped with the Linux microPlatform is ``aktualizr-lite``. This client is a build variant of the Aktualizr project. It is targeting users who wish to have the security aspects of TUF but do not want the complexity of Uptane.

  .. figure:: /_static/diagrams/aktualizr-lite/aktualizr-lite.png
     :align: center
     :width: 8in

There are two modes ``aktualizr-lite`` supports.

Daemon Mode (Default)
---------------------

This is the default mode of ``aktualizr-lite`` in the Linux microPlatform. It is a systemd service, which is enabled by default on Community Factory images. Additionally, the daemon will only be enabled in a Personal or Enterprise factory after ``lmp-device-register`` has sucessfully registered your device. The daemon will periodically check for new updates, and apply them when found.

To disable daemon mode:

``sudo systemctl disable aktualizr-lite``

To enable daemon mode:

``sudo systemctl enable aktualizr-lite``

To restart the daemon:

``sudo systemctl restart aktualizr-lite``

To stop the daemon:

``sudo systemctl stop aktualizr-lite``

To view the daemon logs:

``sudo journalctl -f -u aktualizr-lite``


Manual Mode
-----------

If you have disabled daemon mode, you can use ``aktualizr-lite`` manually from the command line to fetch updates and apply them. Manual mode can be useful for debugging, testing, or demoing a device.

.. note:: Manual mode will require you to reboot your device to apply an update.

View Current Status
~~~~~~~~~~~~~~~~~~~

You can run ``sudo aktualizr-lite status`` to view the current status of the device.

Fetch and List Updates
~~~~~~~~~~~~~~~~~~~~~~

This command will refresh the targets metadata from the OTA server, and present you with a list of available targets which can be applied.

``sudo aktualizr-lite list``

Apply Latest Update
~~~~~~~~~~~~~~~~~~~

This command will apply the latest available update to the device. This includes both OSTree and Docker app targets.

``sudo aktualizr-lite update``

Apply Specific Update
~~~~~~~~~~~~~~~~~~~~~

If you would like to update to a specifc build number, you can use the following command.

``sudo aktualizr-lite update --update-name <build_number>``

Configuration
-------------

Configuration update methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Editing ``/var/sota/sota.toml`` on a device
* Adding or editing an existing configuration snippet e.g. ``/etc/sota/conf.d/zz-50-fioctl-01.toml`` on a device
* Running *fioctl* from any host ``fioctl devices config <device>``, see :ref:`ref-configuring-devices` for more details


Parameters
~~~~~~~~~~

The following are aktualizr-repo's configuration parameters that can be useful to play with, the presented values are the default one.

.. code-block::

    [uptane]
    # Target/Update check-in interval
    polling_sec = 300

    [pacman]
    # A comma separated list of Compose Apps to update
    compose_apps = ""

    # Compose Apps root directory
    compose_apps_root = "/var/sota/compose-apps"

    # Prune/Delete unused docker containers and images
    docker_prune = "1"

    # A comma separated list of Tags to look for in Targets that should be applied to a given device
    tags = "master"

    [logger]
    # Set log level 0-5 (trace, debug, info, warning, error, fatal)
    loglevel = 2

    [bootloader]
    # A command to invoke after an ostree repo update in order to reboot a system and apply the update
    reboot_command = "/bin/true"
