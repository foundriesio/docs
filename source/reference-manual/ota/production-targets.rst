.. _ref-production-targets:

Production Targets
==================

As noted in the :ref:`offline keys documentation<ref-offline-keys>`,
production devices receive a slightly different copy of the TUF
targets metadata. This production copy must be signed with both
the Foundries.io targets signing key and the Factory's offline targets
signing key.

Production targets are managed by using Waves. Normally, when the
TUF targets metadata is updated, all devices see it and can start
updating themselves. Waves are a feature that allow Factory operators
to control the rate at which devices see a new copy of the TUF targets
metadata.

Before a Factory can start doing production OTAs, an initial production
Targets file must be created. This can be done by creating a dummy wave
like::

  # fioctl wave init <wave-name> <target number> <tag>
  fioctl wave init -k /absolute/path/to/targets.only.key.tgz populate-targets 12 production
  fioctl wave  complete populate-targets

This creates a new ``targets.json`` file for production devices subscribing
to the ``production`` tag. It will include a single Target from CI
build. In this example, build 12.

.. _ref-rm-wave:

Performing a production OTA
---------------------------

Continuing from the example above. A Factory may go through some
development work and have a new CI build #42 that's ready to be run in
production. A wave can be initialized with::

  fioctl wave init -k /absolute/path/to/targets.only.key.tgz v2.0-update 42 production

.. note::

   Operators will want to generate
   :ref:`OSTree static deltas<ref-static-deltas>` before rolling
   out waves to devices.

A new wave is ready to share with device groups. A Factory might have a
device group called "canary". Those devices can be moved to this new
update with::

  fioctl waves rollout v2.0-update canary

At this point, an operator can monitor the status of the OTA via
``fioctl status``. If the update goes badly they can cancel the wave
with::

  fioctl waves cancel v2.0-update

The devices that were successfully updated to Target 42 will continue to
run it. However, all other production devices on the ``production`` tag
will continue to run Target 12.

Assuming the first wave to the ``canary`` device-group succeeded, an
operator can roll out to more devices. For example a device-group named
``us-east-1``::

  fioctl waves rollout v2.0-update us-east-1

Eventually the operator can update the primary ``targets.json`` file for all
devices on the ``production`` tag with::

  fioctl waves complete v2.0-update

.. note::

   When flashing new production devices, it is recommended to only use promoted
   production targets.
