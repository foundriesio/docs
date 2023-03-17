.. _platform-customizing:

Platform Customization
======================

This page covers some common ways that the Linux® microPlatform (LmP) can be modified.
Platform Customization includes kernel options, startup services, user and group configuration, 
and other options related to the platform build. 

.. seealso::

   The tutorial for :ref:`tutorial-customizing-the-platform` covers adding a Systemd Startup Service.
   This helps introduces core concepts and steps related to customizing the platform, and is a good place to start.

Kernel Command Line Arguments
-----------------------------

The method of modifying kernel command line arguments differs between what LmP distro you have set.
The two options available are ``lmp``  (default) and ``lmp-base``.

See the :ref:`ref-linux-distro` page for an overview of the two options.

Distro: lmp
^^^^^^^^^^^

Extend the kernel command line by setting ``OSTREE_KERNEL_ARGS`` in ``meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc``::

    OSTREE_KERNEL_ARGS:<machine> = "console=${console} <new-args> ${OSTREE_KERNEL_ARGS_COMMON}"

Make sure you set the correct ``<machine>`` and other variables as needed.

.. note::
    The default is ``OSTREE_KERNEL_ARGS_COMMON ?= "root=LABEL=otaroot rootfstype=ext4"``.
    This variable is responsible for setting a valid ``root`` label for the device.
    It is not necessary on devices specifying the partition path directly with ``root=``.

Distro: lmp-base
^^^^^^^^^^^^^^^^

Extend the kernel command line by appending your commands to ``bootcmd_args`` in ``meta-subscriber-overrides/recipes-bsp/u-boot/u-boot-base-scr/<machine>/uEnv.txt.in``.
For example::

    bootcmd_args=setenv bootargs console=tty1 console=${console} root=/dev/mmcblk2p2 rootfstype=ext4 rootwait rw <new-args>

Reference for ``.bbappend`` can be found in ``meta-subscriber-overrides/recipes-bsp/u-boot/u-boot-base-scr.bbappend``::

    FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

.. note::
    If testing a board supported in ``meta-lmp``, an unmodified ``uEnv.txt.in`` can be found in ``meta-lmp/meta-lmp-bsp/recipes-bsp/u-boot/u-boot-base-scr/<machine>/uEnv.txt.in``.

Automatically Loading a Kernel Module
-------------------------------------

There are different options on how to automatically load a kernel module.
The best way depends on the use case.
Two cases are covered here.

A. Configure to only load a natively supported kernel module, such as ``i2c-dev``, by adding the following change in ``conf/machine/include/lmp-factory-custom.inc``::

    KERNEL_MODULE_AUTOLOAD:<machine> = "i2c-dev"

B. Add a new driver/module to the Linux kernel source code by editing ``meta-subscriber-overrides/recipes-kernel/kernel-modules/<module>_<pv>.bb`` and configuring the autoload in the recipe::

    SUMMARY = "Module summary"
    LICENSE = "GPLv2"
    LIC_FILES_CHKSUM = "file://COPYING;md5=12f884d2ae1ff87c09e5b7ccc2c4ca7e"

    inherit module

    SRC_URI = " \
      file://Makefile \
      file://<module>.c \
      file://<module>.h \
      file://COPYING \
    "

    S = "${WORKDIR}"

    KERNEL_MODULE_AUTOLOAD:append = "<module>"

Make sure to provide the source code and header for the new module, as well as the license and Makefile.
Also make sure to adjust the provided values as needed by the recipe (``LICENSE``, ``PV``).


Bind Mounting a File Into a Container
-------------------------------------

When bind mounting a file into a container, the parent directory needs to be bind mounted.
If a bind mount destination does not exist, Docker will create the endpoint as an empty directory rather than a file.

The Docker documentation on `containers and bind mounting <https://docs.docker.com/storage/bind-mounts/>`_ is a good place to start if you wish to learn more about this.

.. _ref-troubleshooting_systemd-service:

Adding a new Systemd Startup Service
-------------------------------------

LmP uses `systemd <https://systemd.io/>`_ for service management.
The tutorial on :ref:`tutorial-customizing-the-platform` provides a detailed walk-through of the steps required for adding a systemd service.
A summarized example for adding a shell script to run at startup is provided below for quick reference.
You should first be familiar with editing the ``meta-subscribers-overrides`` layer.

.. important::

    Make sure to replace ``<service-name>`` accordingly throughout the instructions below.

#. Create a directory for your service in ``meta-subscriber-overrides`` repo::

    mkdir -p recipes-support/<service-name>

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

#. Create the systemd service file ``<service-name>.service`` under this new directory::

    [Unit]
    Description=A description of your service
    After=rc-local.service

    [Service]
    Type=oneshot
    LimitNOFILE=1024
    ExecStart=/usr/bin/<service-name>.sh
    RemainAfterExit=true
    Environment=HOME=/home/root

#. Add the ``<service-name>.sh`` script to run at startup under this new directory::

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

#. Now add the configuration fragment in ``recipes-connectivity/networkmanager/networkmanager/eth1.nmconnection``::

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

.. _ref-troubleshooting_user-groups:

Extending User Groups
^^^^^^^^^^^^^^^^^^^^^

.. tip::
   The default LmP group and password tables can be found in ``meta-lmp/meta-lmp-base/files``.

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

Adding LmP Users
^^^^^^^^^^^^^^^^

#. To create a new LmP user or replace the default ``fio`` user, first add the new user to the system.
   The steps are similar to the ones described in :ref:`ref-troubleshooting_user-groups`.
   However normal users need a valid shell and ``user-id`` higher than ``1000`` for adding a new user, or equal to ``1000`` if replacing the ``fio`` user.
   For example:
   **group-table:**

   .. code-block:: none
  
        test-user:x:1001:

  **passwd-table:**
   
   .. code-block:: none
        
        test-user:x:1001:1001::/home/test-user:/bin/sh

#. To create the password for this new user, run from a host computer ``mkpasswd -m sha512crypt``.
   When prompted for password, enter the desired password for the user.
   This returns the hashed password. For example:

   .. prompt:: bash host:~$

       mkpasswd -m sha512crypt
       Password:
       $6$OJHEGl4Dk5nEwG6k$z19R1jc7cCfcQigX78cUH1Qzf2HINfB6dn6WgKmMLWgg967AV3s3tuuJE7uhLmBK.bHDpl8H5Ab/B3kNvGE1E.

#. Edit the result from the previous command to escape any ``$`` characters, for example:

   .. code-block:: none

       \$6\$OJHEGl4Dk5nEwG6k\$z19R1jc7cCfcQigX78cUH1Qzf2HINfB6dn6WgKmMLWgg967AV3s3tuuJE7uhLmBK.bHDpl8H5Ab/B3kNvGE1E.

   This is the ``USER_PASSWD``/``LMP_PASSWORD`` to be added to the build as the new user password.   

#. If including a new user, add the following block to ``meta-subscriber-overrides/recipes-samples/images/lmp-factory-image.bb``:

   .. code-block:: none

       USER_PASSWD = "\$6\$OJHEGl4Dk5nEwG6k\$z19R1jc7cCfcQigX78cUH1Qzf2HINfB6dn6WgKmMLWgg967AV3s3tuuJE7uhLmBK.bHDpl8H5Ab/B3kNvGE1E."

       EXTRA_USERS_PARAMS += "\
       groupadd <user>; \
       useradd -p '${USER_PASSWD}' <user>; \
       usermod -a -G sudo,users,plugdev <user>; \
       "

   **Or** if replacing the ``fio`` user, add the following to ``meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc``:

   .. code-block:: none
        
        LMP_USER = "<user>"
        LMP_PASSWORD = "\$6\$OJHEGl4Dk5nEwG6k\$z19R1jc7cCfcQigX78cUH1Qzf2HINfB6dn6WgKmMLWgg967AV3s3tuuJE7uhLmBK.bHDpl8H5Ab/B3kNvGE1E."

   .. note::

      Remember to replace ``USER_PASSWD``, ``<user>`` and ``LMP_PASSWORD`` accordingly.

After these changes, the files ``/usr/lib/passwd`` and ``/usr/lib/group`` should include the configuration for the new user.

