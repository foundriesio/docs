.. title:: Linux microPlatform Network Debugging
.. meta::
   :description: Learn how to debug network related issues on the Linux microPlatform using tcpdump in this guide for FoundriesFactory.

.. _howto-linux-net-debug:

Network Debugging
=================

This page provides information on debugging network related issues on
the Linux microPlatform.

Using ``tcpdump``
-----------------

The Linux microPlatform base image includes a ``tcpdump`` binary at
``/usr/sbin/tcpdump`` for use capturing traffic and diagnosing issues.
Note that ``/usr/sbin`` is not part of the :envvar:`PATH` environment
variable for the base image user, and you must run ``tcpdump`` as root.

Capturing Bluetooth 6lo Network Traffic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your Linux microPlatform device is acting as a gateway to IoT
devices connected via a Bluetooth link, you may want to restrict your
capture to just the traffic exchanged with those IoT devices.

To do this, use ``-i bt0`` when invoking ``tcpdump``:

.. code-block:: console

   $ sudo /usr/sbin/tcpdump -i bt0

Note that if you only have one such device, the network interface
will be torn down by the kernel if the Bluetooth link is lost. When
that happens, you'll see a message like this from tcpdump:

.. code-block:: none

   tcpdump: pcap_loop: The interface went down

The best workaround for this if you want to continue to capture
traffic on ``bt0`` for a Bluetooth device that resets and reconnects
is to have another device remain connected to your Linux microPlatform
gateway for the duration of the capture.

Capturing LAN Network Traffic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're using Ethernet, use ``-i eth0`` to view traffic exchanged
with the rest of the LAN:

.. code-block:: console

   $ sudo /usr/sbin/tcpdump -i eth0

You can use ``-i wlan0`` for wireless traffic.

Other Network Interfaces
~~~~~~~~~~~~~~~~~~~~~~~~

To view a complete list of network interfaces you can use with the
``-i`` option, run:

.. code-block:: console

   $ ip link show

One of these may be useful, for example, if you need to capture
traffic on a network device created for use with containers.

Capturing to a File
~~~~~~~~~~~~~~~~~~~

It is often convenient to capture traffic in a file for later
analysis, for example with tools such as Wireshark. Use ``-w
file.pcap`` when invoking ``tcpdump`` to save to a file named
``file.pcap``. For example, to capture traffic exchanged over the
``bt0`` interface to a file ``bt0.pcap``:

.. code-block:: console

   $ sudo /usr/sbin/tcpdump -i bt0 -w bt0.pcap

At time of writing, the version of tcpdump present in the Linux
microPlatform does not support the ``--print`` option. To capture to
file and view the text representation simultaneously, you can use a
pipeline like this:

.. code-block:: console

   $ sudo /usr/sbin/tcpdump -i bt0 -U -w - | tee bt0.pcap | sudo /usr/sbin/tcpdump -r -

External References
-------------------

- `tcpdump manual page`_
- `Wireshark documentation`_
- `Docker container networking`_

.. _Docker container networking:
   https://docs.docker.com/engine/userguide/networking/

.. _tcpdump manual page:
   https://www.tcpdump.org/tcpdump_man.html

.. _Wireshark:
   https://www.wireshark.org/

.. _Wireshark documentation:
   https://www.wireshark.org/docs/
