.. highlight:: sh

.. _tutorial-dtls:

LWM2M System With DTLS
======================

This page describes how to enable DTLS-based LWM2M communication
between the gateway and IoT devices in the basic system you've already
set up.

These instructions assume you are using a BLE Nano 2.

.. warning::

   This is an experimental feature, with important security limitations.

   - The application implementation currently does not use a
     high-quality source of random values. Random values are commonly
     used throughout the DTLS protocol for various security
     properties.

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

Generate Credentials Partition
------------------------------

You first need to generate a binary blob containing device credentials
to use.

From the ZMP installation directory, run a command like this::

  ./zephyr-fota-samples/dm-lwm2m/scripts/gen_cred_partition.py --device-id=deadbeef --device-token=000102030405060708090a0b0c0d0e0f --output=cred.bin

The arguments are as follows.

- ``--device-id`` is a public identifier for the device.
  This is currently limited to eight hexadecimal characters.
- ``--device-token`` is a secret, device-specific token value (i.e.,
  the token must be different for each device on the network). This is
  a sequence of 32 two-character hexadecimal values, each representing
  a byte. In the above example, the first byte is 0x00, the second is
  0x01, etc.
- ``--output`` is the output file which will contain the binary.

Build and Flash IoT Device With DTLS Enabled
--------------------------------------------

Again from the ZMP installation directory, you now need to re-build
and re-flash the application with DTLS enabled, along with the
credentials partition::

  rm -rf outdir/zephyr-fota-samples/dm-lwm2m/nrf52_blenano2
  ./zmp build -b nrf52_blenano2 --conf-file "prj_dtls.conf boards/nrf52_blenano2.conf" zephyr-fota-samples/dm-lwm2m
  ./zmp flash -b nrf52_blenano2 zephyr-fota-samples/dm-lwm2m
  pyocd-flashtool -se -t nrf52 --address 0x7f000 cred.bin

Provision Leshan With Device Token
----------------------------------

Now use the Leshan REST API to provision the device ID and token as in
the following command line. (Make sure to change each occurrence of
``deadbeef`` to your device ID, and the key from ``000102...0f`` to
the key value you chose earlier.)

As noted above, this command line uses HTTP, and thus leaks the key,
for example to any eavesdropper on the local network::

  curl -v -X PUT -H "Content-Type: application/json" -d "{\"endpoint\":\"deadbeef\",\"psk\":{\"identity\":\"deadbeef\",\"key\":\"000102030405060708090a0b0c0d0e0f\"}}" http://localhost:8081/api/security/deadbeef

Use the System
--------------

You should now be able to use the system with DTLS enabled in
:ref:`same ways as the basic system <tutorial-basic-use>`.
