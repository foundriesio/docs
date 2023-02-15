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

We highly recommend not pruning all Targets from a tag to avoid container
builds failing from the lack of platform builds for this tag. To keep the last
``<number>`` targets from a tag use::

  fioctl targets prune --by-tag <tag> --keep-last <number>

There is also the ``--dryrun`` option so you can check the pruned targets before
running the command::

  fioctl targets prune --by-tag <tag> --keep-last <number> --dryrun

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

First, configure the **aktualizr-lite** polling interval:

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

5. Create the ``90-sota-fragment.toml`` file under this new directory:

.. code-block::

    [uptane]
    polling_sec = <time-sec>

.. note::
    Make sure to replace ``<time-sec>`` with the expected poll interval in seconds.

6. In the **recipes-samples/images/lmp-factory-image.bb** file, include this new
package under ``CORE_IMAGE_BASE_INSTALL``, for example:

.. code-block::

    --- a/recipes-samples/images/lmp-factory-image.bb
    +++ b/recipes-samples/images/lmp-factory-image.bb
    @@ -24,9 +24,10 @@ CORE_IMAGE_BASE_INSTALL += " \
         networkmanager-nmcli \
         git \
         vim \
    +    sota-fragment \
    ...

Then, configure the **fioconfig** daemon interval:

8. Create the ``fioconfig`` folder in ``meta-subscriber-overrides`` repo:

.. prompt:: bash host:~$

    cd meta-subscriber-overrides
    mkdir -p recipes-support/fioconfig

9. Add a new file under this directory:

.. prompt:: bash host:~$

     touch recipes-support/fioconfig/fioconfig_git.bbappend

10. Include the content below to the file created in the last step:

.. code-block:: none

    FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

    SRC_URI:append = " \
        file://fioconfig.conf \
    "

    do_install:append() {
        install -Dm 0644 ${WORKDIR}/fioconfig.conf ${D}${sysconfdir}/default/fioconfig
    }

11. Create another directory under the one we just created so we can supply the
source file (``fioconfig.conf``) for the recipe above:

.. prompt:: bash host:~$

    cd meta-subscriber-overrides
    mkdir -p recipes-support/fioconfig/fioconfig

12. Create the ``fioconfig.conf`` file under this new directory:

.. code-block::

    DAEMON_INTERVAL=<time-sec>

.. note::
    Make sure to replace ``<time-sec>`` with the expected poll interval in seconds.

Commit and trigger a new build to include these new changes and have a new
polling interval.

OTA Update Fails Because of Missing SPL Keys
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When updating to a newer base lmp-manifest, some FoundriesFactories
may face issues with OTA upgrades from v85 to the next release. It manifests
as a failed boot attempt and error in the u-boot log:

.. code-block::

    U-Boot SPL 2021.04+fio+g38c3083e39 (Feb 16 2022 - 14:50:02 +0000)
    power_pca9450b_init
    DDRINFO: start DRAM init
    DDRINFO: DRAM rate 3000MTS
    DDRINFO:ddrphy calibration done
    DDRINFO: ddrmix config done
    Normal Boot
    Trying to boot from MMC2
    SPL: Booting secondary boot path: using 0x1300 offset for next boot image
    ## Checking hash(es) for config config-1 ... fit_config_verify_required_sigs: No signature node found: FDT_ERR_NOTFOUND
    SPL_FIT_SIGNATURE_STRICT needs a valid config node in FIT
    ### ERROR ### Please RESET the board ###

This suggests that the SPL key is missing from the factory. The key is defined
in the OE recipe and it defaults to ``spldev``.

.. prompt::

    UBOOT_SPL_SIGN_KEYNAME="spldev"

This can be confirmed by checking whether files ``spldev.key`` and ``spldev.crt``
are missing from the ``lmp-manifest/factory-keys`` directory. If so, the easiest
fix is to generate the keys and add them to the repository.

.. prompt::

    cd factory-keys
    openssl genpkey -algorithm RSA -out spldev.key \
          -pkeyopt rsa_keygen_bits:2048 \
          -pkeyopt rsa_keygen_pubexp:65537
    openssl req -batch -new -x509 -key spldev.key -out spldev.crt

Once the ``spldev.key`` and ``spldev.crt`` are created, add them to the repository.

.. prompt::

    git add factory-keys/spldev.key
    git add factory-keys/spldev.crt
    git commit

Once the commit is pushed upstream, the Foundries.io CI will generate a build
that fixes the issue.

Handling updates in /etc
^^^^^^^^^^^^^^^^^^^^^^^^

Files created or modified in ``/etc`` during runtime are not handled by OSTree
during an OTA. For this reason, we suggest setting system-wide configs in
``/usr`` whenever possible so that these changes are covered by OTA updates.

We suggest managing files that live in ``/usr`` with a systemd service
(:ref:`ref-troubleshooting_systemd-service`). The runtime service should handle
the needed updates to the ``/etc`` files.

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

Bind mounting a file into a container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When bind mounting a file into a container, the parent directory needs to be bind mounted.
If a bind mount destination does not exist, Docker will create the endpoint as an empty directory rather than a file.

The Docker documentation on `containers and bind mounting <https://docs.docker.com/storage/bind-mounts/>`_ is a good place to start if you wish to learn more about this.

.. _ref-troubleshooting_systemd-service:

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

.. _ref-troubleshooting_user-groups:

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
    This example works for system groups and system users (``user-id`` less than
    ``1000``). For normal users, check :ref:`ref-troubleshooting_lmp-user`.

.. note::
    Platform build errors like below are fixed after extending the user group:
    ``normal groupname `<group>` does not have a static ID defined.``

3. Add these files to the build in ``meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc``:

.. code-block:: none

    USERADD_GID_TABLES += "files/custom-group-table"
    USERADD_UID_TABLES += "files/custom-passwd-table"

.. _ref-troubleshooting_lmp-user:

Adding LmP Users
^^^^^^^^^^^^^^^^

1. To create a new LmP user or replace the default ``fio`` user, first add the new
user to the system. The steps are similar to the ones described in
:ref:`ref-troubleshooting_user-groups`, but normal users need a valid shell and
``user-id`` higher than ``1000`` for adding a new user, or equal to ``1000`` if
replacing the ``fio`` user, for example:

**group-table:**

.. code-block:: none

    test-user:x:1001:

**passwd-table:**

.. code-block:: none

    test-user:x:1001:1001::/home/test-user:/bin/sh

2. To create the password for this new user, run on a host computer:

.. prompt:: bash host:~$

    mkpasswd -m sha512crypt

When prompted for password, enter the wanted password for the user. This returns
the hashed password. For example:

.. prompt:: bash host:~$

    mkpasswd -m sha512crypt
    Password:
    $6$OJHEGl4Dk5nEwG6k$z19R1jc7cCfcQigX78cUH1Qzf2HINfB6dn6WgKmMLWgg967AV3s3tuuJE7uhLmBK.bHDpl8H5Ab/B3kNvGE1E.

3. Edit the result from the previous command to escape any ``$`` characters, for example:

.. code-block:: none

    \$6\$OJHEGl4Dk5nEwG6k\$z19R1jc7cCfcQigX78cUH1Qzf2HINfB6dn6WgKmMLWgg967AV3s3tuuJE7uhLmBK.bHDpl8H5Ab/B3kNvGE1E.

This is the ``USER_PASSWD``/``LMP_PASSWORD`` to be added to the build as the new user password.

4. If including a new user, add the following block to ``meta-subscriber-overrides/recipes-samples/images/lmp-factory-image.bb``:

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

After these changes, the files ``/usr/lib/passwd`` and ``/usr/lib/group`` should
include the configuration for the new user.

Re-register a Device
^^^^^^^^^^^^^^^^^^^^

You may need to re-register the same device during development. In this case,
follow these steps:

1. Delete the device from the UI ``Devices`` tab or with:

.. prompt:: bash host:~$

    fioctl device delete <device-name>

2. Stop ``aktualizr-lite`` and ``fioconfig`` on the device:

.. prompt:: bash device:~#

    systemctl stop aktualizr-lite
    systemctl stop fioconfig.path
    systemctl stop fioconfig.service

3. Delete ``sql.db`` on the device:

.. prompt:: bash device:~#

    rm /var/sota/sql.db

4. Then perform the registration again.


NXP SE05X Secure Element and PKCS#11 Trusted Application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are two memory limits to be aware of: the Secure Element's non-volatile
memory, and the built-time configurable PKCS#11 Trusted Application (TA) heap
size.

When RSA and EC keys are created using the TA, a request is sent to the Secure
Element for the creation of those keys. On success, a key is created in the
Secure Element non volatile memory; the public key is then read back from the
SE to the TA persistent storage —only a handle to the private key in the
Secure Element is provided and stored by the TA.

During that creation process the TA also keeps a copy of the key on its heap.

This means that a system that chooses to create all of its keys during boot
might run out of heap before running out of storage in the secure element.

To avoid this issue, OP-TEE should be configured with ``CFG_PKCS11_TA_HEAP_SIZE``
large enough that it allows the client to fill the SE NVM before an out of
memory condition is raised by the TA (which would cause a secure world panic).

An experimental way to validate the thresholds is to loop on RSA or EC
key creation until it fails: if there is a panic or a PKCS#11 OOM fault,
``CFG_PKCS11_TA_HEAP_SIZE`` can then be increased as there is still room in the SE NVM
to store more keys.


