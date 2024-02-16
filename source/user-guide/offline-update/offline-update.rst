.. _ug-offline-update:

Offline Updates
===============

This section guides you through the steps of updating a device offline.

.. tip::
   Make sure to check the :ref:`Offline Update Considerations`.

Prerequisites
-------------

1. Enable Offline Update support, i.e. add ``aklite-offline`` to ``PACKAGECONFIG`` of ``aktualizr``. For example:

    .. prompt:: bash

        cat meta-subscriber-overrides.git/recipes-sota/aktualizr/aktualizr_%.bbappend
        PACKAGECONFIG:append = " aklite-offline"
2. Enable :ref:`ug-container-preloading` if you would like to update ``Compose Apps`` along with rootfs (aka ostree).

3. Ensure that :ref:`The Update Framework (TUF) keys are taken offline <ref-offline-keys>`.

4. Build an LmP image and flash it onto a target device or update the device with the image via OTA.

Obtaining Offline Update Content
--------------------------------

First download the offline update content from your Factory to an install medium which can be attached to the target device.
The offline update content, further referred to as "bundle", consists of:

1. `TUF metadata`_;
2. `OSTree`_ repo containing a device's rootfs;
3. :ref:`Compose Apps <ref-compose-apps>`.

Use the command ``fioctl targets offline-update <target-name> <dst> <--tag <tag> [--prod] | --wave <wave-name>> [--expires-in-days <days>]`` to download the bundle.

* ``<target-name>`` - denotes the Target to update a device to
* ``<dst>`` - defines a path to download the update content to
* ``<tag>`` - specifies the Target tag and the tag that the device is on
* ``--prod`` - indicates that this is an update for a production device and ``<target-name>`` refers to *Production Target* (see the note below)
* ``--wave`` - indicates that this is an update for a production device and ``<target-name>`` refers to *Wave Target* (see the note below)
* ``<days>`` - Offline artifact validity period in days

.. note::
    Use ``fioctl waves init`` command to generate :ref:`Wave Target <ref-rm-wave>`.

    Use ``fioctl waves complete`` command to turn *Wave Target* into :ref:`Production Target <ref-production-targets>`.

    Ensure that the target device is a *Production* device, see :ref:`Manufacturing Process for Device Registration <ref-factory-registration-ref>` for more details.

.. note::
    In order to download all artifacts, ``fioctl`` requires token with scopes: ``targets:read``, ``ci:read``.

Performing the Offline Update
-----------------------------

Before doing the offline update, ensure the bundle is accessible on a device, e.g., attach and mount the USB drive.

Use the ``aklite-offline`` CLI utility to perform an offline update.

1. Run ``aklite-offline install [--config <config dir or file>] --src-dir <path to a bundle>``.

2. Run one of :ref:`the post installation actions <Post Install and Run Actions>` depending on the ``aklite-offline install`` result:

    a. code 100: reboot device and invoke ``aklite-offline run [--config <config dir or file>]`` to finalize an ostree installation and start Apps if both ostree/rootfs and Apps are updated;
    b. code 10: invoke ``aklite-offline run [--config <config dir or file>]`` to start updated Apps.
    c. code 90: reboot device to finalize the previous boot firmware update and go to the step #1 to start the update.

3. Reboot a device after running ``aklite-offline run [--config <config dir or file>]`` command if:

    a. code 100: Apps failed to start after update, you must reboot a device to complete the rollback;
    b. code 5: the update includes a boot firmware, you can optionally reboot a device to finalize the boot firmware upgrade.

Usage Details
-------------
The CLI utility supports two commands:

1. ``aklite-offline install [--config <config file/dir>] --src-dir <update-content-dir>``
2. ``aklite-offline run [--config <config file/dir>]``

.. prompt:: text

    ``--config`` -  Path to a directory that contains one of more ``*.toml`` configuration snippets or a path to a ``*.toml`` file. It may be omitted at all so the command collects config from the snippets found in the default directories/files, as ``aktualizr-lite`` does:

    /usr/lib/sota/conf.d
    /var/sota/sota.toml
    /etc/sota/conf.d/

    ``--src-dir`` - Path to a directory that contains the bundle downloaded by ``fioctl targets offline-update`` command.


.. _Post Install and Run Actions:

Post Install and Run Actions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``install`` and ``run`` commands sets exit codes (``echo $?``) to instruct which of the post install actions you should perform.

The ``install`` command sets the following exit codes:

- *0*: Installation was not performed.
    - Device already runs the specified target, no update is needed.
- *4*: Installation was not performed.
    - Failed to pull the provided TUF metadata to the device TUF repo or the provided TUF metadata are invalid.
- *6*: Installation was not performed.
    - Failed to find Targets in the device TUF repo that matches a device tag and/or hardware ID.
- *8*: Installation was not performed.
    - Failed to find the ostree commit and/or all Apps of the Target to be installed in the provided source bundle.
- *10*: Installation succeeded.
    -  ``aklite-offline run`` must be invoked to start the updated Apps.
- *30*: Installation was not performed.
    - Could not start a new update because there is an ongoing installation that requires finalization.
- *50*: Installation was not performed.
    - Failed to pull Target content.
- *70*: Installation was not performed.
    - The pulled Target content is invalid, specifically App compose file is invalid.
- *90*: Installation was not performed.
    - Reboot is required to complete the previous boot firmware update. After reboot a client should repeat the update attempt from the beginning.
- *100*: Installation succeeded.
    - Reboot is required to complete installation. After reboot ``aklite-offline run`` must be invoked.
- *101*: Installation succeeded.
    - Restart of dockerd service is required to complete installation, e.g. ``systemctl restart docker``. After the restart ``aklite-offline run`` must be invoked.

The ``run`` command sets the following exit codes:

- *0*: Update succeeded.
    - Device is booted on the updated rootfs and running the updated Apps.
- *5*: Update succeeded.
    - The boot firmware was updated too. Optionally, a reboot to confirm its update can be performed.
- *40*: The ``run`` command was not executed
    - Could not start the command because there is no pending installation. Make sure you ran the ``install`` command before.
- *90*: Update succeeded.
    - Device is booted on the updated rootfs and running the updated Apps.
    - Bootloader is updated too, optionally, a reboot to confirm its update can be performed.
- *99*: Update failed.
    - Device failed to boot on the updated rootfs and rolled back to the previous version.
- *100*: Update failed.
    - Device successfully booted on the updated rootfs but failed to start the updated Apps after the reboot.
    - Device is rolling back to the previous version, reboot followed by ``aklite-offline run`` is required to complete the rollback.
- *110*: Update failed.
    - Device failed to boot on the updated rootfs and rolled back to the previous version.
    - Device failed to start the previous version's Apps since they are unknown.
- *120*: Update and rollback failed.
    - Device successfully booted on the updated rootfs but failed to start the updated Apps after the reboot.
    - Device cannot perform rollback because the Target/version to rollback to is unknown.

Configuration Details
~~~~~~~~~~~~~~~~~~~~~

The minimum required configuration is:

.. prompt:: text

    [provision]
    primary_ecu_hardware_id = <>

The command can digest the default device config consisting of:

1. ``*toml`` files added into LmP during bitbaking (usually just ``/usr/lib/sota/conf.d/40-hardware-id.toml``);
2. ``sota.toml`` generated by ``lmp-device-register``.

If a device needs to support offline **and** online updating, then the configuration needs to be shared with ``aktualizr-lite``.

Normally, each LmP image includes a configuration file ``/usr/lib/sota/conf.d/40-hardware-id.toml`` which defines a hardware ID.
Therefore, by default, an LmP image includes the minimum required configuration, hence NO device registration is required for ``aklite-offline`` to work.

If you register a device and ``sota.toml`` is generated, then the offline update command can either work alone or alone with ``aktualizr-lite``.
In the later case, you must stop the ``aktualizr-lite`` systemd service before running the offline update command.

.. _Offline Update Considerations:

Offline Update Considerations
-----------------------------

* **Offline Update is not a packaged delivery**

  The content provided by ``fioctl targets offline-update`` command should be packaged by you, and verified by the client service.

* **Offline Update does not provide a secure delivery**

  Related to the bullet above, Foundries.io™ cannot provide secure delivery of an update bundle since you should do the packaging and delivery.

* **Offline Update allows installing Targets from different Tags**

  A custom client application should handle this case if it is not the intended behavior.

* **Online/Offline Mixed Updates**

  Toggling between online and offline modes is not tested or validated by Foundries.io.
  It should be handled by a custom client application.
  Both cases can work together, but the offline update feature is designed to be offline only, until the device is registered.

There are a few points to take into account by the custom client application:

   * **The critical rule is not to run two types of updates/clients simultaneously**: ``aktualizr-lite`` should be stopped before ``aklite-offline`` runs and vice-versa.

   * Offline Update can downgrade version: A client around the offline updater should check it out and decide whether to allow a downgrade or not.

   * Offline Update does content-based shortlisting: Only the Apps included in a source directory are installed.

   * Offline Update fails if its input TUF metadata are outdated, e.g. an online update updated TUF root meta to version N while an offline content has version N-1 of root meta.

.. _TUF metadata:
   https://theupdateframework.io/metadata/

.. _OSTree:
  https://github.com/ostreedev/ostree
