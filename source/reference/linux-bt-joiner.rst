.. _ref-linux-bt-joiner:

Linux microPlatform bt-joiner Container
=======================================

This page provides additional information on the ``bt-joiner`` Linux
microPlatform container which is provided by Open Source
Foundries. This container is used to provide IPv6 connectivity over
Bluetooth Low Energy to Zephyr microPlatform devices in the system
described in :ref:`tutorial-basic`.

.. _ref-linux-bt-joiner-whitelist:

Whitelist Setup for IoT Gateway
-------------------------------

Follow these instructions to set up a 6LoWPAN Bluetooth device
whitelist. This lets you configure your gateway device so that it only
attempts to connect to a subset of the Bluetooth devices in its
vicinity. This can be useful to avoid interfering with other gateways
or unrelated devices.

.. note::

   It's helpful to power off any IoT devices in your area prior to
   starting.

Enable the whitelist feature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable the whitelist, simply enable the whitelist function by
modifying the file ``bluetooth_6lowpand.conf`` in the
``gateway-ansible`` repository.  You'll want to set ``USE_WL`` to
``1``, and add a ``WL=IOT_DEVICE_MAC_ADDRESS`` line for each IoT
device you wish to whitelist.

Then redeploy the container on your gateway device, e.g. by using the
Ansible playbook provided in that repository.

How to Find Devices for the Whitelist
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that the whitelist is enabled, you can find the beaconing devices
by running the following command in the gateway's console::

    sudo hcitool lescan

While leaving this command running, power on the IoT devices
you wish to add to the whitelist. You should see an additional line
appear as each device is powered on.

The colon-separated list of hexadecimal numbers before each line
containing ``XXX IPSP node`` is that device's Bluetooth address. You can
add an address as a WL entry in ``bluetooth_6lowpand.conf`` to
whitelist the device.

For example, to whitelist a device with address ``D6:E7:D2:E8:6C:9F``,
add the following line to ``bluetooth_6lowpand.conf``::

  WL=D6:E7:D2:E8:6C:9F

Disable the whitelist feature
+++++++++++++++++++++++++++++

To turn off the whitelist feature, set ``USE_WL`` to ``0`` in
``bluetooth_6lowpand.conf``, then redeploy the container.
