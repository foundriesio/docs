.. _tutorial-enabling-application:

Enabling the App
^^^^^^^^^^^^^^^^^

After creating the systemd service recipe, it is important to install the package to the image.

In ``meta-subscriber-overrides`` is  ``recipes-samples/images/lmp-factory-image.bb`` with the variable ``CORE_IMAGE_BASE_INSTALL``.

To install a package to the image, append this variable with the package name.

For this example, add ``shellhttpd`` and ``netcat``.
As the Linux® microPlatform does not include ``curl``, let us include ``curl`` as well.

.. tip::
   This tutorial installs curl as a package to illustrate how packages can be added to the platform.
   In practice, you can also install ``curl`` as a :ref:`container <ref-troubleshooting_network-connectivity>`.
   Installing as a container rather than directly on the platform may be simpler and take less time.

Edit ``recipes-samples/images/lmp-factory-image.bb`` and append ``CORE_IMAGE_BASE_INSTALL``:

.. code-block:: console

    $ cd ..
    $ vi recipes-samples/images/lmp-factory-image.bb

.. code-block:: text

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
