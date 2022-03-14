Shellhttpd Recipe
^^^^^^^^^^^^^^^^^

All applications installed on your platform are described by a recipe.

A recipe is a file with the application name, version and extension ``.bb``.
To create the application ``shellhttpd`` the corresponding recipe will have the
name: ``shellhttpd_0.1.bb``.

In the ``meta-subscriber-overrides`` folder, create the ``recipes-support`` folder.

.. prompt:: bash host:~$

    mkdir recipes-support

In the ``recipes-support`` folder, use git to download the ``shellhttpd`` recipe
from the extra-meta-subscriber-overrides repository:

.. prompt:: bash host:~$, auto

    host:~$ cd recipes-support
    host:~$ git remote add fio https://github.com/foundriesio/extra-meta-subscriber-overrides.git
    host:~$ git remote update
    host:~$ git checkout remotes/fio/main -- shellhttpd

The ``shellhttpd`` recipe should be inside the ``recipes-support`` folder:

.. prompt:: bash host:~$, auto

    host:~$ tree -L 3 .

Example output:

.. prompt:: text

     └── shellhttpd
         ├── shellhttpd
         │   ├── httpd.sh
         │   └── shellhttpd.service
         └── shellhttpd_0.1.bb

Check the content of your ``shellhttpd/shellhttpd_0.1.bb`` file:

.. prompt:: bash host:~$, auto

    host:~$ cat shellhttpd/shellhttpd_0.1.bb

**shellhttpd/shellhttpd_0.1.bb**:

.. prompt:: text

     SUMMARY = "Start up Shellhttpd Application"
     LICENSE = "MIT"
     LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

     inherit allarch systemd
     RDEPENDS_${PN} += "bash"

     SRC_URI = " \
	     file://httpd.sh \
	     file://shellhttpd.service \
     "
     SRCREV = "f90f221ce4fcea2fde0062bc909f26cca6dbd1b6"

     S = "${WORKDIR}/git"

     PACKAGE_ARCH = "${MACHINE_ARCH}"

     SYSTEMD_SERVICE_${PN} = "shellhttpd.service"
     SYSTEMD_AUTO_ENABLE_${PN} = "enable"

     do_install () {
	     install -d ${D}${systemd_system_unitdir}
	     install -m 0644 ${WORKDIR}/shellhttpd.service ${D}${systemd_system_unitdir}
	     install -d ${D}${datadir}/shellhttpd/
	     install -m 0755 ${WORKDIR}/httpd.sh ${D}${datadir}/shellhttpd/
     }

     FILES:${PN} += "${systemd_system_unitdir}/shellhttpd.service"
     FILES:${PN} += "${systemd_unitdir}/system-preset"
     FILES:${PN} += "${datadir} ${datadir}/app-manager/"

The ``shellhttpd/shellhttpd_0.1.bb`` file has all the details for the ``shellhttpd`` application.

This tutorial does not intend to cover the Yocto Project concepts. However,
let's highlight the following variables:

- ``SRC_URI``: It is including the files ``httpd.sh`` and ``shellhttpd.service`` in the ``${WORKDIR}``.
- ``do_install``: It is installing the file from ``${WORKDIR}`` to the Linux distribution root file system.

Check the content of your ``shellhttpd/shellhttpd/httpd.sh`` file:

.. prompt:: bash host:~$, auto

     host:~$ cat shellhttpd/shellhttpd/httpd.sh

**shellhttpd/shellhttpd/httpd.sh**:

.. prompt:: text

     #!/bin/sh -e

     PORT="${PORT-8090}"
     MSG="${MSG-OK}"

     RESPONSE="HTTP/1.1 200 OK\r\n\r\n${MSG}\r\n"

     while true; do
     	echo -en "$RESPONSE" | nc -c -l -p "${PORT}" || true
     	echo "= $(date) ============================="
     done

The ``shellhttpd/shellhttpd/httpd.sh`` is very similar to the ``httpd.sh`` used in the previous tutorials.

This is the shell script executed by the ``shellhttpd.service`` file.

Check the content of your ``shellhttpd/shellhttpd/shellhttpd.service`` file:

.. prompt:: bash host:~$, auto

    host:~$ cat shellhttpd/shellhttpd/shellhttpd.service

**shellhttpd/shellhttpd/shellhttpd.service**:

.. prompt:: text

     [Unit]
     Description=Shellhttpd Minimal Web Server
     DefaultDependencies=no
     After=systemd-udev-settle.service
     Before=sysinit.target shutdown.target
     Conflicts=shutdown.target
     Description=Start up Shellhttpd Application

     [Service]
     ExecStart=/bin/sh /usr/share/shellhttpd/httpd.sh
     RemainAfterExit=true

     [Install]
     WantedBy=sysinit.target

The ``shellhttpd/shellhttpd/shellhttpd.service`` is a systemd service. The only
variable that should be highlight here is:

- ``ExecStart``: Execute the ``httpd.sh`` script.
