.. _iotfoundry-top:

End-to-end Demonstration Systems
================================

The IoT Foundry provides IoT platform demonstration systems with
end-to-end connectivity. It is comprised of:

- Containers for cloud data and device management systems,
- a Basic IoT Gateway based on the :ref:`linux-top`, and
- demonstration apps based on the :ref:`zephyr-top`, which support
  cloud data and device management systems, and connect to the cloud
  through the gateway.

We continuously test and maintain these systems, and keep them
synchronized with the upstream projects they depend on.

The two end-to-end demonstration systems we currently support are:

HTTP / MQTT via Hawkbit
-----------------------
  .. toctree::
     :maxdepth: 1

     hawkbit-howto
     hawkbit-appendix

CoAP / LWM2M via Leshan
-----------------------

  .. toctree::
     :maxdepth: 1

     lwm2m-howto
     lwm2m-appendix
