.. highlight:: sh

.. _iot-gateways-6lowpan_whitelist:

6LoWPAN Whitelist
=================

This document is intended as a walk-through for setting up a 6LoWPAN
Bluetooth device whitelist using the joiner script here:

https://raw.githubusercontent.com/linaro-technologies/iot-gateway-files/master/bluetooth_6lowpand.sh

.. warning::

   This guide assumes you are working on an IoT Gateway device such as
   a 96Boards Hikey using a prebuilt image from here:

   http://builds.96boards.org/snapshots/reference-platform/debian-iot/

   These images will include the above script as
   ``/usr/bin/bluetooth_6lowpand``

.. note::

   Prior to starting this walk through, please power off any IoT
   devices in your area.

.. contents::
   :local:

Enable the whitelist feature
----------------------------

To enable the whitelist, use the following commands::

    sudo service bluetooth_6lowpand stop
    sudo bluetooth_6lowpand --whitelist_on
    sudo bluetooth_6lowpand --whitelist_clear
    sudo service bluetooth_6lowpand start

How to Find Devices for the Whitelist
-------------------------------------

Now that the whitelist is enabled, you can find the beaconing devices
using the following command::

    sudo hcitool lescan

While leaving this command running, power on the :ref:`iot-devices`
you wish to add to the whitelist. You should see an additional line
appear as each device is powered on.

The following is an example of the output from this command::

  LE Scan ...
  D6:E7:D2:E8:6C:9F (unknown)
  D6:E7:D2:E8:6C:9F Linaro IPSP node

Write down all of the "Linaro IPSP node" Bluetooth addresses, as you
will need these for the next steps.

Add a Device to the Whitelist
-----------------------------

Next, add each Bluetooth address to the whitelist with the following
command::

    # btaddress is formatted: ##:##:##:##:##:##
    sudo bluetooth_6lowpand --whitelist_add <btaddress>

As you run each command, you may notice that the bluetooth_6lowpand
service will join the device during its next scan.

==================================================

**Once you've added all of the devices, you're done!  If you require
no further changes, you can skip the rest of this guide.**

==================================================


Additional Commands
-------------------

List the devices in the whitelist
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To list the devices currently in the bluetooth_6lowpand whitelist, use
the following command::

    sudo bluetooth_6lowpand --whitelist_list

Remove a device from the whitelist
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To remove a device from the whitelist, use the following command::

    # btaddress is formatted: ##:##:##:##:##:##
    sudo bluetooth_6lowpand --whitelist_remove <btaddress>

.. note::

   If a device is currently joined to the 6lowpan network, it will be
   disconnected once this command is run.

Disable the whitelist feature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To turn off the whitelist feature, use the following commands::

    sudo service bluetooth_6lowpand stop
    sudo bluetooth_6lowpand --whitelist_off
    sudo service bluetooth_6lowpand start
