.. highlight:: sh

.. _tutorial-dtls:

LWM2M System With DTLS
======================

This page describes how to enable DTLS-based LWM2M communication
between the gateway and IoT devices in the basic system you've already
set up.

.. important::

   These instructions assume you are using an nRF52840 based board;
   the extra code needed to enable DTLS doesn't fit on nRF52832.

.. warning::

   This is an experimental feature, with important security limitations.

   - The firmware update procedure uses plain HTTP, rather than LWM2M
     over DTLS. This leaks the contents of the updated firmware
     binary. (This can be used in denial of service and information
     disclosure attacks, but the MCUBoot binary will still refuse to
     boot unsigned binaries.)

   - The Leshan server still allows unauthenticated HTTP access to the
     IoT devices via its user interface and REST API. For example,
     this is used below to provision the device token, which leaks it
     over the local network to any eavesdropper. It also allows
     interacting with any device objects using an unauthenticated and
     unencrypted interface.

Generate and Flash Credentials Partition
----------------------------------------

You first need to generate a binary blob containing device credentials
to use, and flash it onto the device.

From the ZMP installation directory, run a command like this::

  ./zmp-samples/dm-lwm2m/scripts/gen_cred_partition.py --device-id=deadbeef --device-token=000102030405060708090a0b0c0d0e0f --output=cred.bin

The arguments are as follows.

- ``--device-id`` is a public identifier for the device.
  This is currently limited to eight hexadecimal characters.
- ``--device-token`` is a secret, device-specific token value (i.e.,
  the token must be different for each device on the network). This is
  a sequence of 32 two-character hexadecimal values, each representing
  a byte. In the above example, the first byte is 0x00, the second is
  0x01, etc.
- ``--output`` is the output file which will contain the binary.

Now flash the partitition to your device. Inspect your board's device
tree in the build directory for its correct location on the device
flash.

Build and Flash IoT Device With DTLS Enabled
--------------------------------------------

You now need to re-build and re-flash the application with DTLS
enabled, along with the credentials partition (the location of the
credentials partition is set by your board's device tree overlay
file)::

  west build -s zmp-samples/dm-lwm2m -d build-lwm2m-dtls -- -DOVERLAY_CONFIG=overlay-dtls.conf
  west sign -t imgtool -d build-dm-lwm2m-dtls -- --key mcuboot/root-rsa-2048.pem
  west flash -d build-dm-lwm2m-dtls --hex-file zephyr.signed.hex

Provision Leshan With Device Token
----------------------------------

Now use the Leshan web interface to provision the device ID and
token. If using the demonstration server, this interface is available
here:

https://mgmt.foundries.io/leshan/#/security

Use the System
--------------

You should now be able to use the system with DTLS enabled in
:ref:`same ways as the basic system <tutorial-basic-use>`.
