.. _ref-linux:

Linux microPlatform Reference Manual
====================================

The Open Source Foundries Linux microPlatform is an extensible
software and hardware platform that makes it easier to develop,
secure, and maintain Internet-connected Linux-based embedded devices.

.. note::

   Just getting started? Check out :ref:`tutorial-linux` in the
   :ref:`tutorial`.

The Linux microPlatform is based on `OpenEmbedded`_ / `Yocto`_, and adds a
select set of board support package layers to enable popular
development boards.

Though the `Linux kernel`_ and software used for
any on of the microPlatform builds may contain out-of-tree patches or
features, a fundamental goal is to run as close to the tip, or latest
software, as possible so that users of the Linux microPlatform can
benefit from the latest changes.

The Linux microPlatform also provides reference applications as
`Docker containers`_ to enable gateway functionality, such as
IPv6/IPv4 routing and MQTT message brokering.

.. toctree::

   linux-building
   linux-targets
   linux-kernel
   linux-bt-joiner
   linux-dev-container
   linux-layers
   linux-repo
   linux-ota

.. _OpenEmbedded: https://www.openembedded.org/wiki/Main_Page
.. _Yocto: https://www.yoctoproject.org
.. _Linux kernel: https://www.kernel.org
.. _Docker containers: https://www.docker.com
