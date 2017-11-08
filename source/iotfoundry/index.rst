.. _iotfoundry-top:

End-to-end Demonstration Systems
================================

By following the earlier guides in this documentation, you now have:

- A :ref:`linux-top` build installed on your device, and access to
  containerized :ref:`IoT gateway <iot-gateway>` applications for
  cloud data and device management systems,
- A :ref:`zephyr-top` installation on your system, which includes
  sample applications provided by Open Source Foundries and an IoT
  device you have flashed with a simple sample application.

By following step-by-step instructions in the following pages, you can
combine these to create systems which exchange telemetry data between
your IoT device and the cloud, as well as perform firmware over the
air (FOTA) updates to your IoT device.

microPlatform subscribers have access to continuously tested and
maintained source code and binaries for these systems, which are kept
synchronized with changes to the upstream projects they depend on.
Publicly available versions are released up to every six months.

The two end-to-end demonstration systems we currently support are:

hawkBit FOTA and MQTT
---------------------

.. toctree::
   :maxdepth: 1

   hawkbit-howto
   hawkbit-appendix

LWM2M FOTA and Data
-------------------

.. toctree::
   :maxdepth: 1

   lwm2m-howto
   lwm2m-appendix
