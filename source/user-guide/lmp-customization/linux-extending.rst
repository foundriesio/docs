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

Add "stress-ng" to the package list::

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

Once completed and the update is applied, the device will reboot.
This behavior is customizable; you can apply rules to determine when devices should restart.
Once restarted, the ``stress-ng`` command will be available.

List of Available Recipes
-------------------------

OE provides a `tool`_ to search layers and recipes.
Remember to set the same branch name used by the current factory version.

.. _tool:
   https://layers.openembedded.org/layerindex/branch/master/layers/

Creating a Python3 Package from PyPi
------------------------------------

Some Python packages do not yet have a recipe for python3 in OE.
If this is the case with a desired package, use the template below to add a new package from PyPi.

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

Using the information and packages from the PyPi website, fill in the details about the new Python package

.. figure:: /_static/pypi-package.png
   :alt: Pypi package
   :align: center
   :width: 5in

   Pypi package

Update the following variables to reflect the details for the package you wish to create a recipe for.

#. ``DESCRIPTION``
#. ``HOMEPAGE``
#. ``LICENSE``
#. ``LIC_FILES_CHKSUM``
#. ``SRC_URI[md5sum]`` (md5sum of the download artifact from pypi)
#. ``SRC_URI[sha256sum]`` (sha256sum of the download artifact from pypi)
#. ``DEPENDS`` Dependencies resolved at do_configure
#. ``RDEPENDS`` Dependencies resolved at do_build

Using ``FEATURES`` to Configure LmP
-----------------------------------

Three "features" variables control and configure the build system: ``DISTRO_FEATURES``, ``IMAGE_FEATURES`` and ``MACHINE_FEATURES``.
Each one takes effect in a single aspect of the build system.

.. important::

    When changing ``DISTRO_FEATURES``, the distro changes.
    This results in the rebuilding of packages, which can take a while.

    When changing ``MACHINE_FEATURES``, the hardware description changes.
    This results in a different group of packages installing to the image.

    When changing ``IMAGE_FEATURES``, the image changes.
    This may reflect in the list of packages installed, or in the image configuration.

    Make sure you understand the result of any change.

``DISTRO_FEATURES`` is a list of configurations from a distro that reflects how some packages build or install.
While there is a list of `Yocto Project distro features`_ supported, the list can expand by including other meta layers.
For example, the distro features ``systemd`` or ``wayland`` define the list of packages to install, and configures how some packages build.
The distro feature ``modsign``,along with certificates, signs the kernel modules.

The default value used by LmP is defined in  ``meta-lmp/meta-lmp-base/conf/distro/include/lmp.inc``.
This can be customized by architecture, machine, or any other override.
To customize, use ``DISTRO_FEATURES:append = <value>`` to add a feature, and ``DISTRO_FEATURES:remove = <value>`` to remove one.
To remove a feature from an override list, use ``DISTRO_FEATURES:remove:<machine> = <value>``.

Use the command ``bitbake-getvar`` to see the value of some variables, and all the intermediate values::

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

Using ``DISTRO="lmp"`` generates the log.
``DISTRO_FEATURES`` can be changed by seven operations, and one of them is for an override (``tegra``).
The log also shows file path and line for each operation.

The line starting with ``DISTRO_FEATURES=`` show the variable value.

The Yocto Project also provides ``IMAGE_FEATURES`` and ``MACHINE_FEATURES``.
These are lists of features for the image and to describe the machine, respectively.
There is also lists of `Yocto Project image features`_ and `Yocto Project machine features`_ supported by the project.

The LmP uses the ``MACHINE_FEATURES`` for a machine to determine if a package gets included.
For example, the OP-Tee package is only included in an image if the target machine includes the feature ``optee`` within ``MACHINE_FEATURES``.

.. _Yocto Project distro features:
   https://docs.yoctoproject.org/kirkstone/ref-manual/features.html#distro-features

.. _Yocto Project image features:
   https://docs.yoctoproject.org/kirkstone/ref-manual/features.html#image-features

.. _Yocto Project machine features:
   https://docs.yoctoproject.org/kirkstone/ref-manual/features.html#machine-features

.. _ref-ug-private-repo:

Including Private Git+ssh Repositories
--------------------------------------

Custom recipes may need access to private Git repositories only available via SSH.
The ci-scripts_ repo has logic to handle this when a Factory has secrets created using a simple naming convention.

.. _ci-scripts:
   https://github.com/foundriesio/ci-scripts/blob/master/lmp/bb-build.sh

Secrets matching the pattern ``ssh-*.key`` are loaded into an ssh-agent, and ``ssh-known_hosts`` is used to sets the trusted host keys for the Git server(s).

To generate ``ssh-known_hosts``::

  $ ssh-keyscan github.com > /tmp/ssh-known_hosts

An example for accessing a private GitHub repo::

  $ fioctl secrets update ssh-github.key==/tmp/ssh-github.key
  $ fioctl secrets update ssh-known_hosts==/tmp/ssh-known_hosts

At this point new CI jobs will be able to access recipes that have ``SRC_URI`` items like::

  SRC_URI = "git://git@github.com/<repo>;protocol=ssh;branch=main"
