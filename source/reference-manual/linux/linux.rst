.. _ref-linux:

Linux microPlatform
===================
The Foundries.io™ Linux® microPlatform (LmP) is an extensible software and hardware platform.
The LmP makes it easier to develop, secure, and maintain Internet-connected, Linux-based embedded devices.

The LmP is based on `OpenEmbedded`_ / `Yocto Project`_,
adding a select set of board support package layers to enable popular development boards.

Though the `Linux kernel`_ and software used for LmP builds may contain out-of-tree patches or features,
a fundamental goal is to run as close to the latest software as possible so that you can benefit from the latest changes.

In a Factory, the LmP is the baseline software stack, meant to be extended by you.
The LmP is open source software, and maintained by Foundries.io on `GitHub`_.

.. seealso::
   :ref:`lmp-customization` introduces ways it can be tailored to your needs.

.. toctree::
   :maxdepth: 1

   linux-supported
   linux-repo
   development-tags
   linux-dev-container
   linux-kernel
   linux-lmp-fs
   linux-layers
   linux-distro
   linux-wic-installer
   linux-persistent-log
   linux-net-debug
   linux-disk-encryption
   linux-update
   linux-dev-mode
   linux-oss-compliance
   factory-device-reset
   building-sdk
   toolchain

.. _OpenEmbedded: https://www.openembedded.org/wiki/Main_Page
.. _Yocto Project: https://www.yoctoproject.org
.. _Linux kernel: https://www.kernel.org
.. _GitHub: https://github.com/foundriesio
