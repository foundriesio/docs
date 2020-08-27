.. _ref-linux:

Advanced Topics
===============

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

The Linux microPlatform also provides reference applications as
`Docker containers`_ to enable gateway functionality, such as
IPv6/IPv4 routing and MQTT message brokering.

.. toctree::
   :maxdepth: 1

   linux-building
   linux-targets
   linux-kernel
   linux-persistent-log
   linux-dev-container
   linux-layers
   linux-repo
   linux-net-debug
   fioctl/fioctl
   device-tags
   advanced-tagging
   containers
   compose-apps
   app-conversion
   vpn
   aktualizr-lite
   secure-boot
   secure-element.050
   container-secrets
   factory-definition
   configuration-management
   device-testing
   offline-keys
   docker-apps

.. _OpenEmbedded: https://www.openembedded.org/wiki/Main_Page
.. _Yocto: https://www.yoctoproject.org
.. _Linux kernel: https://www.kernel.org
.. _Docker containers: https://www.docker.com
