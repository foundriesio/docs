.. highlight:: sh

.. _ref-linux-building:

Building From Source: Development Container
===========================================

This is a guide for building the Linux® microPlatform (LmP) from source using a Docker container.
The container uses Ubuntu and provides the build environment for the LmP.

.. tip::
   This is the same container used by the FoundriesFactory™ Platform CI,
   and is the recommendecd environment for building local LmP images.


This guide assumes some familiarity with :term:`Open Embedded` concepts.
If you are new to Open Embedded/the :term:`Yocto Project`,
we strongly recommend beginning with the documentation provided under :ref:`ref-linux-building-ref`.

.. important::
   Locally built images are useful for testing and hardware enablement, but are not meant to be updated via OTA.
   For OTA support, use our CI system.

.. _ref-linux-building-hw:

Requirements
------------

* Minimum 50GB of storage for a complete LmP build
* `Docker Installed`_.

Build and Install the LmP for your Factory
------------------------------------------

If you are already working with a Factory, you can download the source code with the following steps:

1. Make and enter an installation directory for the LmP with your ``<factory-name>``:

   .. code-block:: console

      $ mkdir <factory-name> && cd <factory-name>

2. Install the ``<factory-name>`` meta-layers using repo:

   .. code-block:: console
  
      $ repo init -u https://source.foundries.io/factories/<factory-name>/lmp-manifest.git -b main -m <factory-name>.xml
      $ repo sync

   The manifest ``<factory-name>.xml`` refers to all the LmP meta-layers and also to the ``<factory-name>`` specific repositories as described :ref:`ref-factory-sources`.

3. Build the image for ``<factory-name>`` with :term:`bitbake`:

   .. parsed-literal::

      MACHINE=<machine-name> source setup-environment [BUILDDIR]
      bitbake lmp-factory-image

   Set ``MACHINE`` to a supported machine.
   See the current available options in :ref:`ref-linux-supported`.

   ``BUILDDIR`` is optional; the script defaults to ``build-lmp``.

   ``lmp-factory-image`` is the suggested default image.
   Customize it with the steps from :ref:`ref-adding-packages-image`.

   .. tip::
      The ``bitbake`` step can take a while.

Your build artifacts will be under ``deploy/images/<machine-name>``.
The artifact you use to flash your board is ``lmp-factory-image-<machine-name>.wic.gz``.

.. important::

   While the local build is great for developing and debugging,
   the image is not visible for the OTA system, and is for local use.

   When you push the changes to your Factory Git repos, it will trigger a new build.
   You can then flash and register your device following the instructions of :ref:`gs-flash-device` and :ref:`gs-register`.
   Then, you can take advantage of the OTA system.

Build and Install Without a Factory
-----------------------------------

Setup
^^^^^

#. Create local folders for ``sstate-cache``, ``downloads`` and ``build`` to save the build outside the container:

   .. code-block:: console

      $ mkdir -p ~/lmp/sstate-cache ~/lmp/downloads ~/lmp/build

#. Run |version| of the container as the ``builder`` user:

   .. parsed-literal::

      $ docker run --rm -u builder --name lmp-sdk -v ~/lmp/build:/build/lmp -v ~/lmp/sstate-cache:/build/lmp/sstate-cache -v ~/lmp/downloads:/build/lmp/downloads -it hub.foundries.io/lmp-sdk:|docker_tag|

#. Setup Git inside the container (required by ``repo``)
   
   .. code-block:: console

      $ git config --global user.name "Your Full Name"
      $ git config --global user.email "your-email-address@example.com"

.. _ref-linux-building-install:

Download the Layers
^^^^^^^^^^^^^^^^^^^

The `Google Repo`_ tool fetches Git repos at known-good revisions, and keeps them in sync.

#. Enter the build directory:

   .. code-block:: console

     $ cd build/lmp

#. Fetch release |version| using :term:`Repo`:

   .. parsed-literal::

      $ repo init -u https://github.com/foundriesio/lmp-manifest -b |manifest_tag|
      $ repo sync

Setup the Build Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, set up your environment for building the source.

.. tip::
   For information on supported hardware platforms, see :ref:`ref-linux-supported`.

The distribution variable ``DISTRO`` is ``lmp`` by default.
This distro comes from the `meta-lmp-base` layer (see :ref:`ref-linux-layers` for more details).

Set up your environment using the ``setup-environment`` script::

  MACHINE=qemuarm64-secureboot source setup-environment [BUILDDIR]

If ``MACHINE`` is not provided, the script will list all machines from the enabled layers and prompt you to select one.

``BUILDDIR`` is optional; if not specified, the script defaults to ``build-lmp``.
Keep in mind that ``BUILDDIR`` must be within the ``lmp`` directory, otherwise your build will fail.

Build the Image
---------------

To build the LmP base-console, run:

.. code-block:: console

   $ bitbake lmp-base-console-image

.. note::

   Depending on your system's resources, the speed of your internet connection, and other factors, the first build could take several hours.
   Subsequent builds are much faster since some artifacts are cached.

At the end of the build, your build artifacts will be under ``deploy/images/<MACHINE>``.
The artifact you will use to flash your board will be something similar to ``lmp-base-console-image-<MACHINE>.wic.gz``.

Install the Image
^^^^^^^^^^^^^^^^^

* For QEMU, follow the procedure outlined in the :ref:`ref-rm_qemu_arm64` flashing instructions.
* For other targets, see :ref:`ref-linux-supported` for their instructions.



.. _ref-linux-building-ref:

References
----------

We recommend the following reference material on OpenEmbedded and the Yocto Project:

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
   https://docs.yoctoproject.org/scarthgap/brief-yoctoprojectqs/
.. _Yocto Project Reference Manual:
   https://docs.yoctoproject.org/scarthgap/ref-manual/
.. _BitBake Manual:
   https://docs.yoctoproject.org/bitbake/
.. _Docker Installed:
   https://docs.docker.com/get-docker/
.. _Google Repo:
   https://source.android.com/docs/setup/create/repo
