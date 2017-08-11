Linaro Technologies Division (LTD)
==================================

This is the documentation for the Linaro Technologies Division.

Zephyr MicroPlatform
--------------------

The :ref:`zephyr-top` is an extensible software and hardware platform
that makes it easier to develop, secure, and maintain
Internet-connected embedded devices. The Zephyr MicroPlatform is based
on the `Zephyr <https://www.zephyrproject.org/>`_ real-time operating
system.

.. toctree::
   :hidden:

   zephyr/index

Linux MicroPlatform
-------------------

The :ref:`linux-top` is a minimal Linux distribution for deploying and
managing multi-tenant, containerized applications on Linux devices.
The Linux MicroPlatform is built using OpenEmbedded and adding a
select set of board support package layers for enabling some popular
development boards.  Though the Linux kernel and software used for any
on of the MicroPlatform builds may contain out-of-tree patches or
features, a fundamental goal is to run as close to the tip, or latest
software, as possible so that users of the Linux MicroPlatform can
benefit from the latest changes.

.. toctree::
   :hidden:

   linux/index

Basic IoT Gateway (BIG)
-----------------------

The :ref:`basic-iot-gateway-top` is built from the Linux MicroPlatform
and specific containers are added to enable gateway functionality,
such as IPv6/IPv4 routing and MQTT message brokering.

.. toctree::
   :hidden:

   BasicIoTGateway/index

End-to-end Opensource IoT Demonstrations Systems
------------------------------------------------

:ref:`iotfoundry-top` shows you how to combine the Zephyr MicroPlatform
and the Linux MicroPlatform along with server/cloud applications to
create complete systems.

With these systems, you can publish sensor data from devices to the
cloud and perform firmware over the air (FOTA) updates of the device
firmware.

.. toctree::
   :hidden:

   iotfoundry/index

.. The following bold text (and the list of todos themselves) only
   appear when todo_include_todos is True in conf.py.

.. ifconfig:: todo_include_todos is True

   **Documentation-wide TODO List**

.. todo::

   Add "advanced and special topics" Zephyr MicroPlatform docs:

   - Support a new device
   - Build developer docs
   - Add features to the tooling ("internals" docs, generally)
   - HLL support (uPython, JerryScript)
   - Cloud service integration

.. todolist::
