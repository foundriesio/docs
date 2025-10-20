.. _lmp-customization:

LmP Customization
=================

This page covers common ways to modify the Linux® microPlatform (LmP).
This includes kernel options, startup services, user and group configuration, and other options related to the platform build. 

.. seealso::

   The tutorial for :ref:`tutorial-customizing-the-platform` covers adding a custom recipe service.
   This is a good place to start, as it introduces concepts and steps related to customizing LmP.

.. _ref-customizing-the-distro:

Customizing the Distro
-----------------------

This section shows how to build new Targets with a different distro.
The following is an example on how to build a new Target with :ref:`LmP XWayland <ref-lmp-wayland-xwayland>`.

1. Update your factory config:

   .. code-block:: console

      $ git clone https://source.foundries.io/factories/<factory>/ci-scripts.git
      $ cd ci-scripts
      $ vi factory-config.yml

2. Add the distro under ``LmP``:

   .. code-block:: yaml

       worker_tag: "amd64-partner-aws"
       params:
          IMAGE: lmp-factory-image
          DOCKER_COMPOSE_APP: "1"
          DISTRO: "lmp-xwayland"

3. Commit and push the changes:

   .. code-block:: console

       $ git add .
       # git commit -m "Adding lmp-xwayland as base for my factory"
       # git push

4. Changes to the ``ci-script`` repository do not auto-trigger builds.
   To do so, push a commit in ``lmp-manifest`` or ``meta-subscriber-overrides``:

   .. code-block:: console

       $ git clone https://source.foundries.io/factories/<factory>/lmp-manifest.git
       $ cd lmp-manifest
       $ git commit -m "trigger build" --allow-empty

Kernel Command Line Arguments
-----------------------------

The method of modifying kernel command line arguments differs between what LmP distro you have set.
The two options available are ``lmp``  (default) and ``lmp-base``.

See the :ref:`ref-linux-distro` page for an overview of the two options.

Distro: ``lmp``
^^^^^^^^^^^^^^^

Extend the kernel command line by setting ``OSTREE_KERNEL_ARGS`` in ``meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc``::

    OSTREE_KERNEL_ARGS:<machine> = "console=${console} <new-args> ${OSTREE_KERNEL_ARGS_COMMON}"

Make sure you set the correct ``<machine>`` and other variables as needed.

.. note::

    The default is ``OSTREE_KERNEL_ARGS_COMMON ?= "root=LABEL=otaroot rootfstype=ext4"``.
    This variable sets a valid ``root`` label for the device.
    It is not necessary on devices specifying the partition path directly with ``root=``.

Distro: ``lmp-base``
^^^^^^^^^^^^^^^^^^^^

Extend the kernel command line by appending your commands to ``bootcmd_args`` in ``meta-subscriber-overrides/recipes-bsp/u-boot/u-boot-base-scr/<machine>/uEnv.txt.in``.
For example::

    bootcmd_args=setenv bootargs console=tty1 console=${console} root=/dev/mmcblk2p2 rootfstype=ext4 rootwait rw <new-args>

Create ``meta-subscriber-overrides/recipes-bsp/u-boot/u-boot-base-scr.bbappend`` with the following content to include your source file::

    FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

.. note::
    If testing a board supported in ``meta-lmp``, the default ``uEnv.txt.in`` can be found in ``meta-lmp/meta-lmp-bsp/recipes-bsp/u-boot/u-boot-base-scr/<machine>/uEnv.txt.in``.

Automatically Loading a Kernel Module
-------------------------------------

Configure to only load a natively supported kernel module, such as ``i2c-dev``, by adding the following change in ``conf/machine/include/lmp-factory-custom.inc``::

    KERNEL_MODULE_AUTOLOAD:<machine> = "i2c-dev"

.. _ref-troubleshooting_systemd-service:

Adding a new Systemd Startup Service
-------------------------------------

LmP uses `systemd <https://systemd.io/>`_ for service management.
The tutorial on :ref:`tutorial-customizing-the-platform` provides a detailed walk-through of the steps required for adding a systemd service.
A summarized example for adding a shell script to run at startup is provided below for quick reference.
You should first be familiar with editing the ``meta-subscribers-overrides`` layer.

.. important::

    Make sure to replace ``<service-name>`` accordingly throughout the instructions below.

#. Create a directory for your service in ``meta-subscriber-overrides`` repo:

   .. code-block:: console

      $ mkdir -p recipes-support/<service-name>

#. Add a new file named ``<service-name>.bb`` under this directory, with the following content::

    SUMMARY = "Description of your service"
    LICENSE = "MIT"
    LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

    inherit allarch systemd

    SRC_URI = " \
	    file://<service-name>.service \
	    file://<service-name>.sh \
    "

    S = "${WORKDIR}"

    PACKAGE_ARCH = "${MACHINE_ARCH}"

    SYSTEMD_SERVICE:${PN} = "<service-name>.service"
    SYSTEMD_AUTO_ENABLE:${PN} = "enable"

    do_install () {
	    install -d ${D}${bindir}
	    install -m 0755 ${WORKDIR}/<service-name>.sh ${D}${bindir}/<service-name>.sh

	    install -d ${D}${systemd_system_unitdir}
	    install -m 0644 ${WORKDIR}/<service-name>.service ${D}${systemd_system_unitdir}
    }

    FILES:${PN} += "${systemd_system_unitdir}/<service-name>.service"
    FILES:${PN} += "${systemd_unitdir}/system-preset"

#. Create another directory with the same name as the one we just created to place the source file(s) for the recipe::

    recipes-support/<service-name>/<service-name>

#. Create the systemd service file ``<service-name>.service`` under this new directory, configuring it to meet your needs:

   .. code-block:: systemd

      [Unit]
      Description=A description of your service
      After=rc-local.service

      [Service]
      Type=oneshot
      LimitNOFILE=1024
      ExecStart=/usr/bin/<service-name>.sh
      RemainAfterExit=true
      Environment=HOME=/home/root

#. Add the ``<service-name>.sh`` script to run at startup under this new directory

   .. code-block:: shell

      #!/bin/sh
      #
      # SPDX-License-Identifier: Apache 2.0
      #
      # Copyright (c) 2021, Foundries.io Ltd.

      # NOTE: This script will always exit with 0 result as other services
      # are dependent on it.

      # break on errors
      set -e

      echo "Hello World"
      exit 0

   .. note::
       If testing script locally, remember to make it executable.

#. Remember to install the new service by appending the ``CORE_IMAGE_BASE_INSTALL`` variable in ``lmp-factory-image.bb``::

    CORE_IMAGE_BASE_INSTALL += " \
    <service-name> \
    "

#. Lastly, check that the service is starting. From the device:

   ``systemctl status <service-name>.service``

Setting a Static IP on the Device
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While this example shows how to configure the ``eth1`` interface, the steps can be extended for other net interfaces.

#. First, create the .bbappend file, ``recipes-connectivity/networkmanager/networkmanager_%.bbappend``::

    FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

    SRC_URI:append = " \
        file://eth1.nmconnection \
    "

    do_install:append () {
        install -d ${D}${sysconfdir}/NetworkManager/system-connections
        install -m 0600 ${WORKDIR}/eth1.nmconnection ${D}${sysconfdir}/NetworkManager/system-connections

#. Now add the configuration fragment in ``recipes-connectivity/networkmanager/networkmanager/eth1.nmconnection``
   
   .. code-block:: none

    [connection]
    id=Wired connection 1
    uuid=7a0a09e1-6a0e-449f-9d51-9f48ba411edf
    type=ethernet
    autoconnect-priority=-999
    interface-name=eth1

    [ipv4]
    address1=<static-ip>/24,<gateway-address>
    method=manual

    [ipv6]
    addr-gen-mode=stable-privacy
    method=auto

.. important::
   Remember to adjust the `address1` parameter as needed.


LmP Users and Groups
--------------------

Users and groups can be added and configured prior to building an image.

.. tip::
   Default LmP group and password tables can be found in ``meta-lmp/meta-lmp-base/files``.
   This includes ``lmp-passwd-table``, ``lmp-group-table``, and for the default user,
   ``lmp-passwd-table-default`` and ``lmp-group-default``.

.. _ref-troubleshooting_user-groups:

Extending User Groups
^^^^^^^^^^^^^^^^^^^^^

To define a new user group in a Factory:

1. Define a custom group table in ``meta-subscriber-overrides/files/custom-group-table`` with the wanted user groups with ``<username>:x:<user-id>``.
   For example:

   .. code-block:: none

      systemd-coredump:x:998:

2. Define a custom passwd table in ``meta-subscriber-overrides/files/custom-passwd-table`` for the new user group: ``<username>:x:<user-id>:<group-id>::<home-dir>:<command>``.
   For example:

   .. code-block:: none

       systemd-coredump:x:998:998::/:/sbin/nologin

   .. note::
       This example works for system groups and system users (``user-id`` less than ``1000``).
       For normal users, check :ref:`ref-troubleshooting_lmp-user`.

   .. important::
       Platform build errors like below are fixed after extending the user group:
       ``normal groupname `<group>` does not have a static ID defined.``

3. Add these files to the build in ``meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc``:

   .. code-block:: none

       USERADD_GID_TABLES += "files/custom-group-table"
       USERADD_UID_TABLES += "files/custom-passwd-table"

.. _ref-troubleshooting_lmp-user:

Adding New LmP Users
^^^^^^^^^^^^^^^^^^^^

#. To create a new LmP user, first add the new user to the system.
   The steps are similar to the ones described in :ref:`ref-troubleshooting_user-groups`.
   Normal users need a valid shell and ``user-id`` **higher** than ``1000``.
   For example:
   
   **group-table:**

   .. code-block:: none
  
      test-user:x:1001:

   **passwd-table:**
   
   .. code-block:: none
        
      test-user:x:1001:1001::/home/test-user:/bin/sh
    
#. To create the password, run ``mkpasswd -m sha512crypt`` from a host computer.
   When prompted, enter the desired password for the user.
   This returns the hashed password:

   .. code-block:: console

       $ mkpasswd -m sha512crypt
       Password:
       $6$OJHEGl4Dk5nEwG6k$z19R1jc7cCfcQigX78cUH1Qzf2HINfB6dn6WgKmMLWgg967AV3s3tuuJE7uhLmBK.bHDpl8H5Ab/B3kNvGE1E.

#. Escape special characters by editing manually or by using the ``printf`` command from your shell, instead of the above:

   .. code-block:: none

       password_hash=`mkpasswd -m sha512crypt`
       printf '%q' "$password_hash"

   This is the ``USER_PASSWD``/``LMP_PASSWORD`` to be added to the build as the new user password.

#. Add the following block to ``meta-subscriber-overrides/recipes-samples/images/lmp-factory-image.bb``:

   .. code-block:: none

       USER_PASSWD = "\$6\$OJHEGl4Dk5nEwG6k\$z19R1jc7cCfcQigX78cUH1Qzf2HINfB6dn6WgKmMLWgg967AV3s3tuuJE7uhLmBK.bHDpl8H5Ab/B3kNvGE1E."

       EXTRA_USERS_PARAMS += "\
       groupadd <user>; \
       useradd -p '${USER_PASSWD}' <user>; \
       usermod -a -G sudo,users,plugdev <user>; \
       "

After these changes, the files ``/usr/lib/passwd`` and ``/usr/lib/group`` should include the configuration for the new user.

.. _replace-default-user:

Replacing Default ``fio`` User
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. tip::
   See ``lmp-passwd-table-default`` and ``lmp-group-table-default`` for ``fio`` user defaults.

To replacing the default user ``fio``, follow the steps for :ref:`ref-troubleshooting_lmp-user`;
For the ``user-id``, the value should be ``1000``. 

Add the following to ``meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc``,
replacing the values for your user and password as appropriate:

.. code-block:: none
        
   LMP_USER = "<user>"
   LMP_PASSWORD = "\$6\$OJHEGl4Dk5nEwG6k\$z19R1jc7cCfcQigX78cUH1Qzf2HINfB6dn6WgKmMLWgg967AV3s3tuuJE7uhLmBK.bHDpl8H5Ab/B3kNvGE1E."

LmP Time Servers
----------------

By default, LmP does time synchronization using ``systemd-timesyncd``. It is recommended to use that whenever possible as it is well integrated with ``systemd``. However, a common request is to enable Network Time Protocol (NTP) as a time server instead.

For that, first disable ``systemd-timesyncd`` support in ``meta-subscriber-overrides/recipes-core/systemd/systemd_%.bbappend``:

.. code-block:: none

    PACKAGECONFIG:remove = "timesyncd"

Then, enable ``ntp`` in ``meta-subscriber-overrides/recipes-samples/images/lmp-factory-image.bb`` by appending the ``CORE_IMAGE_BASE_INSTALL`` variable:

.. code-block:: none

    CORE_IMAGE_BASE_INSTALL += " \
        ntp \
    "

.. note::
    If ``systemd-timesyncd`` is used, the default ``ntp`` server list is set `in this recipe <https://github.com/foundriesio/meta-lmp/blob/main/meta-lmp-base/recipes-core/systemd/systemd_%25.bbappend>`_::

        DEF_FALLBACK_NTP_SERVERS ?= "time1.google.com time2.google.com time3.google.com time4.google.com time.cloudflare.com"

    If needed, this can be customized in ``meta-subscriber-overrides/recipes-core/systemd/systemd_%.bbappend``::

        DEF_FALLBACK_NTP_SERVERS += " <new-server>"

Installing Files Under ``var``
------------------------------

Anything created under ``/var`` gets removed when creating the OSTree deployment. For this reason, a recipe can only install content under it using `tmpfiles`_.

An example of using `tmpfiles`_ to create a directory under ``/var`` can be found in meta-lmp `collectd.bbappend`_, where `tmpfiles.conf`_ shows the directory to be created.

.. tip::
   Files can also be created dynamically using a runtime service. See how to add a :ref:`Custom Systemd Service<ref-troubleshooting_systemd-service>`.

.. _tmpfiles:
   https://www.freedesktop.org/software/systemd/man/tmpfiles.d.html
.. _collectd.bbappend:
   https://github.com/foundriesio/meta-lmp/blob/main/meta-lmp-base/recipes-extended/collectd/collectd_%25.bbappend
.. _tmpfiles.conf:
   https://github.com/foundriesio/meta-lmp/blob/main/meta-lmp-base/recipes-extended/collectd/collectd/tmpfiles.conf
