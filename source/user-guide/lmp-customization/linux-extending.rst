.. _extending-lmp:

Extending the Linux microPlatform
=================================

.. _ref-adding-packages-image:

Adding Packages to the Image
----------------------------

The ``meta-subscriber-overrides.git`` repo allows you to customize the packages included in your factory image.
To do this, you add packages as a list to the variable ``CORE_IMAGE_BASE_INSTALL`` in ``recipes-samples/images/lmp-factory-image.bb``.
For a quick example let us add the ``stress-ng`` utility package to the build:

.. code-block:: bash

  git clone https://source.foundries.io/factories/<myfactory>/meta-subscriber-overrides.git
  vi meta-subscriber-overrides/recipes-samples/images/lmp-factory-image.bb

Add "stress-ng" to the package list.::

  vim \
  stress-ng \
  ...

Then::

  git add meta-subscriber-overrides/recipes-samples/images/lmp-factory-image.bb
  git commit -m "add stress-ng package to device image"
  git push

Go and get a coffee—your Factory is generating a new image with this package.
This can take a half an hour or more.

You can check the status at:

 ``https://ci.foundries.io/projects/<myfactory>/lmp/``

Once completed, the device will reboot after the update is applied.
This behavior is customizable so that you can apply rules to determine when devices should be restarted.
Once restarted the stress-ng command will be available.

List of Available Recipes
-------------------------
OE provides a tool_ to search layers and recipes.
Remember to set the same branch name used by the current factory version.

.. _tool:
   https://layers.openembedded.org/layerindex/branch/master/layers/

Creating a Python3 Package from PyPi
------------------------------------
There are Python packages that do not yet have a recipe for python3 in OE.
If this is the case with a desired package, use this template below to add a new package from PyPi.

Create a recipe in the **meta-subscriber-overrides.git** repository using the following naming scheme:

  ``recipes-devtools/python/python3-<package name>_<version>.bb``

  (E.g.: recipes-devtools/python/python3-virtualenv_16.4.3.bb)

Example file contents::

  DESCRIPTION = "Virtual Python Environment builder"
  HOMEPAGE = "https://pypi.python.org/pypi/virtualenv"
  SECTION = "devel/python"
  LICENSE = "MIT"
  LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=51910050bd6ad04a50033f3e15d6ce43"

  SRC_URI[md5sum] = "5f012791118fe99990d9422cf560edf3"
  SRC_URI[sha256sum] = "984d7e607b0a5d1329425dd8845bd971b957424b5ba664729fab51ab8c11bc39"

  inherit setuptools pypi

  DEPENDS += " \
        python3-pip \
        "

  RDEPENDS:${PN} += " \
        python3-dateutil \
        "

Using the information and packages at the PyPi website, you can fill in the details about the new Python package

.. figure:: /_static/pypi-package.png
   :alt: Pypi package
   :align: center
   :width: 5in

   Pypi package

Update the following variables to reflect the details from the package you wish to create a recipe for.

#. ``DESCRIPTION``
#. ``HOMEPAGE``
#. ``LICENSE``
#. ``LIC_FILES_CHKSUM``
#. ``SRC_URI[md5sum]`` (md5sum of the download artifact from pypi)
#. ``SRC_URI[sha256sum]`` (sha256sum of the download artifact from pypi)
#. ``DEPENDS`` Dependencies resolved at do_configure
#. ``RDEPENDS`` Dependencies resolved at do_build

Using FEATURES to configure LmP
-------------------------------

There are three features variable we can use to control and configure the build system: ``DISTRO_FEATURES``, ``IMAGE_FEATURES`` and ``MACHINE_FEATURES``.
Each one of them takes effect in one aspect of the build system.

.. important::

    When changing ``DISTRO_FEATURES``, the distro is changed and it results in
    rebuild of several packages which can take a while.

    When changing ``MACHINE_FEATURES``, the hardware description changes and it
    result in different group of packages being installed in the image.

    When changing ``IMAGE_FEATURES``, the image changes, and it may reflect on the
    list of packages installed, or in the image configuration.

    Make sure to understand what will be the result in case of any change.

DISTRO_FEATURES is a list of configurations from a distro that reflects how some packages are built or installed.
There is a list of `Yocto Project distro features`_ supported.
However, the list can be expanded by other meta layers.

For example, the distro feature ``systemd`` or ``wayland`` are used to define the list of packages to be installed, and to configure how some packages build.
The distro feature ``modsign`` is used along with certificates to sign the kernel modules.

The default value used by LmP is defined in the ``meta-lmp/meta-lmp-base/conf/distro/include/lmp.inc`` and can be customized by architecture, machine, or any other override.
To customize it, use ``DISTRO_FEATURES:append = <value>`` to add a feature to the list, and ``DISTRO_FEATURES:remove = <value>`` to remove a feature from the list.
To remove a feature from an override list, use ``DISTRO_FEATURES:remove:<machine> = <value>``.

The command ``bitbake-getvar`` can be used to see the value of some variables, and all the intermediate values::

  $ bitbake-getvar DISTRO_FEATURES
  NOTE: Starting bitbake server...
  #
  # $DISTRO_FEATURES [7 operations]
  #   :append /lmp/source/main/build-lmp/conf/../../layers/meta-lmp/meta-lmp-base/conf/distro/include/lmp.inc:40
  #     " pam usrmerge virtualization ptest alsa"
  #   :append /lmp/source/main/build-lmp/conf/../../layers/meta-lmp/meta-lmp-base/conf/distro/lmp.conf:18
  #     " sota"
  #   set? /lmp/source/main/build-lmp/conf/../../layers/openembedded-core/meta/conf/distro/include/default-distrovars.inc:20
  #     "${DISTRO_FEATURES_DEFAULT}"
  #   :append /lmp/source/main/build-lmp/conf/../../layers/openembedded-core/meta/conf/distro/include/init-manager-systemd.inc:2
  #     " systemd"
  #   set /lmp/source/main/build-lmp/conf/../../layers/openembedded-core/meta/conf/documentation.conf:144
  #     [doc] "The features enabled for the distribution."
  #   set? /lmp/source/main/build-lmp/conf/../../layers/openembedded-core/meta/conf/bitbake.conf:884
  #     ""
  #   :append[tegra] /lmp/source/main/build-lmp/conf/../../layers/meta-lmp/meta-lmp-bsp/conf/machine/include/lmp-machine-custom.inc:690
  #     " opengl"
  # pre-expansion value:
  #   "${DISTRO_FEATURES_DEFAULT} pam usrmerge virtualization ptest alsa sota systemd"
  DISTRO_FEATURES="acl argp bluetooth ext2 ipv4 ipv6 largefile usbgadget usbhost wifi xattr zeroconf pci vfat modsign efi security tpm integrity seccomp pam usrmerge virtualization ptest
  alsa sota systemd"

The log is generated using ``DISTRO="lmp"``. The ``DISTRO_FEATURES`` changed with seven operations and only one of them is for an override (``tegra``).
The log also shows the file path and line for each operation.

The line starting with ``DISTRO_FEATURES=`` show the variable value.

The Yocto Project also provides ``IMAGE_FEATURES`` and ``MACHINE_FEATURES``, a list of features for the image and to describe the machine.
There is a list of `Yocto Project image features`_ and `Yocto Project machine features`_ supported by the project.

The LmP uses the ``MACHINE_FEATURES`` from a machine to define if a package is included.
For example, the OP-Tee package is only included in an image if the target machine includes the feature ``optee`` in ``MACHINE_FEATURE``.

.. _Yocto Project distro features:
   https://docs.yoctoproject.org/kirkstone/ref-manual/features.html#distro-features

.. _Yocto Project image features:
   https://docs.yoctoproject.org/kirkstone/ref-manual/features.html#image-features

.. _Yocto Project machine features:
   https://docs.yoctoproject.org/kirkstone/ref-manual/features.html#machine-features

Including Private Git+ssh Repositories
--------------------------------------

Sometimes custom recipes need access to private Git repositories that
are only available via SSH. The ci-scripts_ repository has logic to
handle this when a Factory has secrets created using a simple naming
convention.

.. _ci-scripts:
   https://github.com/foundriesio/ci-scripts/blob/master/lmp/bb-build.sh

Every secret matching the pattern ``ssh-*.key`` will be loaded into an
ssh-agent and ``ssh-known_hosts`` will be used to set the trusted
host keys for the Git server(s).

For the ``ssh-known_host`` it can be generated like this::

  $ ssh-keyscan github.com > /tmp/ssh-known_hosts

For example, a private GitHub repository could be accessed with::

  $ fioctl secrets update ssh-github.key==/tmp/ssh-github.key
  $ fioctl secrets update ssh-known_hosts==/tmp/ssh-known_hosts

At that point new CI jobs will be able to access recipes that have
``SRC_URI`` items like::

  SRC_URI = "git://git@github.com/<repo>;protocol=ssh;branch=main"
