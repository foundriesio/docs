.. _linux-bt-joiner:

bt-joiner Container
===================

This page documents usage of the ``bt-joiner`` :ref:`gateway container
<iot-gateway>`.

.. _iot-gateway-whitelist:

Whitelist Setup for IoT Gateway
-------------------------------

Instructions follow setting up a 6LoWPAN Bluetooth device whitelist.

.. note::

   Prior to starting this walk through, please power off any IoT
   devices in your area.

Enable the whitelist feature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable the whitelist, simply enable the whitelist function by modifying
the bluetooth_6lowpand.conf.  You'll want to set USE_WL to 1 and add a
WL=MAC_ADDRESS line for each device you wish to whitelist.

How to Find Devices for the Whitelist
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that the whitelist is enabled, you can find the beaconing devices
using the following command::

    sudo hcitool lescan

While leaving this command running, power on the IoT device
you wish to add to the whitelist. You should see an additional line
appear as each device is powered on.

The following is an example of the output from this command (``XXX``
may vary)::

  LE Scan ...
  D6:E7:D2:E8:6C:9F (unknown)
  D6:E7:D2:E8:6C:9F XXX IPSP node

Make a note of the "XXX IPSP node" Bluetooth addresses.

Disable the whitelist feature
+++++++++++++++++++++++++++++

To turn off the whitelist feature, set USE_WL to '0' in bluetooth_6lowpand.conf.
