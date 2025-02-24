.. _ref-update-rollback:

Update Rollback
===============

The Foundries.io™ OTA update service is intended for updating software referenced by a :ref:`Target <ref-targets>`.
Installation of artifacts for a new ``Target`` version on a device may fail for some reason or another.
When this happens, the :ref:`OTA Client <ref-aktualizr-lite>` and the bootloader performs an "Update Rollback" procedure.
This will reinstall and actualize the previous version of ``Target`` artifacts.

``Target`` describes two updatable items: an `OSTree`_ — managed rootfs and the :ref:`Compose Apps <ref-compose-apps>`.
Therefore, versions (hashes) of the ``Target`` components are bound by a specific ``Target`` version (number).
If one updated component fails to install, then both components should be rolled back to the previous version.
This is regardless of the installation status of the other component.

During an update, ``aktualizr-lite`` (the :ref:`OTA Client <ref-aktualizr-lite>`) tries to install a new version of rootfs at first, if found, and then it installs ``Compose Apps``.


Rollback Driven by Rootfs Update Failure
________________________________________

An installation of an `OSTree`_ — managed rootfs consists of two phases:

1. Deployment of a new ostree version.
   Effectively, it is creating hard links for each file of a specific ostree commit, and the corresponding drop-in boot snippet.
   See `OSTree Deployment Doc`_ for more details.
2. Booting a device upon deployment of the new rootfs version.


If the first phase fails then the installation is interrupted and Update Rollback happens:

1.  ``aktualizr-lite`` redeploys the previous version of rootfs;
2.  ``aktualizr-lite`` prunes unused ``Compose Apps`` data (container images/layers of the new version).

If a boot on a new version of rootfs fails three times then:

1. The bootloader boots the previous deployment of rootfs;
2. ``aktualizr-lite`` re-installs the previous version of ``Compose Apps``;
3. ``aktualizr-lite`` prunes unused Compose Apps data (container images/layers of the new version).

Rollback Driven by a Bootloader Update Failure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The FoundriesFactory™ Platform OTA update service supports bootloader update.
Effectively, boot artifacts are included into `OSTree`_ — managed rootfs.
Therefore, a rollback procedure in the case of a bootloader update failure, is the same as in the case of the ostree update failure.
The only difference is how and when the rollback is triggered.
In the case of a regular ostree update, the rollback is managed by the bootloader, and is triggered after a boot fails three times.
In the case of bootloader update failure, the triggering of the rollback depends on a specific hardware.
See :ref:`Boot software updates <ref-boot-software-updates>` for more details.


Rollback Driven by Compose Apps Update Failure
______________________________________________

The rollback procedure depends on the two factors:

1. An update type—whether it is just an Apps update, or a composite update—that includes both rootfs and Apps update.
2. A value of the  :ref:`aktualizr-lite parameter <ref-aktualizr-lite-params>` called ``create_containers_before_reboot``.


Apps Driven Rollback in the Case of a Composite Update
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the first phase of an `OSTree`_ — managed rootfs update is successful, and ``create_containers_before_reboot`` is set to 1 (default), then Apps' containers are (re-)created before a device reboot.
This is needed to apply a new version of rootfs.
However, the Apps' containers (re-)creation may fail.
If that happens, then Apps driven rollback is triggered:

1. ``Aktualizr-lite`` redeploys the previous version of rootfs.
2. ``Aktualizr-lite`` (re-)creates and starts the previous version of Apps' containers.
3. ``Aktualizr-lite`` prunes unused Compose Apps data (container images/layers of the new version).

If ``create_containers_before_reboot`` is set to 0, and a device is successfully booted on a new version of rootfs just after an update, then ``aktualizr-lite`` (re-)creates and starts Apps' containers on its start.
If one of these actions (creation or start) fails, then another type of Apps driven rollback is triggered:

1. ``Aktualizr-lite`` redeploys the previous version of rootfs.
2. ``Aktualizr-lite`` initiates a device reboot.
3. A device boots on the previous version.
4. ``Aktualizr-lite`` (re-)creates and starts the previous version of Apps' containers.
5. ``Aktualizr-lite`` prunes unused Compose Apps data (container images/layers of the failed new version).


Apps Driven Rollback in the Case of a Just Apps Update
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If a new Target installation includes only App updates, and the new version fails at creation or start, then the rollback process does the following:

1. ``Aktualizr-lite`` (re-)creates and starts the previous version of Apps' containers.
2. ``Aktualizr-lite`` prunes unused Compose Apps data (container images/layers of the failed new version).


Rollback Driven by User (Experimental)
______________________________________

The ``Aktualizr-lite`` command line interface allow a rollback to be explicitly initiated.
It is meant to be used in scenarios where additional logic is required to determine if the Target was successfully installed and started.
:ref:`User Initiated Rollback<ref-aklite-command-line-interface-rollback>` for more information.

.. _OSTree:
  https://github.com/ostreedev/ostree
.. _OSTree Deployment Doc:
  https://ostreedev.github.io/ostree/deployment
