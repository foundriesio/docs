.. _ref-linux:

Linux microPlatform
===================
The Foundries.io Linux microPlatform is an extensible
software and hardware platform that makes it easier to develop,
secure, and maintain Internet-connected Linux-based embedded devices.

The Linux microPlatform is based on `OpenEmbedded`_ / `Yocto`_, and adds a
select set of board support package layers to enable popular
development boards.

Though the `Linux kernel`_ and software used for
any on of the microPlatform builds may contain out-of-tree patches or
features, a fundamental goal is to run as close to the tip, or latest
software, as possible so that users of the Linux microPlatform can
benefit from the latest changes.

In a FoundriesFactory, the Linux microPlatform is the baseline software
stack which is meant to be extended by the user. It is open source software,
and maintained by Foundries.io on `GitHub`_.

.. toctree::
   :maxdepth: 1

   linux-supported
   linux-repo
   linux-dev-container
   linux-building
   linux-kernel
   linux-layers
   linux-wic-installer
   linux-persistent-log
   linux-net-debug
   linux-update
   linux-extending

.. _OpenEmbedded: https://www.openembedded.org/wiki/Main_Page
.. _Yocto: https://www.yoctoproject.org
.. _Linux kernel: https://www.kernel.org
.. _Docker containers: https://www.docker.com
.. _GitHub: https://github.com/foundriesio
