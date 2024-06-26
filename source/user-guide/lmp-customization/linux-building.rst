.. highlight:: sh

.. _ref-linux-building:

Building From Source
====================

This is a guide for building the base Linux® microPlatform (LmP) from source for QEMU AARCH64 (Arm® 64).
Information specific to other targets is provided in :ref:`ref-linux-supported`.

This guide assumes familiarity with :term:`Open Embedded` concepts.
If you are just getting started with OpenEmbedded/the :term:`Yocto Project`, it is strongly recommended to begin with the documentation provided under :ref:`ref-linux-building-ref`.

 .. important::

  Locally built images are useful for testing and hardware enablement, but are not meant to be updated via OTA.
  For OTA support we recommend creating your own Factory and using our CI system.

.. _ref-linux-building-hw:

Hardware Requirements
---------------------

You will need a x86 computer to develop on;
Linux is currently natively supported.
On macOS and Windows, see :ref:`ref-linux-dev-container` on setting up a containerized Linux build environment.

You will also require at least 50GB of storage for a complete LmP build.

Setup the Build Environment
---------------------------

On Debian-based Linux distributions, including Ubuntu, run::

   $ sudo apt install coreutils gawk wget git diffstat unzip \
       texinfo g++ gcc-multilib build-essential chrpath socat cpio \
       openjdk-11-jre python2.7 python3 python3-pip python3-pexpect xz-utils \
       debianutils iputils-ping libsdl1.2-dev xterm libssl-dev libelf-dev \
       android-sdk-libsparse-utils ca-certificates repo whiptail

.. note::

   If you are running Ubuntu, make sure to enable the universe repository:

   .. code-block:: none

      sudo add-apt-repository universe

On other Linux distributions, please check the `Yocto Project Quick Start Guide`_ for guidance.

.. _ref-linux-building-install:

Install the LmP
---------------

Download the Layers
^^^^^^^^^^^^^^^^^^^^

The LmP sources can be placed in any directory on your workstation, as long it provides enough disk space for the complete build.
The `Google Repo`_ tool is used to fetch Git repos at known-good revisions, and keeps them in sync.

#. Make and enter an installation directory for the LmP::

     mkdir lmp && cd lmp

   .. note::

      You can also reuse an existing installation directory, or ``/build/lmp``
      if building inside the ``lmp-sdk`` container, as described at :ref:`ref-linux-dev-container`.

#. Install update |version| using :term:`Repo`:

   .. parsed-literal::

      repo init -u https://github.com/foundriesio/lmp-manifest -b |manifest_tag|
      repo sync

Setup Work Environment
^^^^^^^^^^^^^^^^^^^^^^

Next, set up your work environment for building the source.

The supported ``MACHINE`` target used by this guide is ``qemuarm64-secureboot``.
For information on other hardware platforms, see:ref:`ref-linux-supported`.

The default distribution variable, ``DISTRO``, is automatically set to ``lmp``.
This distro is provided by the `meta-lmp-base` layer (see :ref:`ref-linux-layers` for more details).

Set up your work environment using the ``setup-environment`` script::

  MACHINE=qemuarm64-secureboot source setup-environment [BUILDDIR]

If ``MACHINE`` is not provided, the script will list all machines from every enabled OpenEmbedded / Yocto Project layer, and force one to be selected.

``BUILDDIR`` is optional; if it is not specified, the script will default to ``build-lmp``.
Keep in mind that ``BUILDDIR`` must be within the ``lmp`` directory, otherwise your build will fail.

Build the Image
^^^^^^^^^^^^^^^

You can build the LmP base-console image by running::

  bitbake lmp-base-console-image

.. note::

   Depending on the resources available on your system, the speed of your internet connection, and other factors, the first build could take several hours.
   Subsequent builds run much faster since some artifacts are cached.

At the end of the build, your build artifacts will be found under ``deploy/images/raspberrypi3-64``.
The artifact you will use to flash your board is ``lmp-base-console-image-raspberrypi3-64.wic.gz``.

Install the Image
^^^^^^^^^^^^^^^^^

If you are using QEMU, follow the procedure outlined in the :ref:`ref-rm_qemu_arm64` flashing instructions.
See :ref:`ref-linux-supported` for additional information on other targets.

.. _ref-linux-building-ref:

Build and Install the LmP for your Factory
------------------------------------------

If you are already working with a Factory, you can instead download the source code for that factory with the following steps.

1. Make and enter an installation directory for the LmP for your ``<factory-name>``::

     mkdir <factory-name> && cd <factory-name>

2.  Install the ``<factory-name>`` meta-layers using repo:

   .. parsed-literal::

      repo init -u https://source.foundries.io/factories/<factory-name>/lmp-manifest.git -b main -m <factory-name>.xml
      repo sync

   The manifest ``<factory-name>.xml`` refers to all the LmP meta-layers and also to the ``<factory-name>`` specific repositories as described :ref:`ref-factory-sources`.

3.  Build the image for ``<factory-name>`` with :term:`bitbake`:

   .. parsed-literal::

      MACHINE=<machine-name> source setup-environment [BUILDDIR]
      bitbake lmp-factory-image

   The variable ``MACHINE`` should be set to a supported machine.
   See the current available option in :ref:`ref-linux-supported`.

   ``BUILDDIR`` is optional; in case it is not provided, the script default is ``build-lmp``.

   ``lmp-factory-image`` is the suggested default image, and can be customized with the steps from :ref:`ref-adding-packages-image`.

It is worth remembering that the ``bitbake`` step can take a while.
At the end of the build, your build artifacts is found under ``deploy/images/<machine-name>``.
The artifact you use to flash your board is ``lmp-base-console-image-<machine-name>.wic.gz``.

.. important::

   The local build of your Factory is great for developing and debugging and the results can be used on the host machine or deployed to a hardware board.
   However, the image created locally is not yet visible for the OTA system, and is only available for local use.

   When you push the changes to your Factory Git repos, it will trigger a new build.
   You can then flash and register your device following the instructions of :ref:`gs-flash-device` and :ref:`gs-register`.
   Then, you can take advantage of the OTA system.

References
----------

The following reference material on OpenEmbedded and the Yocto Project is recommended for those unfamiliar.

- `OpenEmbedded wiki`_
- `Yocto Project main page`_
- `Yocto Project Quick Start Guide`_
- `Yocto Project Reference Manual`_
- `BitBake Manual`_

.. _OpenEmbedded wiki:
    https://www.openembedded.org/wiki/Main_Page
.. _Yocto Project main page:
   https://www.yoctoproject.org/
.. _Yocto Project Quick Start Guide:
   https://docs.yoctoproject.org/kirkstone/brief-yoctoprojectqs/
.. _Yocto Project Reference Manual:
   https://docs.yoctoproject.org/kirkstone/ref-manual/
.. _BitBake Manual:
   https://docs.yoctoproject.org/bitbake/

.. _Google Repo:
   https://source.android.com/docs/setup/create/repo
