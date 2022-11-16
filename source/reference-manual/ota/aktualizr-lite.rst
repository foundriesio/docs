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

Disabling daemon mode is not recommended, but running ``aktualizr-lite`` manually can be useful for debugging, testing, or demoing a device.

.. note:: Manual mode will require you to reboot your device to apply an update.

.. note:: If ``aktualizr-lite`` default daemon mode does not fit your needs, the alternative is to create a :ref:`ug-custom-sota-client`.

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

If you would like to update to a specific build number, you can use the following command.

``sudo aktualizr-lite update --update-name <build_number>``

.. note::

    This can only be performed when the original and update targets are under the same tag. In case the update is tagged differently, it is required to switch tags before running this command.

Configuration
-------------

Configuration update methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Editing ``/var/sota/sota.toml`` on a device
* Adding or editing an existing configuration snippet e.g. ``/etc/sota/conf.d/z-50-fioctl-01.toml`` on a device
* Running *fioctl* from any host ``fioctl devices config <device>``, see :ref:`ref-configuring-devices` for more details

.. _ref-aktualizr-lite-params:

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

    # The param instructs aktualizr-lite to (re-)create App containers of a new Target just before reboot if set to "1" (default).
    # If the param is set to "0" then the App containers are (re-)created just after a successful boot on a new ostree version during aklite startup.
    create_containers_before_reboot = "0"

    # A percentage of an available storage that can be used by Compose Apps.
    # aktualizr-lite checks whether there is enough storage available before performing OTA update of Compose Apps.
    # min(sizeof(AppsV_N+1) - sizeof(AppsV_N), 0)  <  <available_storage> * <storage_watermark>/100
    # By default, if the configuration param is not specified, it is set to "80".
    storage_watermark = "60" (set to "80" if not specified)

    [logger]
    # Set log level 0-5 (trace, debug, info, warning, error, fatal)
    loglevel = 2

    [bootloader]
    # A command to invoke after an ostree repo update in order to reboot a system and apply the update
    reboot_command = "/bin/true"
