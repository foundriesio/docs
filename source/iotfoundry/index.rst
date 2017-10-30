.. _iotfoundry-top:

End-to-end Demonstration Systems
================================

The IoT Foundry provides IoT platform demonstration systems with
end-to-end connectivity. It is comprised of:

- A :ref:`linux-top` build and containerized gateway applications for
  cloud data and device management systems,
- Demonstration apps based on the :ref:`zephyr-top`, which support
  cloud data and device management systems, and connect to the cloud
  through the gateway.

Using these systems, you can exchange telemetry data with the cloud,
and perform firmware over the air (FOTA) device updates.

We continuously test and maintain these systems, and keep them
synchronized with the upstream projects they depend on.

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
