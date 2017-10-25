.. _linux-top:

Linux microPlatform
===================

The Open Source Foundries Linux microPlatform is an extensible
software and hardware platform that makes it easier to develop,
secure, and maintain Internet-connected Linux-based embedded devices.

The Linux microPlatform is based on `Open Embedded`_, and adds a
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
   :maxdepth: 1

   getting-started
   iot-gateway
   bt-joiner

.. _Open Embedded: https://www.openembedded.org/wiki/Main_Page
.. _Linux kernel: https://www.kernel.org
.. _Docker containers: https://www.docker.com
