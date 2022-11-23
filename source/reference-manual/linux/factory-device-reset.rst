.. _ref-factory-device-reset:

Factory Reset
=============

In this context, factory reset means restoring the device to the original state.
This is a feature of LmP rather than FoundriesFactory.
Reset is performed as a script in ramdisk during boot.
It is triggered by presence of specific files.
Presence of the files is specified in the following order:

#. ``/var/.factory_reset``
#. ``/var/.factory_reset_keep_sota``
#. ``/var/.factory_reset_keep_sota_docker``

Each file has specific meaning.
When a higher priority file is detected, remaining files are ignored.

Full factory reset
------------------

When the file ``/var/.factory_reset`` is present, the script performs full reset.
Full reset means restoring contents of ``/etc/`` and ``/var/`` from :ref:`ostree<ref-static-deltas>`.
All contents created in these directories at runtime will be erased.

Partial factory reset
---------------------

There are currently two options in partial reset.

Keep SOTA
~~~~~~~~~

When the file ``/var/.factory_reset_keep_sota`` is present,
contents of ``/etc/`` are restored from ostree.
Contents of ``/var/`` are partially removed.
``/var/sota/`` contents are kept to allow aktualizr-lite to be preserved.
Docker images and compose apps are deleted.

Keep SOTA and docker
~~~~~~~~~~~~~~~~~~~~

When the file ``/var/.factory_reset_keep_sota_docker`` is present,
contents of ``/etc/`` are restored from ostree.
Contents of ``/var/`` are partially removed.
``/var/sota/`` contents are kept to allow aktualizr-lite and
compose-apps to be preserved.
``/var/lib/`` is preserved as the docker objects are stored there.
