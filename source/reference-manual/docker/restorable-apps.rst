.. _ug-restorable-apps:

Restorable Apps
===============

Restorable Apps are Compose Apps that can be restored in case of any Docker store damages, without needing to be re-downloaded from the Registry.
This is achieved by a distinct way images can pulled and stored on a device.

#. Images are pulled from registries by the `skopeo <https://github.com/containers/skopeo>`_ utility,
   rather than pulling them by utilizing the Docker daemon's regular functionality normally used for Compose Apps;
#. Images are stored in two places on a device.
   In addition to the regular Docker daemon's image store (``/var/lib/docker/image/overlay2`` and ``/var/lib/overlay2``),
   images are also stored in the folder defined in the ``aktualizr-lite`` config file.
   This defaults to ``/var/sota/reset-apps``.
   The additional store path can be overridden in the ``*.toml`` config file by defining a value of ``[pacman].reset_apps_root``.

Image layers are stored in the additional store in ``tar.gzip`` format.
This helps to reduce the device storage cost of this feature.
Effectively, the difference in the Docker store size and the Restorable Apps' additional storage size is equivalent to the compression ratio of ``gzip``.

Employment of Restorable Apps
-----------------------------

Primarily, Restorable Apps are employed to:

#. Support "Factory Reset" feature;
#. Provide means to restore a Docker daemon's store if it gets broken.

Both cases imply that a desired state of Apps can be restored—even if a Docker daemon's store (``/var/lib/docker``) is deleted or broken—without needing to re-download images.
Effectively, images are injected from the additional storage to the store in such cases.

Restorable Apps are enabled by default.
The list of Restorable Apps is equal to the list of Apps enabled on a device (if defined, the value of ``compose_apps``, otherwise all Target Apps).
You may extend the default list of Restorable Apps in the following ways:

#. For **manual** registration, by invoking lmp-device-register_ with ``‑‑restorable‑apps <comma‑separated app list>``.
#. For **auto** registration, using ``--restorable-apps <comma-separated app list>`` with lmp-device-auto-register_.
#. By setting ``reset_apps=<a comma-separated list of apps>`` in ``[pacman].reset_apps`` for a device/aklite config.
   You may change the given configuration for a specific device, a device group, or all devices (see :ref:`ref-configuring-devices` for details).

To disable Restorable Apps, specify an empty string ``""`` as the value of ``<a comma-separated list of apps>`` in one of the previous options.
For example, ``lmp-device-register --restorable-apps ""``.

.. seealso::
   :ref:`ug-lmp-device-auto-register`


.. _lmp-device-register: https://github.com/foundriesio/lmp-device-register
.. _lmp-device-auto-register: https://github.com/foundriesio/meta-lmp/tree/main/meta-lmp-base/recipes-support/lmp-device-auto-register
