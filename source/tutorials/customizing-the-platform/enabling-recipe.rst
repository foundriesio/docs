.. _tutorial-enabling-application:

Enabling Application
^^^^^^^^^^^^^^^^^^^^

After creating the file recipe, it is important to install the package to the image.

The ``meta-subscriber-overrides`` provides the ``recipes-samples/images/lmp-factory-image.bb`` 
file with the variable ``CORE_IMAGE_BASE_INSTALL``.

To install a package to the image file, append this variable with the package name.

For this example, add the ``shellhttpd`` and ``netcat`` package. Additionally, if you 
remember from the previous tutorial, the Linux microPlatform does not include ``curl``, 
this is why we used ``wget`` in the device. Let's include the ``curl`` as well.

Edit the ``recipes-samples/images/lmp-factory-image.bb`` file and append the 
variable ``CORE_IMAGE_BASE_INSTALL``:

.. prompt:: bash host:~$, auto

    host:~$ cd ..
    host:~$ gedit recipes-samples/images/lmp-factory-image.bb

**recipes-samples/images/lmp-factory-image.bb:**

.. prompt:: text

     SUMMARY = "Minimal factory image which includes OTA Lite, Docker, and OpenSSH support"
     
     require recipes-samples/images/lmp-image-common.inc
     
     # Factory tooling requires SOTA (OSTree + Aktualizr-lite)
     require ${@bb.utils.contains('DISTRO_FEATURES', 'sota', 'recipes-samples/images/lmp-feature-factory.inc', '', d)}
     
     # Enable wayland related recipes if required by DISTRO
     require ${@bb.utils.contains('DISTRO_FEATURES', 'wayland', 'recipes-samples/images/lmp-feature-wayland.inc', '', d)}
     
     # Enable OP-TEE related recipes if provided by the image
     require ${@bb.utils.contains('MACHINE_FEATURES', 'optee', 'recipes-samples/images/lmp-feature-optee.inc', '', d)}
     
     require recipes-samples/images/lmp-feature-softhsm.inc
     require recipes-samples/images/lmp-feature-wireguard.inc
     require recipes-samples/images/lmp-feature-docker.inc
     require recipes-samples/images/lmp-feature-wifi.inc
     require recipes-samples/images/lmp-feature-ota-utils.inc
     require recipes-samples/images/lmp-feature-sbin-path-helper.inc
     
     IMAGE_FEATURES += "ssh-server-openssh"
     
     CORE_IMAGE_BASE_INSTALL_GPLV3 = "\
         packagegroup-core-full-cmdline-utils \
         packagegroup-core-full-cmdline-multiuser \
     "
     
     CORE_IMAGE_BASE_INSTALL += " \
         kernel-modules \
         networkmanager-nmcli \
         git \
         vim \
         packagegroup-core-full-cmdline-extended \
         ${@bb.utils.contains('LMP_DISABLE_GPLV3', '1', '', '${CORE_IMAGE_BASE_INSTALL_GPLV3}', d)} \
         netcat \
         curl \
         shellhttpd \
     "
