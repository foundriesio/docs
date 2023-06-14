.. _ref-production-targets:

Production Targets
==================

As noted in the :ref:`offline keys documentation<ref-offline-keys>`,
FoundriesFactory® leverages The Update Framework (TUF) to deliver Over-the-Air (OTA) Software Updates to devices.
By design, production devices receive a slightly different copy of TUF targets metadata than test devices.
Production TUF targets must be signed by both Foundries.io™ owned and user-owned targets signing keys.

Production targets are managed through so-called **waves** — a FoundriesFactory way to release production updates.
Normally, when the TUF targets metadata is updated, all devices see it and can start updating themselves.
Waves allow Factory operators to control an exact time when devices see a new version of the TUF targets metadata.

.. note::

    Production devices can only be updated to production targets.
    The opposite is also true, production targets can only be installed on production devices.
    From the TUF perspective these are two isolated sets of updates.

    Within a scope of below paragraphs a term "device" always means a "production device".

.. _ref-rm-wave:

Performing a Production OTA
---------------------------

A user should define a process to select CI builds which need to be delivered to production devices.
Let's assume a user selected a CI build version 42 as ready to be run in production.
To start the production release process, a user would create a new wave using the below command::

  # fioctl waves init <wave-name> <target number> <tag> -k <keys.tgz>
  fioctl waves init -k /absolute/path/to/targets.only.key.tgz v2.0-update 42 production

This creates a new TUF targets role version for production devices which listen to OTA updates for the ``production`` tag.
That TUF targets role only includes a single Target from CI build (in above example, that target version is 42).

.. note::

   We recommend that a user generates :ref:`OSTree static deltas<ref-static-deltas>` before rolling out waves to devices.

Once created, a new wave can be rolled out to Factory production devices, all at once or in phases.
We recommend to first roll out a wave to a dedicated device group, which contains a small number of production devices.
Let's assume a user wants to first roll out a new ``v2.0-update`` wave to a device group called ``canary``.
This can be done using the below command::

  fioctl waves rollout v2.0-update canary

A user can roll out a wave to as many device groups as their workflow requires,
before making the software update generally available.
For example, a user may decide to roll out a wave to device group ``us-east-1``,
after enough devices in group ``canary`` were updated successfully.
To do that, a user would run the below command::

  fioctl waves rollout v2.0-update us-east-1

To monitor the status of your Factory OTA updates status use the ``fioctl status`` command.
FoundriesFactory also provides a dedicated command to monitor the wave OTA updates status — ``fioctl wave status``.

Eventually, a user may decide that a new software release (represented by a wave) is good enough to be generally available.
In this case, wave TUF targets need to be copied into production TUF targets for a specific tag.
In our example that is accomplished by using the below command::

  fioctl waves complete v2.0-update

Alternatively, if a wave progresses badly, a user can cancel it using the below command (unless a wave is already completed)::

  fioctl waves cancel v2.0-update

Those devices that were successfully updated to Target 42 will continue to run it.
However, other production devices will not be updated, and will continue to run the previous version.

.. note::

  We recommend using a production target after a validated and completed wave to flash new production devices.
