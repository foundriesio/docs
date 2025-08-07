.. _ref-waves-ug:

Waves and Production Targets
============================

Waves is the FoundriesFactory mechanism to promote and deliver updates to :ref:`production devices <ref-production-registration>`.
It allows deciding which updates are promoted to production, with granular control of how the updates are delivered across the field.
It also provides additional security as only Factory Owners and Admins in possession of TUF targets keys are allowed perform these actions.

Suggested Flow
--------------

When devices are registered to production, they only update to :ref:`ref-production-targets`.

Below you can find the standard flow to promote a target to a Production Target using Waves (``fioctl waves``).

.. note::
   This process can only be performed by Factory Owners and Admins owning the :ref:`Offline TUF Targets keys <ref-offline-targets-keys>`.

.. image:: /_static/user-guide/waves/waves-flow.png
   :width: 400
   :align: center
   :alt: Waves subcommands suggested flow

Waves Init
~~~~~~~~~~

  * Starts a new Wave on the selected Target.
  * No updates delivered at this point.
  * Wave Status: ``Active``.

.. code-block:: console

   $ fioctl waves init -k ~/path/to/keys/targets.only.key.tgz <wave> <target-number> <tag>

Waves Rollout
~~~~~~~~~~~~~

  * Delivers the update to a subset of the fleet (device groups, specific devices by UUID, percentage of the fleet).
  * Multiple rollout commands can be issued for a single wave.
  * Different wave rollouts can happen in parallel.
  * Optional stage, but recommended for controlled deployment of the production update.
  * Options for granular control are available at this stage, please check command helper and :ref:`ref-production-targets`.
  * Wave Status: ``Active``.

.. code-block:: console

   $ fioctl waves rollout <wave> [flags]

Waves Complete
~~~~~~~~~~~~~~

  * Delivers the update to all production devices following this wave tag.
  * Only after Wave Complete, this Target becomes a Production Target.
  * Wave Status: ``Complete``.

.. code-block:: console

   $ fioctl waves complete <wave>

Waves Cancel
~~~~~~~~~~~~

  * Cancels an active wave.
  * Devices that updated prior to Waves Cancel stays in the updated version.
  * This Target does not become a Production Target.
  * Wave Status: ``Canceled``.

.. code-block:: console

   $ fioctl waves cancel <wave>

Waves Status Summary
~~~~~~~~~~~~~~~~~~~~

.. tip::
   Wave Status can be checked with ``fioctl waves list`` or in the ``Waves`` tab of the Factory.

Below is a summary of Waves and Production Targets status at each wave stage:

.. list-table:: Waves x Production Targets
   :header-rows: 1
   :align: center

   * - Wave Stage
     - Wave Status
     - Production Target
   * - Init
     - Active
     - No
   * - Rollout
     - Active
     - No
   * - Complete
     - Complete
     - Yes
   * - Cancel
     - Canceled
     - No

Waves Considerations
--------------------

* For production manufacturing, we recommend using only Production Targets.
  The assumption is that these are the production quality Targets.

  * Targets become Production Targets after the Wave Complete step.

  * You can get the list of Production Targets with:

  .. code-block:: console

     $ fioctl targets list --production --by-tag <tag>

* You may create as many waves as you need for your release strategy.
  But, there may be only one active wave per device tag at a time.
  If you need to roll out more than one wave to one tag, either complete or cancel a previous wave to that tag.

* The Wave Rollout step can be skipped by initializing and completing the wave.
  This delivers the update across all fleet at once.

* Tags in :ref:`ref-ci-targets` do not conflict with tags in Production Targets.

  * This means that both CI and Production Targets can have the same tag and not impact the other class of devices.
    For example, a production device following the ``release`` tag does not update to a CI Target tagged with ``release`` and vice-versa.

* Up to LmP v95, unexpected downgrades can happen during :ref:`TUF keys rotation <ref-offline-keys>` in case there are devices running on Canceled Waves.

  * During the TUF keys rotation, the TUF root metadata is refreshed, causing the devices to receive a fresh version of the targets list.
    As a Canceled Wave does not produce a Production Target, devices running on this Wave will update to the last Complete Wave, causing a downgrade.
    This is expected in terms of the TUF specification.

  * Starting with v95, downgrades are forbidden by default.

  * To avoid this behavior in previous LmP versions, complete a wave for the impacted devices prior to the rotation.

* It is not possible to Cancel a Wave after it has been Completed, but its Target can be removed from the Production Targets list by pruning it.
  To achieve this, Init then Complete a new Wave for this particular Tag with the `--prune <target-number>` parameter:

.. code-block:: console

   $ fioctl waves init -k ~/path/to/keys/targets.only.key.tgz <new-wave> <target-number> <tag> --prune <target-to-prune>
   $ fioctl waves complete <new-wave>

Production Workflow
-------------------

Assuming your production fleet is separated into device groups, where ``canary`` is a small device group for testing purposes.
Here we show a simplified overview of Waves usage in production:

* Production devices are registered to follow a unique tag, for example ``release``.

* When a new release is available, a new wave is created for the ``release`` tag.

* Rollout this wave for the ``canary`` device group and observe the update results.

  * If anything goes wrong with this update, you can cancel the wave at this point.

  * It is up to you to define the acceptance criteria for the update.

* New rollouts to device groups or particular devices can be performed at this stage.

* The wave should be completed when you wish to deliver the update to all devices on the fleet following this tag.

With this use case, devices update as soon as this new wave is completed or rolled out to their device group.

.. tip::
   For advanced use cases and more granular control of your fleet, check :ref:`Production Targets Advanced Usage<ref-rm-prod-target-adv>`.
