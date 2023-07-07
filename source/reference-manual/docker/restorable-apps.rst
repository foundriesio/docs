.. _ug-restorable-apps:

Restorable Apps
===============

Restorable Apps are Compose Apps that have capability to be restored in a case of any docker store damages without a need to be re-downloaded from Registry.
It's achieved by the distinct way images are pulled and stored on a device.

#. Images are pulled from Registries by `skopeo <https://github.com/containers/skopeo>`_ utility, unlike pulling them by utilizing of the docker's/docker daemon's regular functionality in the case of Compose Apps;
#. Images are stored in two places on a device. In addition to the regular docker daemon's image store (``/var/lib/docker/image/overlay2`` and ``/var/lib/overlay2``),
   images are also stored in the folder defined in the ``aktualizr-lite`` config. By default, it's set to ``/var/sota/reset-apps``.
   The additional store path can be overridden in the ``*.toml`` configuration file by defining a value of ``[pacman].reset_apps_root`` configuration variable.

Image layers are stored in the additional store in ``tar.gzip`` format. This helps to reduce the device storage cost of this feature.
Effectively, the difference in the docker store size and the Restorable Apps' additional storage size is equivalent to the compression ratio of ``gzip``.

Primarily, Restorable Apps are employed to:
-------------------------------------------

#. support "Factory Reset" feature;
#. provide means to restore a docker daemon's store if it gets broken.

Both cases implies that a desired state of Apps (effectively a docker daemon store's state) can be restored even if
a docker daemon's store (``/var/lib/docker``) is deleted or partially broken without a need to re-download images from remote Registries.
Effectively, images are injected from the additional storage to the store in such cases.

Restorable Apps are enabled by default, and a list of Restorable Apps is equal to a list of Apps enabled on a device (a value of ``compose_apps`` parameter if defined or all Target Apps).
A user may extend the default list of Restorable Apps in the following ways:

#. By invoking of lmp-device-auto-register_ utility with the ``--restorable-apps <a comma-separated list of apps>`` option during manual device registration.
#. If a device auto registration is configured for a factory, then by adding the ``--restorable-apps <a comma-separated list of apps>`` option to the lmp-device-auto-register_ script.
   See :ref:`ug-lmp-device-auto-register` for more details.
#. By setting ``reset_apps=<a comma-separated list of apps>`` value in ``[pacman].reset_apps`` of a device/aklite config.
   A user may change the given configuration for a specific device, a device group or all factory devices (see :ref:`ref-configuring-devices` for details).

To disable Restorable Apps, a user should specify an empty string ``""`` as a value of ``<a comma-separated list of apps>`` in one of the previous options (e.g. ``lmp-device-register --restorable-apps ""``).

.. _lmp-device-auto-register: https://github.com/foundriesio/meta-lmp/tree/main/meta-lmp-base/recipes-support/lmp-device-auto-register
