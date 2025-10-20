.. _ref-ug-dev-workflow:

Developer Workflow and Guidelines
=================================

This document outlines best practices and relevant information to get started developing with the FoundriesFactory™ Platform.
The workflows suggested here provide simple ways of working from development to production, aiming to keep your fleet and your code up to date and easy to maintain.

Overview of Factory Configuration
---------------------------------

We leverage the tagging functionality of FoundriesFactory to simplify the development process. Let's recap:

* A device registered to the Factory follows a single tag and runs the latest available Target for that tag.

* The ``ci-scripts`` repository of your Factory is used to define the platform and container branches used by our continuous integration system to create Targets.

* The built Targets are tagged as specified in the ``factory-config.yml`` file.

* Fioctl can be used to append or modify the Targets tags.

.. seealso::
   :ref:`ref-factory-sources`

   `What's a Target`_

Development Best Practices
--------------------------

Branching
~~~~~~~~~

By default, each source repository has a single ``main`` branch.
Additional branches can be created and enabled to build in your Factory, see :ref:`ref-new-branch`.

We recommend the following branch strategy:

* ``main`` as the stable development

	``main`` can be used as a reference for release candidates and marking Targets ready for production.

* ``devel`` as the experimental branch

	``devel`` is ahead of ``main`` and can be used for active development.

	Once stable, it should be merged back to ``main``.

* ``next`` as the LmP migration branch

	``next`` is used to bring new LmP versions to your Factory.

.. tip::
   Adapting a new LmP version to your Factory can be challenging, particularly when there is a BSP update available. It often requires several iterations until the migration is complete, so we recommend using a special branch for that.
   Once the migration is complete, it should be merged back to ``devel``/``main``.

If you have bigger development teams and require more granular division of branches, we also recommend the following:

- ``developer`` branches

	Owned by a developer.

	Branches off of ``devel`` for a particular development.

	Example: ``devel-joe``.

	It should be merged back to ``devel`` once the development is complete.

	It should be rebased frequently to keep up to date with ``devel`` and avoid conflicts.

- ``feature`` branches

	Feature specific branch.

	Similar to developer branches, this branches off of ``devel`` and requires rebasing to keep up to date with the active development.

	The feature name is assigned to the branch name, so a ``ci-scripts`` change is required at every new branch/feature.

	Example: ``feature-enable-wifi7``.

- ``generic-feature`` branches

	Feature specific branch similar as above, however it uses a generic name so only the initial ``ci-scripts`` change is needed as the branch is reused for multiple features.

	Rebasing after each set of feature changes are merged is required.

	Example: ``feature-wifi``, used for all wifi feature changes over time.

.. important::
   We recommend that the ``main`` and ``devel`` branches are managed by an admin and that developers keep their child branches up to date with the latest development.

   Enabling :ref:`ug-mirror-action` allows setting up pull requests for peer reviews.

.. note::
   Although there is no limit of branches/tags you can have in a Factory, we recommend cleaning up stale branches from time to time.

Embedded and OS Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~

LmP provides a minimal OS image with OTA and device management capabilities.
Customers should tailor the image according to their needs.

If a custom board is used, it is also expected that customers provide the board support patches for their design.

.. seealso::
   :ref:`tutorial-customizing-the-platform`

   :ref:`lmp-customization`

Some tips for this stage of the development:

* :ref:`Local builds <ref-linux-building>`

	Provides fast iterations. This is particularly useful when debugging board support issues during LmP migrations.

	No OTA update support in locally built images.

* ``lmp-base`` :ref:`distro <ref-linux-distro>`

	Developer friendly distro, with no OSTree support.
	This provides a standard read-write rootfs, where boot files can be easily replaced for fast iterations.

	Useful when doing the initial bootloader and device tree porting.

	No OTA update support for ``lmp-base`` images.

Application Development
~~~~~~~~~~~~~~~~~~~~~~~

We recommend that the applications are developed using :ref:`ref-compose-apps` so they are detached from the OS code.

Some tips for this stage of the development:

* :ref:`ref-private-registries`

	Besides setting up a :ref:`ug-mirror-action`, it is also possible to set up your FoundriesFactory to access third-party container registries.
	This allows container images to be built externally and for FoundriesFactory CI to only pull these containers.

	This helps to keep your source code protected with restricted access.

	.. seealso::
	   :ref:`ref-ug-ip-protection`

* Using Multi-Arch Containers

	By default, the FoundriesFactory CI builds container images for ``amd64``, ``armhf``, and ``aarch64`` architectures.

	Multi-arch containers benefits customers on resource-constrained devices by allowing users to do most of their application development on a standard laptop (x86/``amd64`` architecture) before pushing to the ``containers`` repository.
	Developers can then pull the ``amd64`` image for local debug.
	See an example in :ref:`tutorial-gs-with-docker`.

	Building for both ``armhf`` and ``aarch64`` is also interesting when there are future plans to migrate from one architecture to another.
	The apps are ready!

* :ref:`ug-container-preloading`

	Container preloading enables an additional CI run to preload the containers into the image used for flashing the device.

	This allows your apps to start before the device is registered to your Factory.
	This may also help reduce the size of the first update.

.. note::
   Containers require an equivalent platform build, otherwise the ``publish-compose-apps`` CI run fails.
   Though, it is possible to re-use platform builds for different container branches.
   See :ref:`ref-advanced-tagging`.

Tagging and Testing
~~~~~~~~~~~~~~~~~~~

By default, a device updates to the latest available Target for the tag it follows.

It is possible to manipulate the Targets by adding and removing tags to achieve diverse scenarios.
This is useful for testing purposes, moving devices to specific builds and for flagging particular Targets.

.. note::
   Quick Commands:

   * Add/remove a tag to/from a Target

   .. code-block::

      $ fioctl targets tag --tags <list-of-tags> --by-version <build_number>

   * Change the tag a device follows

   .. code-block::

      $ fioctl device config updates <device> --tags <tag>

   * List Targets by tag

   .. code-block::

      $ fioctl targets list --by-tag <tag>

Here we cover common use cases and workflows:

* **Keeping a Device on a Particular Target**

A device ``dev-1`` follows the tag ``devel``, and runs the Target ``100``.
You do not wish to update this device, so you create a new tag ``devel-stable`` and move your device to this tag.

.. code-block::

   # Add the tag "devel-stable" to version 100
   $ fioctl targets tag --tags devel,devel-stable --by-version 100
   Changing tags of qemuarm64-secureboot-lmp-100 from [devel] -> [devel devel-stable]

   # Move the device "dev-1" to follow the tag "devel-stable"
   $ fioctl device config updates dev-1 --tags devel-stable
   Currently configured tag:
   Tag reported by device: devel
   Setting tag to devel-stable

As new ``devel`` Targets become available, ``dev-1`` continues on Target ``100``, as that is the latest Target available for the ``devel-stable`` tag.

* **Controlled Updates**

Similar to the previous example, you want a portion of your devices to avoid automatically consuming every ``devel`` build as they come from CI.
At this point, these devices listen to the ``devel-stable`` tag and are running Target ``100``.

A new Target ``110`` is ready for promotion.
The stable Targets are manually tagged with ``devel-stable``.

.. code-block::

   # Add the tag "devel-stable" to version 110
   $ fioctl targets tag --tags devel,devel-stable --by-version 110
   Changing tags of qemuarm64-secureboot-lmp-110 from [devel] -> [devel devel-stable]

This will cause the devices listening to the ``devel-stable`` Tag to update to Target ``110``.

As new ``devel`` Targets become available, the set of devices continue on Target ``110``, as that is the latest Target available for the ``devel-stable`` tag.

* **Using Test Devices**

The previous workflow can also be used for test devices.
Selected Targets are tagged for testing as ``devel-test``.

Additionally, these test devices could run a series of tests on this Target and report back as ``good`` or ``bad``.
This would then be used to add another tag to the Target: ``devel-test-good`` or ``devel-test-bad``.

* **Avoiding an Update**

Let's say there are two test devices: one is sitting in the lab and the other belongs to a developer.
The test devices update once a day as there is no requirement for frequent tests.

The developer who owns the test unit forces an update to their own device outside of the test cycle and identifies that the new update introduces a bug.

The user can then avoid that update on the lab device by removing the test tag from the bad Target.

.. code-block::

   # Remove the tag "devel-test" from version 110
   $ fioctl targets tag --tags devel --by-version 110
   Changing tags of qemuarm64-secureboot-lmp-110 from [devel devel-test] -> [devel]

   # Alternatively, mark that Target as bad with a specific tag
   $ fioctl targets tag --tags devel,devel-test-bad --by-version 110
   Changing tags of qemuarm64-secureboot-lmp-110 from [devel devel-test] -> [devel devel-test-bad]

The device in the lab stays on the previous Target, for example ``100``, as there is no newer Target available for the test tag.

* **Flagging a Pre-Production Target**

Another useful scenario is flagging Targets intended for production.
These Targets can be identified after successful tests, as release candidates or pre-production Targets.

Let's say Target ``100`` passed all tests successfully and it is ready to be delivered to your production fleet.
Target ``100`` can be flagged with the ``pre-production`` tag.

.. code-block::

   # Add the tag "pre-production" to version 100
   $ fioctl targets tag --tags devel,devel-stable,pre-production --by-version 100
   Changing tags of qemuarm64-secureboot-lmp-100 from [devel devel-stable] -> [devel devel-stable pre-production]

After that, listing the Targets by the ``pre-production`` tag provides the list of Targets to be released to production.

.. code-block::

   $ fioctl targets list --by-tag pre-production
   VERSION  TAGS                              APPS                                ORIGIN
   -------  ----                              ----                                ------
   100      devel,devel-stable,pre-production

This is convenient as a Factory Admin can rely on checking this tag to release Production Targets.

.. note::
   By default, updates can only move forward.
   This means that a device running Target ``100`` can update to Target ``110``, but the opposite is not possible after a successful update.

Advanced Tagging
""""""""""""""""

:ref:`ref-advanced-tagging` covers mix and matching platform and container builds, allowing elaborated development strategies.
Check the linked page for additional use cases.

.. seealso::
   :ref:`tutorial-working-with-tags`

Managing Devices
~~~~~~~~~~~~~~~~

Devices can be managed as a fleet, as a group or as a single unit.

Managing single devices is helpful during the development and testing phases, where developers usually handle their own devices.
However, as you move close to production, it is recommended to manage device groups instead.

A device group can be assigned to a team so that the access to its devices can be shared.
This allows granular control of user access to each device group.

A common use for device management is to set the device tag and applications.
As tagging is covered in the previous sections, here we show use cases for handling the applications:

* **Setting the App List**

By default, the device runs all apps available for its Target.
When this is not desired, a custom app list can be set.

.. code-block::

   # Setting the app list to "shellhttpd"
   $ fioctl devices config updates <device> --apps shellhttpd
   Currently configured apps: []
   Apps reported as installed on device: [shellhttpd,shellhttpd2]
   Setting apps to [shellhttpd]

* **Disabling All Apps**

All applications can be disabled from a device.
This helps, for example, when working on the platform code and there is no intention to interact with the apps.

.. code-block::

   # Removing all apps from the device
   $ fioctl devices config updates <device> --apps ,
   Currently configured apps: [shellhttpd]
   Apps reported as installed on device: [shellhttpd]
   Setting apps to []

* **Recovering the Target App List**

After a custom app list was set, it can be recovered so that the default apps from the Target can run on the device.

.. code-block::

   # Setting the apps list to Target defaults
   $ fioctl devices config updates <device> --apps -
   Currently configured apps: []
   Apps reported as installed on device: []
   Setting apps to system default.

.. seealso::
   :ref:`ref-configuring-devices`

   :ref:`Access to Device Groups`

Production Best Practices
-------------------------

When talking about production workflows, you first need to define which Target to release to production.

As discussed, it is possible to flag ``pre-production`` Targets to be later moved into production, but this is a convenience rather than a requirement.
Any CI Target can be promoted to production.

:ref:`Waves <ref-waves-ug>` are used to promote CI Targets into Production Targets.
Production devices only update to Production Targets.
A Production Target is signed twice: once by FoundriesFactory CI (as normal CI Targets), and once by the customer, using the :ref:`Offline TUF Targets key <ref-offline-targets-keys>`.

By requiring additional signing, Waves control what is delivered to your production devices.
By using offline keys owned by the customer, Waves limit which users can perform this action.
The combination of these factors makes Waves a robust way of managing your production fleet.

Waves also allows you to control how the update is delivered to your fleet.
You can roll out the delivery by device groups, by device UUID or by a randomized number of devices in your fleet.

For production releases, see the workflows documented at :ref:`ref-ug-production-workflow` and :ref:`ref-rm-prod-target-adv`.

.. note::
   It is worth noting that production devices also follow tags, as normal development devices.

   The name spaces for CI and Production Targets are separate: tags created via the Waves interface does not associate with the CI name space nor does the CI tags interact with the Waves name space.

.. _`What's a Target`: https://foundries.io/insights/blog/whats-a-target/
