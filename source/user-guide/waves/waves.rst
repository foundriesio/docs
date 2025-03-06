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

.. image:: /_static/userguide/waves/waves-flow.png
   :width: 400
   :align: center
   :alt: Waves subcommands suggested flow

Waves Init (``fioctl waves init``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  * Starts a new Wave on the wanted Target.
  * No updates delivered at this point.
  * Wave Status: ``Active``.

Waves Rollout (``fioctl waves rollout``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  * Delivers the update to a specific device group.
  * Multiple rollout commands can be issued for a single wave.
  * Different wave rollouts can happen in parallel.
  * Optional stage, but recommended.
  * Options for granular control are available at this stage, please check command helper and :ref:`ref-production-targets`.
  * Wave Status: ``Active``.

Waves Complete (``fioctl waves complete``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  * Delivers the update to all production devices following this wave tag.
  * Only after Wave Complete, this Target becomes a Production Target.
  * Wave Status: ``Complete``.

Waves Cancel (``fioctl waves cancel``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  * Cancels an active wave.
  * Devices that updated prior to Waves Cancel stays in the updated version.
  * This Target does not become a Production Target.
  * Wave Status: ``Canceled``.

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

* For production manufacturing, we recommend using only Production Targets. The assumption is that these are the production quality Targets.

  * Targets become Production Targets after the Wave Complete step.

  * You can get the list of Production Targets with:

  .. code-block::

     fioctl targets list --production --by-tag <tag>

* You may create as many waves as you need for your release strategy. But, there may be only one active wave per device tag at a time. If you need to roll out more than one wave to one tag, either complete or cancel a previous wave to that tag.

* The Wave Rollout step can be skipped by initializing and completing the wave. This delivers the update across all fleet at once.

* Tags in :ref:`ref-ci-targets` do not conflict with tags in Production Targets.

  * This means that both CI and Production Targets can have the same tag and not impact the other class of devices. For example, a production device following the ``release`` tag does not update to a CI Target tagged with ``release`` and vice-versa.

* Up to LmP v95, unexpected downgrades can happen during :ref:`TUF keys rotation <ref-offline-keys>` in case there are devices running on Canceled Waves.

  * During the TUF keys rotation, the TUF metadata is refreshed, causing the devices to receive a fresh version of the targets list. As a Canceled Wave does not produce a Production Target, devices running on this Wave will update to the last Complete Wave, causing a downgrade. This is expected in terms of the TUF specification.

  * Starting with v95, downgrades are forbidden by default.

  * To avoid this behavior in previous LmP versions, complete a wave for the impacted devices prior to the rotation.

Production Workflow
-------------------

The production workflow and release strategy depend on each use case. Here, we present two approaches for simplified usage.

Keeping the Same Tag
~~~~~~~~~~~~~~~~~~~~

This approach benefits use cases where the whole fleet is expected to be in the same software version.

* Production devices follow a unique general tag, for example ``production``, throughout the entire life cycle.

* When a new release is available, a new wave is created for the ``production`` tag.

* Devices update as soon as this new wave is completed or rolled out to their device group.

Creating New Release Tag
~~~~~~~~~~~~~~~~~~~~~~~~

This approach allows granular controls of the fleet and software versions. It is possible to have multiple stable releases for different usage and versions of the product.

* Production devices follow a release tag, for example ``v1.0``.

* When a new release is available, a new wave is created for the new release tag, for example ``v1.1``.

* Device groups are configured to follow the new release tag, for example for a particular device group:

.. code-block::

   fioctl config updates -g <device-group> --tag v1.1

* Devices following the new tag update as soon as this new wave is completed or rolled out to their device group.

.. tip::
   For advanced use cases, check :ref:`Production Targets Advanced Usage<ref-rm-prod-target-adv>`.
