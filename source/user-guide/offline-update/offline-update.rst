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

2. Enable Apps fetching if you would like to update ``Compose Apps`` along with rootfs (aka ostree).
   To do so, add the following configuration snippet to the ``containers`` section of :ref:`your Factory definition <ref-factory-definition>`:

    .. prompt:: bash


        containers:
            ...
            offline:
                enabled: <true | false>
                app_shortlist: <comma separated list of apps> # all target apps are fetched if not specified or empty


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
    - Failed to update TUF metadata.
- *6*: Installation was not performed.
    - Failed to find Targets in the device TUF repo that matches a device tag and/or hardware ID.
- *8*: Installation was not performed.
    - Failed to find the ostree commit and/or all Apps of the Target to be installed in the provided source bundle.
- *10*: Installation succeeded.
    -  ``aklite-offline run`` must be invoked to start the updated Apps.
- *11*: Installation was not performed.
    - Provided TUF metadata is invalid.
- *12*: Installation was not performed.
    - Provided TUF metadata is expired.
- *14*: Installation was not performed.
    - TUF metadata not found in the provided path.
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

* **Offline Update Bundle Packaging**

  The content provided by ``fioctl targets offline-update`` command should be packaged by you, and verified by the client service.

* **Offline Update Bundle Delivery**

  Related to the bullet above, Foundries.io™ cannot provide secure delivery of an update bundle since you should do the packaging and delivery.

* **Offline Update for Unregistered Devices**

  When dealing with devices not registered in FoundriesFactory® or :ref:`a custom registration server <ref-fully-detached>`,
  several considerations arise:

  * Production Status: The distinction between production and non-production status of the device remains undetermined.
  * Device Tag: The specific tag associated with the device is not configured.

  As a consequence, during the initial offline update, users can install both production and non-production targets on unregistered devices.
  However, subsequent updates are constrained by the type of targets installed during the initial update.
  Therefore, the target type chosen during the first update dictates the supported targets' type for future updates.

  Additionally, due to the absence of a defined tag in the configuration of unregistered devices,
  users can install targets associated with any tag.
  This issue can be addressed by incorporating a configuration snippet (a ``*.toml`` file) into either ``/usr/lib/sota/conf.d`` or ``/etc/sota/conf.d``.
  We recommend implementing this solution through a new recipe in the factory's ``meta-subscriber-overrides.git`` repository.
  The snippet should contain the following content:

.. prompt:: text

    [pacman]
    tags = "<tag>"

* **Online/Offline Mixed Updates (aka hybrid mode)**

  There are a few points to take into account by the custom client application:

  * Offline or Online downgrade fails by default.
    Therefore, if the latest target is installed on a device through an online update,
    then an offline update for the outdated bundle fails, unless a user explicitly specifies the ``--force`` parameter.
  * Offline Update fails if its input TUF metadata are outdated.
    For example, it fails if an online update upgrades the device's TUF root/timestamp/snapshot/targets metadata
    to version N while the bundle contains version N-1 of the metadata.
  * Running offline and online update simultaneously leads to undefined behaviour.
    It is impossible to run two or more update agents of the same or different types simultaneously,
    for example ``aktualizr-lite daemon`` and ``aklite-offline``.
    However, since the API supports both types of the update, a user may develop :ref:`a custom sota client <ug-custom-sota-client>` that does
    these two types of update in parallel by mistake.

Controlling the Expiration Time of the Offline Update Bundle
------------------------------------------------------------

The bundle obtained through the ``fioctl targets offline-update`` command comes with an expiration time.
If the expiration time of the bundle has passed, the offline update will fail.

Use the ``--expires-in-days`` parameter of the ``fioctl targets offline-update`` command to set the desired expiration time of the bundle.
If the command fails with the one of the errors below, then it means the root or
targets metadata expires sooner than the date specified in the parameter.

.. code-block:: bash

    Getting CI Target details; target: intel-corei7-64-lmp-2377, tag: master...
    Refreshing and downloading TUF metadata for Target intel-corei7-64-lmp-2377 to 2377/tuf...
    ERROR: Failed to download TUF metadata: HTTP error during POST 'https://api.foundries.io/ota/factories/<factory>/targets/intel-corei7-64-lmp-2377/meta/': 400 BAD REQUEST
    = Root metadata expire (2024-07-06T07:56:57Z) before the specified expiration time (2025-02-11T09:17:39Z)

    Getting production Target details; target: intel-corei7-64-lmp-2356, tag: master...
    Refreshing and downloading TUF metadata for Target intel-corei7-64-lmp-2356 to 2356/tuf...
    ERROR: Failed to download TUF metadata: HTTP error during POST 'https://api.foundries.io/ota/factories/<factory>/targets/intel-corei7-64-lmp-2356/meta/': 400 BAD REQUEST
    = Targets metadata expire (2025-01-28T16:38:23Z) before the specified expiration time (2025-02-06T09:27:35Z)

To fix the issue, either decrease the parameter value or refresh the root/targets metadata accordingly and then re-run the command.

To refresh root metadata you should :ref:`rotate TUF root role key <ref-offline-tuf-root-key-rotation>`.
The expiration time is set to one year since the moment of the latest root key rotation.

To refresh targets role metadata use one of the following depending on targets type, CI or wave/production.

* CI targets — Trigger a new CI build, it will create a new target and update CI targets role metadata expiration time to 1 year since the moment of creation.
* Wave or production targets — Create a new wave for the given target version.
  Use ``--expires-days`` or ``--expires-at`` parameters of the ``fioctl waves init`` command to set a desired expiration time.
  By default, if none of the parameters above are specified, the expiration of a wave's targets role metadata is set to one year.

Therefore, the ``--expires-in-days`` parameter of the ``fioctl targets offline-update`` command is the primary knob
to tune the bundle's expiration time up to 1 year (the maximum validity period of TUF root metadata).
Effectively, this parameter sets the expiration time for the bundle's copy of the TUF timestamp role metadata, and does not affect the factory's metadata.

Root and/or CI/wave/production targets refreshing serves as the secondary mechanism.
It should be applied if the desired expiration time occurs later than
the root's and/or the targets' expiration, respectively.

More details on FoundriesFactory TUF metadata expiration time can be found in :ref:`the following section <Math Behind the Offline Update Bundle Expiration Time>`.

.. _Math Behind the Offline Update Bundle Expiration Time:

Understanding the Math Behind the Offline Update Bundle Expiration Time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The expiration time of the bundle is determined by the expiration times of the TUF metadata it encompasses.
Specifically, it equals the minimum value among the expiration times across all TUF roles' metadata.

* CI/Wave/Production *root* role metadata
    The expiration time is set to 1 year from the moment when of the latest TUF root key was added or rotated.
    The other commands that modify the TUF root metadata do not extend its expiration.
    It is possible to set the TUF root expiration time to any value through the API.

* CI *timestamp*, *snapshot*, and *targets* roles metadata
    The default expiration time is set to 1 year since the last successful CI build.
    If there are no builds for a year, the expiration is automatically extended by one month every month.
    A user can overwrite the default value using the factory config parameter :ref:`tuf.targets_expire_after <def-tuf-expiration>`.

* Wave/Production *timestamp* roles metadata
    The expiration time is set to 7 days.
    The `TUF specification`_ recommends setting a short expiration date for the TUF timestamp metadata and re-signing it frequently.
    This allows clients to quickly detect if they are being prevented from obtaining the most recent metadata ("indefinite freeze attacks").
    The FoundriesFactory automatically refreshes the metadata for an additional 7 days just before expiration.

* Wave/Production *snapshot* and *targets* roles metadata
    The default expiration time is set to 1 year.
    A user can overwrite the default value using the ``--expires-days`` or ``--expires-at`` parameter of the ``fioctl wave init`` command.

.. _TUF metadata:
   https://theupdateframework.io/metadata/

.. _TUF specification:
   https://theupdateframework.github.io/specification/latest/

.. _OSTree:
  https://github.com/ostreedev/ostree
