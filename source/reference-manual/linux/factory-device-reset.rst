.. _ref-factory-device-reset:

Factory Reset
=============

In this context, Factory reset means restoring a device to the original state.
This is a feature of LmP, rather than of the FoundriesFactory™ Platform.
A reset is performed as a script in ramdisk during boot.
It is triggered by the presence of specific files.
Presence of the files is specified in the following order:

#. ``/var/.factory_reset``
#. ``/var/.factory_reset_keep_sota``
#. ``/var/.factory_reset_keep_sota_docker``

Each file has specific meaning.
When a higher priority file is detected, remaining files are ignored.

Full Factory Reset
------------------

When the file ``/var/.factory_reset`` is present, the script performs a full reset.
A full reset means restoring contents of ``/etc/`` and ``/var/`` from :ref:`ostree<ref-static-deltas>`.
All contents created in these directories at runtime will be erased.

Partial Factory Reset
---------------------

There are currently two options in partial reset.
The main difference with full reset is that the device remains connected to your Factory.

Keep SOTA
~~~~~~~~~

When the file ``/var/.factory_reset_keep_sota`` is present,
contents of ``/etc/`` are restored from ostree.
Contents of ``/var/`` are partially removed.
``/var/sota/`` contents are kept to allow aktualizr-lite to be preserved.
Docker images and compose apps are deleted.

Keep SOTA and Docker
~~~~~~~~~~~~~~~~~~~~

When the file ``/var/.factory_reset_keep_sota_docker`` is present,
contents of ``/etc/`` are restored from ostree.
Contents of ``/var/`` are partially removed.
``/var/sota/`` contents are kept to allow aktualizr-lite and
compose-apps to be preserved.
``/var/lib/`` is preserved as the Docker objects are stored there.

