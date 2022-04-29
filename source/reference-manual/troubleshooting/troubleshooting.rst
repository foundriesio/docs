.. _ref-troubleshooting:

Troubleshooting and FAQ
=======================

General
-------

.. _ref-troubleshooting_network-connectivity:

Network Connectivity
^^^^^^^^^^^^^^^^^^^^

When debugging network connectivity and access issues, it can be helpful to
use ``curl``. However, LmP does not ship with the command.

Rather than including ``curl`` on the host device, a simple approach is to run
it via a Alpine Linux container.

.. _ref-troubleshooting_request-entity-too-large:

Request Entity Too Large
^^^^^^^^^^^^^^^^^^^^^^^^

This error occurs when your Factory has accumulated too much Target metadata to
be signed by TUF. This happens because the :term:`targets.json` containing all
of your Targets that is  associated with your Factory grows large over time::

  Signing local TUF targets
  == 2020-11-24 23:12:53 Running: garage-sign targets sign --repo /root/tmp.dNLAIH
  --key-name targets
  |  signed targets.json to /root/tmp.dNLAIH/roles/targets.json
  |--
  Publishing local TUF targets to the remote TUF repository
  == 2020-11-24 23:12:55 Running: garage-sign targets push --repo /root/tmp.dNLAIH
  |  An error occurred
  |  com.advancedtelematic.libtuf.http.SHttpjServiceClient$HttpjClientError:
  ReposerverHttpClient|PUT|http/413|https://api.foundries.io/ota/repo/magicman//api/v1/user_repo/targets|<html>
  |  <head><title>413 Request Entity Too Large</title></head>
  |  <body>
  |  <center><h1>413 Request Entity Too Large</h1></center>
  |  <hr><center>nginx/1.19.3</center>
  |  </body>
  |  </html>

Solution
""""""""

Pruning (deletion) of Targets is a manual maintenance procedure you
must consider when creating Targets over time.

**The solution** is to prune the Targets that you no longer need using
Fioctl. This removes these targets from the :term:`targets.json` associated with
your Factory, allowing the production of new Targets.

.. warning::

   Ensure there are no important devices running on a Target that is about to be
   pruned. If you are intending on pruning ``master``, be careful and make sure
   you know what you are doing.

You can individually prune/delete targets by their Target number::

  fioctl targets prune <target_number>

Or, you can prune by tag, such as ``devel`` or ``experimental``::

  fioctl targets prune --by-tag <tag>


.. _ref-aktualizr-lite-pruning:

Aktualizr-Lite Pruning Containers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, :ref:`ref-aktualizr-lite` will prune Docker containers periodically.
If this behavior is undesirable, it can be worked around by adding
``aktualizr-lite-no-prune`` as a label to Docker containers, or by adding
``docker_prune = "0"`` to the ``[pacman]`` section of ``/var/sota/sota.toml`` on
a given device.

.. code-block::

   LABEL aktualizr-lite-no-prune

.. note:: https://docs.docker.com/engine/reference/builder/#label

Aktualizr-lite and fioconfig Polling Time
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``fioconfig`` and ``aktualizr-lite`` poll for new configuration and updates
every 5 minutes by default. It might be helpful to decrease this interval for
development purposes. Here are some ways to achieve this.

Changing interval in runtime
""""""""""""""""""""""""""""

1. On your device, create a settings file in the ``/etc/sota/conf.d/`` folder to
configure ``aktualizr-lite``:

.. prompt:: bash device:~$

    sudo mkdir -p /etc/sota/conf.d/
    sudo sh -c 'printf "[uptane]\npolling_sec = <time-sec>" > /etc/sota/conf.d/90-sota-fragment.toml'

2. Next, create a settings file in the ``/etc/default/`` folder to configure
``fioconfig``:

.. prompt:: bash device:~$

    sudo sh -c 'printf "DAEMON_INTERVAL=<time-sec>" > /etc/default/fioconfig'

3. Restart both services:

.. prompt:: bash device:~$

    sudo systemctl restart aktualizr-lite
    sudo systemctl restart fioconfig

.. note::
    Make sure to replace ``<time-sec>`` with the expected poll interval in seconds.

Changing interval in the build
""""""""""""""""""""""""""""""

1. Create the ``sota-fragment`` folder in ``meta-subscriber-overrides`` repo:

.. prompt:: bash host:~$

    cd meta-subscriber-overrides
    mkdir -p recipes-sota/sota-fragment

2. Add a new file under this directory:

.. prompt:: bash host:~$

     touch recipes-sota/sota-fragment/sota-fragment_0.1.bb

3. Include the content below to the file created in the last step:

.. code-block:: none

    SUMMARY = "SOTA configuration fragment"
    SECTION = "base"
    LICENSE = "MIT"
    LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

    inherit allarch

    SRC_URI = " \
            file://90-sota-fragment.toml \
    "

    S = "${WORKDIR}"

    do_install() {
            install -m 0700 -d ${D}${libdir}/sota/conf.d
            install -m 0644 ${WORKDIR}/90-sota-fragment.toml ${D}${libdir}/sota/conf.d/90-sota-fragment.toml
    }

    FILES:${PN} += "${libdir}/sota/conf.d/90-sota-fragment.toml"

4. Create another directory under the one we just created so we can supply the
source file (``90-sota-fragment.toml``) for the recipe above:

.. prompt:: bash host:~$

    cd meta-subscriber-overrides
    mkdir -p recipes-sota/sota-fragment/sota-fragment

5. Create the ``90-sota-fragment.toml`` file under this new directory::

    [uptane]
    polling_sec = <time-sec>

.. note::
    Make sure to replace ``<time-sec>`` with the expected poll interval in seconds.

Platform Customizing
--------------------

Changing kernel command line args
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For ``DISTRO=lmp``, the kernel command line can be extended by setting ``OSTREE_KERNEL_ARGS`` in
``meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc``::

    OSTREE_KERNEL_ARGS:<machine> = "console=${console} <new-args> ${OSTREE_KERNEL_ARGS_COMMON}"

Make sure you set the correct ``<machine>`` and other variables as needed.

.. note::
    By default ``OSTREE_KERNEL_ARGS_COMMON ?= "root=LABEL=otaroot rootfstype=ext4"``.
    This variable is responsible for setting a valid ``root`` label for the
    device. It is not necessarily needed on devices specifying the partition
    path directly with ``root=``.

Now, if ``DISTRO=lmp-base`` is set, the kernel command line can be extended by
appending commands to ``bootcmd_args`` in
``meta-subscriber-overrides/recipes-bsp/u-boot/u-boot-base-scr/<machine>/uEnv.txt.in``,
for example::

    bootcmd_args=setenv bootargs console=tty1 console=${console} root=/dev/mmcblk2p2 rootfstype=ext4 rootwait rw <new-args>

Reference for ``bbappend`` for this file:

**meta-subscriber-overrides/recipes-bsp/u-boot/u-boot-base-scr.bbappend:**

.. prompt:: text

    FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

.. note::
    If testing a reference board supported in ``meta-lmp``, the original ``uEnv.txt.in``
    file can be found in ``meta-lmp/meta-lmp-bsp/recipes-bsp/u-boot/u-boot-base-scr/<machine>/uEnv.txt.in``.

Adding a new systemd startup service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

LmP uses `systemd <https://systemd.io/>`_ for service management. Our tutorial on
:ref:`tutorial-customizing-the-platform` provides a detailed walk-through of
the steps required for adding a systemd service. A summarized example for adding
a shell script to run at startup is provided here for quick reference. You
should first be familiar with editing the ``meta-subscribers-overrides`` layer.

.. note::
    Make sure to replace ``<service-name>`` accordingly throughout the instructions below.

1. Create a directory for your service in ``meta-subscriber-overrides`` repo::

    mkdir -p recipes-support/<service-name>

2. Add a new file named ``<service-name>.bb`` under this directory, with the
   following content::

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

    SYSTEMD_SERVICE_${PN} = "<service-name>.service"
    SYSTEMD_AUTO_ENABLE_${PN} = "enable"

    do_install () {
	    install -d ${D}${bindir}
	    install -m 0755 ${WORKDIR}/<service-name>.sh ${D}${bindir}/<service-name>.sh

	    install -d ${D}${systemd_system_unitdir}
	    install -m 0644 ${WORKDIR}/<service-name>.service ${D}${systemd_system_unitdir}
    }

    FILES:${PN} += "${systemd_system_unitdir}/<service-name>.service"
    FILES:${PN} += "${systemd_unitdir}/system-preset"

3. Create another directory with the same name as the one we just created to
   place the source file(s) for the recipe::

    recipes-support/<service-name>/<service-name>

4. Create the systemd service file ``<service-name>.service`` under this new
   directory::

    [Unit]
    Description=A description of your service
    After=rc-local.service

    [Service]
    Type=oneshot
    LimitNOFILE=1024
    ExecStart=/usr/bin/<service-name>.sh
    RemainAfterExit=true
    Environment=HOME=/home/root

5. Also add the ``<service-name>.sh`` script to run at startup under this new
   directory::

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

6. Remember to install the new service by appending the ``CORE_IMAGE_BASE_INSTALL``
   variable in ``lmp-factory-image.bb``::

    CORE_IMAGE_BASE_INSTALL += " \
    <service-name> \
    "

7. Lastly, check that the service is starting. From the device:

   ``systemctl status <service-name>.service``

Setting a static IP to the device
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example shows how to configure the `eth1` interface, but the steps can be
extended for the other net interfaces.

1. Create the .bbappend file as:

**recipes-connectivity/networkmanager/networkmanager_%.bbappend**

.. code-block:: none

    FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

    SRC_URI:append = " \
        file://eth1.nmconnection \
    "

    do_install:append () {
        install -d ${D}${sysconfdir}/NetworkManager/system-connections
        install -m 0600 ${WORKDIR}/eth1.nmconnection ${D}${sysconfdir}/NetworkManager/system-connections

2. Create the configuration fragment as:

**recipes-connectivity/networkmanager/networkmanager/eth1.nmconnection**

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

Remember to adjust the `address1` parameter as needed.

Automatically Loading a Kernel Module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are different options on how to automatically load a kernel module, the
best way depends on each use case. Here two cases are covered.

1. To load a native supported kernel module, like ``i2c-dev``, just add the
following change:

**conf/machine/include/lmp-factory-custom.inc:**

.. code-block:: none

    KERNEL_MODULE_AUTOLOAD:<machine> = "i2c-dev"

2. Adding a new driver/module to the Linux kernel source code:

**meta-subscriber-overrides/recipes-kernel/kernel-modules/<module>_<pv>.bb:**

.. code-block:: none

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

Make sure to provide the source code and header for the new module, as well as
the license and Makefile. Also make sure to adjust the provided values as
needed by the recipe (``LICENSE``, ``PV``).

Extending User Groups
^^^^^^^^^^^^^^^^^^^^^

The default LmP group and password tables can be found at ``meta-lmp/meta-lmp-base/files``.
To define a new user group in a factory, follow these steps:

1. Define a custom group table in ``meta-subscriber-overrides/files/custom-group-table``
with the wanted user groups:

.. code-block:: none

    <username>:x:<user-id>:

For example:

.. code-block:: none

    systemd-coredump:x:998:

2. Define a custom passwd table in ``meta-subscriber-overrides/files/custom-passwd-table``
for the new user groups:

.. code-block:: none

    <username>:x:<user-id>:<group-id>::<home-dir>:<command>

For example:

.. code-block:: none

    systemd-coredump:x:998:998::/:/sbin/nologin

.. note::
    This example works for system groups and system users (``user-id`` < 1000).

3. Add these files to the build in ``meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc``:

.. code-block:: none

    USERADD_GID_TABLES += "files/custom-group-table"
    USERADD_UID_TABLES += "files/custom-passwd-table"
