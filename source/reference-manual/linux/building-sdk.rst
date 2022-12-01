.. _ref-building-sdk:

Building SDK
============

The Yocto Project Standard SDK is a development environment composed by:

* toolchain
* debug tools
* sysroot (created based on the SDK image)

The SDK is used to replicate the tools and files from the target image,
but without depending on BitBake.
For details on what is SDK
and a complete description on how to work with SDK,
visit
`Yocto Project Application Development and the Extensible Software Development Kit <https://docs.yoctoproject.org/sdk-manual/index.html>`_.

The LmP can be configured to
create a SDK install script of the same rootfs image
built by the CI.
The SDK install script is the one created by
``bitbake <image> -c populate_sdk``.

When the ``lmp:params:BUILD_SDK`` is set
and a new target is created,
the SDK install script is also built.

This configuration increases the build time,
so enable the variable
only when a new SDK install script is needed.

Change the file
``ci-scripts/factory-config.yml``
to include the variable ``BUILD_SDK: "1"``
whenever a new SDK install script is needed,
as the following example.

.. prompt:: text

  lmp:
    params:
        BUILD_SDK: "1"

The SDK image is available
under ``SDK`` folder.

.. figure:: /_static/reference/sdk-artifact.png
   :align: center

   Where to find the SDK install script

To install the SDK, follow the Yocto Project
`instructions <https://docs.yoctoproject.org/singleindex.html#using-the-sdk-toolchain-directly>`_.
