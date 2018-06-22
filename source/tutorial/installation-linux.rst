.. highlight:: sh

.. _tutorial-linux:

Install Linux microPlatform
===========================

The Linux microPlatform is split into two parts:

1. A *base system*, which is built using OpenEmbedded / Yocto. It
   provides a minimal runtime for application development which is
   over the air updatable.

2. Applications, which are developed and deployed as *containers*
   running on the base system. Application updates are accomplished by
   running updated containers. Currently, Docker containers are
   supported.

.. figure:: /_static/tutorial/linux-microplatform.png
   :alt: Linux microPlatform block diagram
   :align: center
   :width: 5in

   Linux microPlatform

This document describes how to:

- Install the base system onto your device and connect to its console.

- Connect the device to the network.

- Run the nginx web server in a container on the device, demonstrating
  application deployment.

(Later on in the Getting Started Tutorial, you'll replace the simple
nginx container with several different containers to turn your Linux
microPlatform device into an LWM2M gateway for your IoT devices.)

.. important::

   Make sure you've obtained dependencies as described in
   :ref:`tutorial-dependencies` before continuing.

.. _tutorial-linux-base:

Install Base microPlatform
--------------------------

You'll start by installing the base microPlatform and connecting to
your device's console.

Instructions for officially supported boards are listed
here. Currently, this is limited to the Raspberry Pi 3 Model B.

- :ref:`tutorial-linux-rpi3`

(If you're using another board, see :ref:`ref-linux-targets` and
:ref:`ref-linux-building` in the reference manual for more
information.)

.. _tutorial-linux-net:

Connect to the Network
----------------------

At this point, you should have shell access to your device.  If you've
already got a network connection as well, you can skip this section.

Option 1: WiFi
~~~~~~~~~~~~~~

Run this command from your Linux microPlatform device console to
connect to a WiFi network::

    sudo nmcli device wifi connect NETWORK_SSID password NETWORK_PASSWORD

Where ``NETWORK_SSID`` is your WiFi network's SSID, and
``NETWORK_PASSWORD`` is the password.

(The default password is ``osf``; you should change it before
connecting to the network, of course.)

Option 2: Ethernet
~~~~~~~~~~~~~~~~~~

Ethernet with DHCP works out of the box on all supported
boards. Simply connect an Ethernet cable.

Test Your Connection
~~~~~~~~~~~~~~~~~~~~

Test your Linux microPlatform device's network connection any way you
would like. For example::

    ping -c 3 opensourcefoundries.com

.. _tutorial-linux-ping:

Ping Your Device
----------------

You now need to find your device's Zeroconf hostname or IP address, so
you can load the nginx splash page in your workstation's browser in
the next step.

Option 1: Zeroconf
~~~~~~~~~~~~~~~~~~

**On Raspberry Pi 3**::

  ping -c 3 raspberrypi3-64.local

**On other boards**:

Linux microPlatform devices attempt to make themselves available on
the local network using Zeroconf [#zeroconf]_ at ``hostname.local``.
You can get your device's hostname from the shell prompt.

For example, if your device's shell prompt looks like:

.. code-block:: none

   hostname:~$

Then try pinging your device **from your development workstation
shell** with::

    ping -c 3 hostname.local

If that works, go ahead and deploy the nginx container.

Option 2: By IP Address
~~~~~~~~~~~~~~~~~~~~~~~

To print global IPv4 addresses, run this **from your Linux
microPlatform device**::

    ip -4 addr show scope global

You can replace ``-4`` with ``-6`` for IPv6.

For example, in the following output::

  $ ip -4 addr show scope global
  2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
      inet 10.0.0.203/24 brd 10.0.0.255 scope global dynamic eth0
         valid_lft 595628sec preferred_lft 595628sec
  6: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default
      inet 172.17.0.1/16 scope global docker0
         valid_lft forever preferred_lft forever

The device IP address is ``10.0.0.203``. (Ignore any ``dockerX``
networks).

To ping the device in the above example, run this **from your
development workstation shell**::

    ping -c 3 10.0.0.203

If that works, go ahead and deploy the nginx container.

.. _tutorial-linux-nginx:

Deploy nginx Container
----------------------

You'll now finish installing the Linux microPlatform by deploying an
example containerized application on your device which provides an
nginx web server.

.. important::

   Run these commands on your Linux microPlatform device, **not your
   workstation**.

Option 1: Subscribers
~~~~~~~~~~~~~~~~~~~~~

First, log in to the Open Source Foundries subscriber container
registry::

    docker login hub.foundries.io --username=unused

The username is currently ignored, but you must provide a value. When
prompted for the password, enter your subscriber access token.

Then run the latest subscriber nginx container::

    docker run --name nginx-demo -p 80:80 hub.foundries.io/nginx:latest

Option 2: Public
~~~~~~~~~~~~~~~~

To run the latest public nginx container available on Docker Hub::

    docker run --name nginx-demo -p 80:80 opensourcefoundries/nginx:latest

Connect to nginx
~~~~~~~~~~~~~~~~

After the image is downloaded, the running container will stay
connected to your terminal.

You can now check that it's working by connecting to
http://your-device-hostname.local (for example,
http://raspberrypi3-64.local) or http://your-device-ip-address/ in
your browser.

You should see an nginx splash page load, as well as log messages
appearing in the terminal where you typed ``docker run``, like so:

.. figure:: /_static/tutorial/nginx-demo.png
   :alt: nginx splash page
   :align: center

   nginx splash page

Example terminal output::

  10.0.0.111 - - [09/Jan/2018:21:07:21 +0000] "GET / HTTP/1.1" 200 612 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36" "-"
  2018/01/09 21:07:22 [error] 7#7: *1 open() "/usr/share/nginx/html/favicon.ico" failed (2: No such file or directory), client: 10.0.0.111, server: localhost, request: "GET /favicon.ico HTTP/1.1", host: "raspberrypi3-64.local", referrer: "http://raspberrypi3-64.local/"
  10.0.0.111 - - [09/Jan/2018:21:07:22 +0000] "GET /favicon.ico HTTP/1.1" 404 571 "http://raspberrypi3-64.local/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36" "-"

Press Control-C to stop the container. You can now remove it using::

  docker rm nginx-demo

The Linux microPlatform is now successfully deployed on your
device.

Next Steps
----------

You can either continue the tutorial at :ref:`tutorial-zephyr`, or
learn more about the Linux microPlatform in :ref:`howto` and the
:ref:`ref-linux`.

.. include:: reporting-issues.include

.. rubric:: Footnotes

.. [#zeroconf]

   Zeroconf is a set of technologies that allows automatic discovery
   of systems and services available on a local area network. It helps
   by assigning a local address name (e.g. ``hostname.local``
   instead of ``192.168.1.10``), which can be used by other Zeroconf
   compatible services like Bonjour on macOS.

   Avahi, a free Zeroconf implementation, is available by default on
   the Linux microPlatform, making it easy for other
   Zeroconf-compatible hosts to locate the IP address assigned to the
   board.

   To use Zeroconf, simply use ``hostname.local`` in place of the
   board's IP address when that is needed.

.. _Open Source Foundries organization's registry:
   https://hub.docker.com/u/opensourcefoundries/
