.. highlight:: sh

.. _ref-linux-building:

Building the Linux microPlatform
================================

This is a guide for building the base Linux microPlatform from source
for Raspberry Pi 3. Additional information specific to other targets
is provided in :ref:`ref-linux-targets`.

This guide assumes the reader is familiar with basic concepts of
OpenEmbedded. It is not meant to be an introduction to the
OpenEmbedded / Yocto Project. If you're just getting started, it's
strongly recommended to begin with the documentation provided in
:ref:`ref-linux-building-ref`.

.. _ref-linux-building-hw:

Get Hardware
------------

You will need a x86 computer to develop on; Linux is currently
natively supported. On macOS and Windows, see
:ref:`ref-linux-dev-container` for information on setting up a
containerized Linux build environment.

You will also require at least 50GB of storage for a complete Linux
microPlatform build.

Set Up Build Environment
------------------------

On Debian-based Linux distributions, including Ubuntu, run::

   $ sudo apt-get install coreutils gawk wget git-core diffstat unzip \
       texinfo gcc-multilib build-essential chrpath socat cpio \
       openjdk-9-jre python python3 python3-pip python3-pexpect xz-utils \
       debianutils iputils-ping libsdl1.2-dev xterm \
       android-tools-fsutils repo whiptail

.. note::

   If you are running Ubuntu 16.04, make sure to enable the universe
   repository by adding following line to your
   :file:`/etc/apt/sources.list`:

   .. code-block:: none

      deb http://archive.ubuntu.com/ubuntu/ xenial universe

On other Linux distributions, please check the `Yocto Project Quick
Start Guide`_ for additional guidance.

.. _ref-linux-building-install:

Install the Linux microPlatform
-------------------------------

The Linux microPlatform sources can be placed in any directory on your
workstation, as long it provides enough disk space for the complete
build. This uses the Repo tool to fetch a variety of Git repositories
at known-good revisions, and keep them in sync as time goes on.

(If you're new to Repo and want to know more, see
:ref:`ref-zephyr-repo`.)

#. Make an installation directory for the Linux microPlatform, and
   change into its directory::

     mkdir lmp && cd lmp

   (You can also reuse an existing installation directory.)

#. Install update |version| using repo:

   .. parsed-literal::

      repo init -u https://github.com/foundriesio/lmp-manifest -b |repo_tag|
      repo sync

Set up Work Environment
-----------------------

Next, set up your work environment for building the source.

The supported ``MACHINE`` target used by this guide is
``raspberrypi3-64``. (For information on other hardware platforms, see
:ref:`ref-linux-targets`.)

The default distribution (``DISTRO``) is automatically set to ``lmp``,
which is provided by the meta-lmp layer (see
:ref:`ref-linux-layers` for more details).

Set up your work environment using the ``setup-environment`` script::

  MACHINE=raspberrypi3-64 source setup-environment [BUILDDIR]

If ``MACHINE`` is not provided, the script will list all possible
machines found in every enabled OpenEmbedded / Yocto Project layer,
and force one to be selected.  ``BUILDDIR`` is optional; if it is not
specified, the script will default to ``build-lmp``.

Build the lmp-gateway Image
---------------------------

You can build the Linux microPlatform gateway image by running::

  bitbake lmp-gateway-image

.. note::

   Depending on the amount of RAM and number of processors and cores
   in your system, the speed of your Internet connection, and other
   factors, the first build could take several hours. Subsequent
   builds run much faster since some artifacts are cached.

At the end of the build, your build artifacts will be found under
``deploy/images/raspberrypi3-64``. The artifact you will
use to flash your board is
``lmp-gateway-image-raspberrypi3-64.wic.gz``.

Install the lmp-gateway Image
-----------------------------

If you're using a Raspberry Pi 3, you can use the same procedure
outlined for prebuilt binaries in :ref:`tutorial-linux`. See
:ref:`ref-linux-targets` for additional information on other targets.

.. _ref-linux-building-ref:

References
----------

The following reference material on OpenEmbedded and Yocto is
recommended for those new to either project.

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
   https://www.yoctoproject.org/docs/current/brief-yoctoprojectqs/brief-yoctoprojectqs.html
.. _Yocto Project Reference Manual:
   https://www.yoctoproject.org/docs/current/ref-manual/ref-manual.html
.. _BitBake Manual:
   https://www.yoctoproject.org/docs/current/bitbake-user-manual/bitbake-user-manual.html
