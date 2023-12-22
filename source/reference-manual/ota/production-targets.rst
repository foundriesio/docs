.. _ref-production-targets:

Production Targets
==================

As a part of going to production, you need to define two distinct sets of devices: *test* versus *production*.
A **production device** is defined by a presence of a special attribute in its public certificate.
This is set at the :ref:`device registration time <ref-factory-registration-ref>`.
If the attribute is absent, it designates a **test device**.

As noted in the :ref:`offline keys documentation <ref-offline-keys>`,
FoundriesFactory® leverages The Update Framework (TUF) to deliver Over-the-Air (OTA) software updates to devices.
Production versus test devices receive different copies of the TUF metadata:

- Test devices receive :ref:`CI targets <ref-ci-targets>`.
- Production devices receive **production targets**,
  managed through so-called **waves** — a FoundriesFactory way to release updates to production devices.

Production Targets provide increased security compared to CI Targets.
They must be signed by the user-owned targets signing key, in addition to the Foundries.io™ owned signing key.

Normally, when the TUF targets metadata is updated, all devices see it and can start updating themselves.
Waves allow Factory operators to control an exact time when devices see a new version of the TUF targets metadata.

.. important::

    Production devices can only be updated to production Targets.
    The opposite is also true, production Targets can only be installed on production devices.
    From the TUF perspective CI versus production TUF Targets comprise two isolated sets of updates.

    Within the scope of the below paragraphs, "device" refers exclusively to a "production device".

.. _ref-rm-wave:

Performing a Production OTA
---------------------------

First define a process to select CI builds which need to be delivered to production devices.
Every user performing production OTAs should generate their personal :ref:`offline TUF targets key <ref-offline-keys>` to sign production Targets.

Let us assume you selected CI build version 42 as ready to be run in production.
To start the production release process, create a new wave using the below command::

  # fioctl waves init <wave-name> <target number> <tag> -k <keys.tgz>
  fioctl waves init -k /absolute/path/to/targets.only.key.tgz v2.0-update 42 production

This creates a new TUF targets role version for production devices which listen to OTA updates for the ``production`` tag.
That TUF targets role only includes a single Target from CI build (in the above example, that Target version is 42).

.. note::

   We recommend generating :ref:`OSTree Static Deltas <ref-static-deltas>` before rolling out waves to devices.
   Static Deltas will optimize your OTA update download.

Once created, a new wave can be rolled out to Factory production devices.
This can be either all at once, or in phases.
There are several ways how a wave can be rolled out:

- To a subset of devices in a specific device group.
- To all devices in a specific device group.
- To a subset of devices in a Factory (potentially, across several device groups, including group-less devices).
- To all devices in a Factory.

We recommend that you first roll out a wave to a dedicated device group, which contains a small number of production devices.
Another good option is to roll out a wave to a small subset of devices in a bigger device group.
Let us assume you want to first roll out a new ``v2.0-update`` wave to a device group called ``canary``.
This can be done using the below command::

  fioctl waves rollout v2.0-update canary

You can roll out a wave in as many phases as your workflow requires,
before making the software update generally available.
For example, you may decide to roll out a wave to device group ``us-east-1`` in several chunks,
after enough devices in group ``canary`` were updated successfully.
To do that, you would run the below command sequence::

  fioctl waves rollout v2.0-update us-east-1 --limit=10
  fioctl waves rollout v2.0-update us-east-1 --limit=50
  fioctl waves rollout v2.0-update us-east-1

The above command chain rolls out a wave to 10 devices in the ``us-east-1`` group,
then to 50 more devices (60 total), and finally to all remaining devices in that group.

You may also want to roll out a wave to a subset of devices in entire fleet, across several device groups::

  fioctl waves rollout v2.0-update --limit=5

It is possible to examine a list of devices that *would* be updated by a rollout command, without actually performing it::

  fioctl waves rollout v2.0-update --limit=5 --dry-run --print-uuids

.. note::

    Keep in mind that the device selection is pseudo-random, and can vary from one command run to another.

You can then inspect and amend that list of devices, and pass it back to the rollout command.
Alternatively, you can provide the device UUIDs to update::

  fioctl waves rollout v2.0-update --uuids=ab8ecb00-8ed4-42ff-90b2-815b371c0f86,7a733e81-f948-43a9-a358-56f3deb5f184

Check the ``fioctl waves rollout --help`` command for all available options,
or look at the :ref:`Advanced Usage <ref-rm-wave-adv>` for more complex workflows.
Hopefully, they should suit your specific production release lifecycle needs.

To monitor the status of your Factory OTA updates, use the ``fioctl status`` command.
FoundriesFactory also provides a dedicated command to monitor the wave status — ``fioctl wave status``.

Eventually, you may decide that a new software release (represented by a wave) is fit be generally available.
In this case, wave TUF targets need to be copied into production TUF targets for a specific tag.
In our example that is accomplished by using the below command::

  fioctl waves complete v2.0-update

Alternatively, if a wave progresses badly, you can cancel it using the below command (unless a wave is already completed)::

  fioctl waves cancel v2.0-update

Those devices that were successfully updated to Target 42 will continue to run it.
However, other production devices will not be updated, and will continue to run the previous version.

.. note::

  We recommend using a production target after a validated and completed wave to flash new production devices.

.. _ref-rm-wave-adv:

Advanced Usage
--------------

The FoundriesFactory ``fioctl waves rollout`` command allows implementing various release workflows.
This section focuses on supported, popular scenarios.

Releasing to Canary Devices
+++++++++++++++++++++++++++

Consider the most trivial use case — a Factory with a small device fleet.
In this case, the two most convenient ways to deliver updates in a controlled way are:

- Delivering updates to device groups, defined before the rollout.
- Delivering updates to ad-hoc device sets, generated at the rollout time.

Each option has pros and cons.
In both, the idea is to incrementally deliver the updates to your fleet in chunks, which gradually increase in size.

Using device groups, a typical setup would look this way.
Assume you have a fleet of 100 devices.
We recommend splitting up 2 device groups out of that fleet: e.g. "canary" having 5 devices, "beta" having 20 devices.
Canary devices would be those that are easier to reach out to in case of any issues during an update.
Having done that, a regular update rollout process would look like this::

    fioctl waves rollout v2.0-update --group canary
    fioctl waves rollout v2.0-update --group beta
    fioctl waves complete

.. note::

    It is up you to define the acceptance criterion for going to the next phase of the rollout.
    Usually, you would run the ``fioctl waves status`` command several times during that period.
    That allows you to watch a nearly real-time picture of how the update is going fleet-wide.
    There must be a *wait and watch* period after each rollout command before proceeding to the next one.

For the same example, you might opt to not use device groups, but still rollout the update in phases.
An equivalent way of doing this using randomized device fleet partitions may look like this::

    fioctl waves rollout v2.0-update --limit 5
    fioctl waves rollout v2.0-update --limit 20
    fioctl waves complete

Alternatively, you may create a file containing a comma-separated list of "canary" device UUIDs.
For example, assume you created a file ``canary-devices.lst``,
and you prefer to keep the next rollout phase randomized.
This way is even closer to the use of device groups, but does not necessitate their management::

    fioctl waves rollout v2.0-update --uuids @/path/to/canary-devices.lst
    fioctl waves rollout v2.0-update --limit 20
    fioctl waves complete

When using dynamic randomized device partitions for the rollout process,
Foundries.io APIs prioritize recently active devices over the offline devices.
It also filters out devices which already participated in a wave rollout.
That helps getting an early response about how the rollout is progressing,
and streamlines the gradual update of your device fleet to a newer version.

Releasing to Large Device Fleets
++++++++++++++++++++++++++++++++

Now let us look at a more complex example of rolling out an update to a large device fleet.
Assume that your Factory has 100'000 production devices to be updated within a wave.
Normally, these devices will be split into a couple of groups according to your criteria.
Also assume your device fleet is arranged according to geographic presence.
For example, having device groups ``us-east``, ``us-west``, ``eu-emea``, and ``apac``.
Some—or all—of these device groups would still contain a large number of devices.
From a safety perspective, it is risky to deliver an update to the entirety of any group like that.

A usual practice would be to apply the "canary" approach (described above) to every individual device group.
For example, commands below would roll out a wave to the ``us-east`` group in 4 incremental chunks::

    fioctl waves rollout v2.0-update --group us-east --limit 5
    fioctl waves rollout v2.0-update --group us-east --limit 20
    fioctl waves rollout v2.0-update --group us-east --limit 100
    fioctl waves rollout v2.0-update --group us-east

You can then use the same technique to roll out an update to other device groups.

Integration with External Device Management Systems
+++++++++++++++++++++++++++++++++++++++++++++++++++

An ability to specify the exact list of device UUIDs to the rollout command allows you to integrate it with your device management system.
For example, let us assume that your ``eu-emea`` device group is the biggest, containing 40'000 devices.
You might use your device management system to split that fleet into several partitions.
For that, you would export the appropriate subsets of device UUIDs into one or more files in a Comma Separated Values (CSV) format.
We support various characters as separators: a comma, a semicolon, and all sorts of newlines and white space.
For example, let's assume a user prepared the following lists of device UUIDs::

- 4 equal partitions ``phase1.lst, phase2.lst, phase3.lst, phase4.lst``, containing 10'000 devices each.
- a partition ``canary.lst``, containing 20 carefully pre-selected "canary" devices, that may intersect with the above partitions.

That would allow you to roll out an update to the device group "eu-emea" in an even more controlled way::

    fioctl waves rollout v2.0-update --group eu-emea --uuids @/path/to/canary.lst
    fioctl waves rollout v2.0-update --group eu-emea --limit 100 --uuids @/path/to/phase1.lst
    fioctl waves rollout v2.0-update --group eu-emea --limit 100 --uuids @/path/to/phase2.lst
    fioctl waves rollout v2.0-update --group eu-emea --limit 100 --uuids @/path/to/phase3.lst
    fioctl waves rollout v2.0-update --group eu-emea --limit 100 --uuids @/path/to/phase4.lst
    fioctl waves rollout v2.0-update --group eu-emea

The above commands roll out to "canary" devices, then to 100 random devices in each "phase",
and finally, to the remainder of the device group.

Going Beyond Limits
+++++++++++++++++++

.. note::

    At Foundries.io, we care a lot about the speed of our APIs and scaling to large device fleets.
    That strategy binds us to define certain limits for specific device management operations.
    One such limit is that you cannot pass more than 10'000 device UUIDs to a single rollout command.
    That constraint also implies that the ``--limit`` argument does not accept a value bigger than 10'000.
    It is still possible to pass more than 10'000 device UUIDs using several rollout commands.
    Also, you can roll out to the entire device group.

    When rolling out to a subset of devices using ``--limit`` argument,
    the "randomized" sample will exclude devices that were already updated to a wave version.
    It also tries to exclude devices that were staged for update
    (included in the device UUID list) in previous rollout commands, but not yet updated to a wave version.

    Precision of the latter criteria drops if previous rollout commands to the same group provided more than 10'000 device UUIDs in total.
    In particular, the same (not yet updated) device can be selected for the rollout several times.
    That precision loss allows us to keep the decision making speed reasonable,
    regardless of the number of devices in your Factory, theoretically scaling to infinity.
    You can restore a lossless precision by specifying both ``--uuids`` and ``--limit`` arguments, as described in an example above.

The techniques described above can be applied without using the ``--group`` argument.
In this case, the rollout command will be applied to a subset of the entire device fleet.
For example, the below commands roll out a wave to 5'000 devices in a ``pre-selected.lst`` file across the entire fleet in 4 incremental chunks::

    fioctl waves rollout v2.0-update --limit 100 --uuids @/path/to/pre-selected.lst
    fioctl waves rollout v2.0-update --limit 400 --uuids @/path/to/pre-selected.lst
    fioctl waves rollout v2.0-update --limit 1000 --uuids @/path/to/pre-selected.lst
    fioctl waves rollout v2.0-update --limit 3500 --uuids @/path/to/pre-selected.lst

You can also dump a pre-selected device list into a file; then inspect, amend, and push it back to the rollout command::

    fioctl waves rollout v2.0-update --limit 1000 --print-uuids >/path/to/pre-selected.lst
    # Open and edit /path/to/pre-selected.lst using your editor of choice.
    fioctl waves rollout v2.0-update --uuids >/path/to/pre-selected.lst

One way or another, Fioctl® allows you to implement various processes to roll out updates to your Factory's device fleet.
