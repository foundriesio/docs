.. _ref-production-targets:

Production Targets
==================

As a part of going to production, a user needs to define two distinct sets of devices: test versus production.
A **production device** is defined by a presence of a special attribute in its public certificate,
which is set at the :ref:`device registration time <ref-factory-registration-ref>`.
If that attribute is absent, it designates a **test device**.

As noted in the :ref:`offline keys documentation<ref-offline-keys>`,
FoundriesFactory® leverages The Update Framework (TUF) to deliver Over-the-Air (OTA) Software Updates to devices.
Production versus test devices receive different copies of the TUF metadata:

- Test devices receive :ref:`CI targets <ref-ci-targets>`.
- Production devices receive **production targets**,
  managed through so-called **waves** — a FoundriesFactory way to release updates to production devices.

Production targets provide an increased security compared to CI targets.
They must be signed by the user-owned targets signing key, in addition to the Foundries.io™ owned signing key.

Normally, when the TUF targets metadata is updated, all devices see it and can start updating themselves.
Waves allow Factory operators to control an exact time when devices see a new version of the TUF targets metadata.

.. note::

    Production devices can only be updated to production targets.
    The opposite is also true, production targets can only be installed on production devices.
    From the TUF perspective CI versus production TUF targets comprise two isolated sets of updates.

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
There are several ways how a wave can be rolled out:

- To a subset of devices in a specific device group.
- To all devices in a specific device group.
- To a subset of devices in a Factory (potentially, across several device groups, and including group-less devices).
- To all devices in a Factory.

We recommend to first roll out a wave to a dedicated device group, which contains a small number of production devices.
Another good option is to roll out a wave to a small subset of devices in a bigger device group.
Let's assume a user wants to first roll out a new ``v2.0-update`` wave to a device group called ``canary``.
This can be done using the below command::

  fioctl waves rollout v2.0-update canary

A user can roll out a wave in as many phases as their workflow requires,
before making the software update generally available.
For example, a user may decide to roll out a wave to device group ``us-east-1`` in several chunks,
after enough devices in group ``canary`` were updated successfully.
To do that, a user would run the below command sequence::

  fioctl waves rollout v2.0-update us-east-1 --limit=10
  fioctl waves rollout v2.0-update us-east-1 --limit=50
  fioctl waves rollout v2.0-update us-east-1

The above command chain rolls out a wave to 10 devices in the ``us-east-1`` group,
then to 50 more devices (60 total), and finally to all remaining devices in that group.

A user may also want to roll out a wave to a subset of devices in entire fleet, across several device groups.
That can be accomplished by the below command::

  fioctl waves rollout v2.0-update --limit=5

It is possible to examine a list of devices that would be updated by a rollout command, without actually performing it::

  fioctl waves rollout v2.0-update --limit=5 --dry-run --print-uuids

.. note::

    Keep in mind that the device selection is pseudo-random, and can vary from one command run to another.

A user can then inspect and amend that list of devices, and pass it back to the rollout command.
Alternatively, a user can provide their own choice of device UUIDs to update, like in the below command::

  fioctl waves rollout v2.0-update --uuids=ab8ecb00-8ed4-42ff-90b2-815b371c0f86,7a733e81-f948-43a9-a358-56f3deb5f184

Please, check the ``fioctl waves rollout --help`` command for all available options.
Hopefully, they should suit your specific production release lifecycle needs.

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
