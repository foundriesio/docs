Docker App Store
================

The Community Factory includes several examples of containers that can be
run on a device based on `Docker App`_.

shellhttpd
~~~~~~~~~~
This is a minimal container that runs a web server using bash and netcat.
Its useful for quick sanity checks of platform functionality.

x-kiosk
~~~~~~~
Runs the chromium browser inside a container and displays a website.

openthread-gateway
~~~~~~~~~~~~~~~~~~
This docker-app establishes the services needed to enable routing of OpenThread
traffic to your standard network. This includes DNS64, CoAP-HTTP proxy,
and NAT64 for IPv6->IPv4 traffic translation.

   .. note::

     This requires an OpenThread compatible NCP to be configured and installed
     on your machine.

.. _Docker App:
   https://github.com/docker/app
