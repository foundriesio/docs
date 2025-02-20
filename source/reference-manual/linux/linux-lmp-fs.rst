.. _ref-linux-lmp-fs:

LmP File Structure
==================

LmP uses the `OSTree`_ upgrade system to cover platform updates.
This brings a modified file system structure, which is detailed on this page.
Also covered here are some related tips about LmP structure, and OTA behavior.

OSTree File System Structure
----------------------------

.. prompt::

   # ls -l /
   total 17
   lrwxrwxrwx   2 root root    7 Jul 31 22:32 bin -> usr/bin
   drwxr-xr-x   5 root root 1024 Aug  1 15:44 boot
   drwxr-xr-x  12 root root 3340 Aug  2 17:17 dev
   drwxr-xr-x  39 root root 4096 Aug  1 15:46 etc
   lrwxrwxrwx   2 root root   17 Jul 31 22:32 home -> var/rootdirs/home
   lrwxrwxrwx   2 root root    7 Jul 31 22:32 lib -> usr/lib
   lrwxrwxrwx   2 root root   18 Jul 31 22:32 media -> var/rootdirs/media
   lrwxrwxrwx   2 root root   16 Jul 31 22:32 mnt -> var/rootdirs/mnt
   lrwxrwxrwx   2 root root   16 Jul 31 22:32 opt -> var/rootdirs/opt
   lrwxrwxrwx   2 root root   14 Jul 31 22:32 ostree -> sysroot/ostree
   dr-xr-xr-x 148 root root    0 Aug  2 17:16 proc
   lrwxrwxrwx   2 root root   12 Jul 31 22:32 root -> var/roothome
   drwxrwxrwt  20 root root  540 Aug  2 17:17 run
   lrwxrwxrwx   2 root root    8 Jul 31 22:32 sbin -> usr/sbin
   lrwxrwxrwx   2 root root   16 Jul 31 22:32 srv -> var/rootdirs/srv
   dr-xr-xr-x  12 root root    0 Aug  2 17:16 sys
   drwxr-xr-x   5 root root 4096 Jul 31 22:34 sysroot
   drwxrwxrwt   7 root root  140 Aug  2 17:17 tmp
   drwxr-xr-x  12 root root 4096 Jan  1  1970 usr
   drwxr-xr-x  13 root root 4096 Aug  1 15:46 var

OSTree brings a **read-only** file system, where the disk partition is ``/sysroot``.
The root that mounted at ``/`` (as above) is ``/sysroot/ostree/deploy/lmp/deploy/<sha>``.

.. warning::
   Some folders should not be manipulated in order to ensure proper behavior of OTA.
   The ``/usr`` path is an example of a critical folder that is mounted as read-only and should not be touched—this is handled by the LmP OTA.

Persistent Storage
------------------

These folders are treated like persistent storage on the device and have particularities with regards to updates:

* ``/var``

   * Main persistent storage, writable directory.

   * Most important files are located under ``/var`` (see :ref:`ref-linux-lmp-fs-important-files`).

   * Not covered by OTA.

* ``/etc``

   * Covered by OTA if untouched.

   * As soon as OSTree detects a change in this directory, it performs a 3-way merge using the old default configuration, the active system's ``/etc``, and the new default configuration.
     This is then no longer covered by OTA.

   * For the reason above, we do not recommend nor support setting system configurations in this directory. It is more reliable to set critical configurations under ``/usr/lib`` as that is always covered by OTA.

.. _ref-linux-lmp-fs-important-files:

Important Files and Folders
---------------------------

* ``/var/sota``: Stores critical OTA files.

.. prompt::

   # ls -l /var/sota/
   total 208
   -rw-r--r-- 1 root root    692 Aug  1 15:41 client.pem
   drwxr-xr-x 3 root root   4096 Aug  1 15:44 compose-apps
   -rw-r--r-- 1 root root    265 Aug  1 15:49 current-target
   drwxr-xr-x 2 root root   4096 Aug  1 15:41 import
   -rw-r--r-- 1 root root    227 Aug  1 15:41 pkey.pem
   drwxr-xr-x 4 root root   4096 Aug  1 15:42 reset-apps
   -rw-r--r-- 1 root root    668 Aug  1 15:41 root.crt
   -rw-r--r-- 1 root root    885 Aug  1 15:41 sota.toml
   -rw-r--r-- 1 root root 180224 Aug  1 15:49 sql.db

``/var/sota/sota.toml``: Stores relevant OTA information, like Tag, Apps, custom configurations, certificates location and server address.

``/var/sota/reset-apps``: Holds preloaded apps if :ref:`ug-restorable-apps` are used (default since LmP **v85**).

``/var/sota/compose-apps``: Apps are extracted to this location during app loading.
It holds preloaded apps if Compose Apps are used.

``/var/sota/current-target``: Brings valuable information about the current Target running on the device, including LmP and containers information.
This is populated after the first OTA.

.. prompt::

   # cat /var/sota/current-target  
   TARGET_NAME="qemuarm64-secureboot-lmp-116"
   CUSTOM_VERSION="<target>"
   LMP_MANIFEST_SHA="9f288aba55d140786360a71f773a098d1aa0a4fd"
   META_SUBSCRIBER_OVERRIDES_SHA="dfd11d7e00db24641bd88c2d9d680c38ba5fdf19"
   CONTAINERS_SHA="459e19cde44e17b17054b0cd972f0520cd214f58"
   TAG="<tag>"

``/var/sota/sql.db``: Device registration database.

``/var/sota/client.pem``, ``/var/sota/pkey.pem``, and ``/var/sota/root.crt``: Device registration certificates.
If available, ``client.pem`` and ``pkey.pem`` can be stored in an HSM rather than on files.

* ``/var/lib/docker``: Stores Docker images and containers.

* ``/var/rootdirs/home/fio/``: Home directory.

* ``/etc/os-release``: Provides LmP information, including platform Target number, Tag, and release.
  It does not include information on Target containers.

.. prompt::

   # cat /etc/os-release 
   ID=lmp
   NAME="Linux-microPlatform"
   VERSION="4.0.11-116-91"
   VERSION_ID=4.0.11-116-91
   PRETTY_NAME="Linux-microPlatform 4.0.11-116-91"
   HOME_URL="https://foundries.io/"
   SUPPORT_URL="https://support.foundries.io/"
   DEFAULT_HOSTNAME="qemuarm64-secureboot"
   LMP_MACHINE="qemuarm64-secureboot"
   LMP_FACTORY="<factory-name>"
   LMP_FACTORY_TAG="<tag>"
   IMAGE_ID=lmp-factory-image
   IMAGE_VERSION=<os-target>

.. hint::
   Version information reads as ``VERSION=<Yocto Project version> - <Target number> - <LmP release tag>``


Tips and Suggestions
--------------------

* A :ref:`systemd service <ref-troubleshooting_systemd-service>` can be used if case a file in a directory not covered by OTA needs to be updated.

* It is recommended to store custom user files under ``/var/local``.
  Keep any custom files location in mind when implementing a :ref:`ref-factory-device-reset`.

* The full initial Target information (includes containers and LmP) just after the provisioning of a device can be checked with:

.. prompt::

   # cat /var/sota/import/installed_versions | grep "\"version\""
      "version": "102",

After the first OTA, it can be read in ``/var/sota/current-target`` as discussed previously.

* If enabling :ref:`ref-linux-persistent-log`, ``/var/log`` is used to store system logs.
  It is recommended to mount it in an additional storage so it does not take valuable internal storage space which could impact the OTA behavior.

.. _OSTree: https://ostreedev.github.io/ostree/introduction/
