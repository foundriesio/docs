.. _ug-offline-update:

Offline Updates
===============

This section guides you through the steps of updating a device offline.

.. tip::
   Make sure to check the :ref:`Offline Update Considerations`.

.. note::
    Since LmP v95, offline updates can be applied using the ``aktualizr-lite`` command-line interface, instead of the ``aklite-offline`` utility.

Prerequisites
-------------

1. Enable Apps fetching if you would like to update ``Compose Apps`` along with rootfs (aka ostree).
   To do so, add the following configuration snippet to the ``containers`` section of :ref:`your Factory definition <ref-factory-definition>`:

    .. code-block:: yaml


        containers:
            ...
            offline:
                enabled: <true | false> # `false` implies that apps are disabled for an offline update
                app_shortlist: <comma separated list of apps> # all target apps are fetched if not specified or empty; if absent then the image preloading app shortlist is applied if set

            ref_options:
                refs/heads/<branch>:
                    params:
                        FETCH_APPS: <"1" | "0"> # overrides value set in `containers.offline.enabled` for a given branch
                        FETCH_APPS_SHORTLIST: <comma separated list of apps> # overrides value set in `containers.offline.app_shortlist` for a given branch


2. Ensure that :ref:`The Update Framework (TUF) keys are taken offline <ref-offline-keys>`.

3. Build an LmP image and flash it onto a target device or update the device with the image via OTA.

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

Signing the Offline Update Bundle
---------------------------------
It is essential to sign the bundle using one or more `TUF targets role`_ keys.
This ensures the authenticity of an offline update bundle during the update process on a device.

If the bundle contains :ref:`CI targets <ref-ci-targets>`, it is signed by the OTA Lite service using the online TUF targets role key.
Users do not need to take any action in this scenario.

If the bundle contains :ref:`production or wave targets <ref-production-targets>`, it should be signed using one or more TUF targets offline keys.
Use ``fioctl targets offline-update sign <bundle-path> --keys <path-to-targets-keys-file>`` command to sign the bundle.
The number of required signatures is determined by the threshold set in the latest `TUF root role metadata`_,
which is printed as part of the overall output of any of the ``fioctl targets offline-update`` sub-commands.
Additionally, you can find out the signature threshold by running ``fioctl targets offline-update show <bundle-path>``,
as well as by using ``fioctl keys tuf show-root --prod`` command (look for the targets role threshold).

``aktualizr-lite`` verifies the bundle signature(s) before initiating the update process to check the authenticity of the bundle.
If the signature check fails, the update process will not be started.

Performing the Offline Update
-----------------------------

Before doing the offline update, ensure the bundle is accessible on a device, e.g., attach and mount the USB drive.

Use the ``aktualizr-lite`` CLI to perform an offline update.

1. Run ``aktualizr-lite update [--config <config dir or file>] --src-dir <path to a bundle>``.

2. Depending on the ``aktualizr-lite update`` result, additional actions may be required to complete the update:

    a. code 100: reboot device and invoke ``aktualizr-lite run [--config <config dir or file>]`` to finalize an ostree installation and start Apps if both ostree/rootfs and Apps are updated;
    b. code 90: reboot device to finalize the previous boot firmware update and go to the step #1 to start the update.

3. Reboot a device after running ``aktualizr-lite run [--config <config dir or file>]`` command if:

    a. code 120: Apps failed to start after update, you must reboot the device and re-execute ``aktualizr-lite run`` to complete the rollback;
    b. code 5: the update includes a boot firmware, you can optionally reboot a device to finalize the boot firmware upgrade.


Detailed information about the aktualizr-lite CLI is provided in the :ref:`aktualizr-lite CLI documentation <ug-aktualizr-lite-cli>`,
including all the possible return codes for each operation.

Configuration Details
~~~~~~~~~~~~~~~~~~~~~

The minimum required configuration is:

.. code-block:: none

    [provision]
    primary_ecu_hardware_id = <>

The command can digest the default device config consisting of:

1. ``*toml`` files added into LmP during bitbaking (usually just ``/usr/lib/sota/conf.d/40-hardware-id.toml``);
2. ``sota.toml`` generated by ``lmp-device-register``.

If a device needs to support offline **and** online updating, then the configuration needs to be shared between both modes.

Normally, each LmP image includes a configuration file ``/usr/lib/sota/conf.d/40-hardware-id.toml`` which defines a hardware ID.
Therefore, by default, an LmP image includes the minimum required configuration, hence NO device registration is required for offline updates to work.

If you register a device and ``sota.toml`` is generated, then the offline update command can either work alone or alone with ``aktualizr-lite`` daemon.
In the later case, you must stop the ``aktualizr-lite`` systemd service before running the offline update command.

.. _Offline Update Considerations:

Offline Update Considerations
-----------------------------

* **Offline Update Bundle Packaging**

  The content provided by ``fioctl targets offline-update`` command should be packaged by you, and verified by the client service.

* **Offline Update Bundle Delivery**

  Related to the bullet above, Foundries.io™ cannot provide secure delivery of an update bundle since you should do the packaging and delivery.

* **Offline Update for Unregistered Devices**

  When dealing with devices not registered with the FoundriesFactory™ service or :ref:`a custom registration server <ref-fully-detached>`,
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

.. code-block:: none

    [pacman]
    tags = "<tag>"

* **Online/Offline Mixed Updates (aka hybrid mode)**

  There are a few points to take into account by the custom client application:

  * Offline or Online downgrade fails by default.
    In order to force the downgrade, a user must explicitly specify version or Target name intended to be installed,
    using the ``--update-name`` option.
  * Offline Update will ignore the TUF metadata if it is outdated,
    but will still allow an update to be performed if the bundle content matches the device's current metadata.

Controlling the Expiration Time of the Offline Update Bundle
------------------------------------------------------------

The bundle obtained through the ``fioctl targets offline-update`` command comes with an expiration time.
**If the expiration time of the bundle has passed, the offline update will fail.**

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

More details on FoundriesFactory TUF metadata expiration time can be found in :ref:`Math Behind the Offline Update Bundle Expiration Time`.

Considerations About Offline Update Bundle Validity and TUF Rotation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are some particularities on the offline update bundle validity after TUF rotations.
This depends on the versions of the TUF root and targets keys at the time of generating the bundle and whether the device is online, hybrid or fully offline.

The table below shows practical cases to deliver long term offline updates to your fleet. Here, ``Old TUF Meta`` means the old TUF metadata used prior to a TUF root key rotation, while ``New TUF Meta`` means the TUF metadata used after a TUF root key rotation. The table points which set of keys were used to generate the device image and offline update bundle.

.. list-table:: Offline Update Validity x TUF Rotation x Device State
   :header-rows: 1
   :align: center
   :widths: 1 1 1 3

   * - Device Image
     - TUF State
     - Offline Bundle
     - Behavior
   * - Old TUF Meta
     - Keys not rotated
     - Old TUF Meta
     - Default state (1):

         * If the offline update bundle is not expired, the update client **will accept** the offline update bundle installation.
         * After the offline update bundle is expired, the update client **will decline** the offline update bundle installation.
   * - Old TUF Meta
     - Keys rotated
     - Old TUF Meta
     - * Fully offline devices: Same as (1).
       * Online/hybrid devices: Once the device gets online and fetches new TUF metadata after the TUF keys rotation, the update client **will decline** the offline update bundle generated with old TUF metadata.
   * - Old TUF Meta
     - Keys rotated
     - New TUF Meta
     - If the offline update bundle is not expired, the update client **will accept** the offline update bundle installation. From this point on, the update client will only install bundles generated with the new TUF metadata. This is valid for online, hybrid and fully offline devices.
   * - New TUF Meta
     - Keys rotated
     - Old TUF Meta
     - The update client **will decline** the offline update bundle installation in any cases.

.. note::
   You can check your offline update bundle expiration with: ``fioctl targets offline-update show <bundle>``.

For the cases where the update client **will decline** the offline update bundle installation, you should regenerate the offline update bundle with new validity, or refresh the TUF metadata in the existing bundle with: ``fioctl targets offline-update --tuf-only``.

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

.. _TUF targets role:
   https://theupdateframework.github.io/specification/latest/#targets

.. _TUF root role metadata:
   https://theupdateframework.github.io/specification/latest/#root

.. _TUF specification:
   https://theupdateframework.github.io/specification/latest/

.. _OSTree:
  https://github.com/ostreedev/ostree
