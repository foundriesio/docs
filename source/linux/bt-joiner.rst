.. _linux-bt-joiner:

bt-joiner Container
===================

This page documents usage of the ``bt-joiner`` :ref:`gateway container
<iot-gateway>`, which is part of the :ref:`linux-top`.

.. _iot-gateway-whitelist:

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

The following is an example of the output from this command when using
Bluetooth 6LoWPAN devices from the :ref:`zephyr-top` (``XXX`` may
vary)::

  LE Scan ...
  D6:E7:D2:E8:6C:9F (unknown)
  D6:E7:D2:E8:6C:9F XXX IPSP node

The colon-separated list of hexadecimal numbers before each "XXX IPSP
node" line is that device's Bluetooth address. You can add an address
as a WL entry in ``bluetooth_6lowpand.conf`` to whitelist the device.

For example, to whitelist the above example device, add the following
line to ``bluetooth_6lowpand.conf``::

  WL=D6:E7:D2:E8:6C:9F

Disable the whitelist feature
+++++++++++++++++++++++++++++

To turn off the whitelist feature, set ``USE_WL`` to ``0`` in
``bluetooth_6lowpand.conf``, then redeploy the container.
