.. _howto-mcuboot-keys:

Zephyr microPlatform MCUboot Key Provisioning HOWTO
===================================================

This page explains how to use your own firmware signing key pair to
secure the boot process on your Zephyr microPlatform devices.

Requirements
------------

You must have the Zephyr microPlatform installed on your system; see
instructions in :ref:`tutorial-zephyr` for details.

Any board supported by the Zephyr microPlatform can be used with these
instructions.

Generate Keys
-------------

From the Zephyr microPlatform installation directory, generate an RSA
2048 key pair by running:

.. code-block:: console

   $ ./mcuboot/scripts/imgtool.py keygen -k my-secret-key.pem -t rsa-2048

(This is the default key type used by MCUboot; if you configured
MCUboot differently, you need to adjust the ``-t`` option.)

.. important::

   The contents of the file my-secret-key.pem must be stored securely
   and kept secret.

Configure MCUboot to Use Your Key
---------------------------------

Now edit the MCUboot configuration to set the
``CONFIG_BOOT_SIGNATURE_KEY_FILE`` Kconfig value to point to your .pem
file, which you created in the previous step. There are multiple ways
to do this, e.g.:

1. To update your build directory :file:`.config`, setting up the key for
   just this build::

     ./zmp configure -o mcuboot YOUR_APP_NAME

   Search for the Kconfig option (type ``/`` to enter the search view,
   enter the config option name, then hit enter to select it and enter
   the interface to change its value).

2. To make the change permanent and part of your MCUboot repository,
   edit :file:`mcuboot/boot/zephyr/prj.conf` to set the value, and
   commit the change. (This means all users of your Git tree need
   access to the key, though.)

Which one you choose depends on your circumstances and
requirements. If in doubt, use choice 1 to produce an MCUboot binary
that you can then save and distribute to any other users, etc. who
need to boot images signed by your private key.

Build App With Custom MCUboot image
-----------------------------------

You can now rebuild your Zephyr microPlatform application binary,
along with a customized MCUboot binary which trusts your public
key. Here is an example building the ``zephyr-fota-samples/dm-lwm2m``
application for the ``nrf52_blenano2`` board using the :ref:`zmp
<ref-zephyr-zmp>` tool:

.. code-block:: console

   $ ./zmp build -K my-secret-key.pem -b nrf52_blenano2 zephyr-fota-samples/dm-lwm2m

The important files this generates (when combined with the previous
steps) are:

- A custom MCUboot binary which trusts your public key in
  :file:`outdir/zephyr-fota-samples/dm-lwm2m/nrf52_blenano2/mcuboot/zephyr/zephyr.bin`. Use
  this binary when flashing devices you are going to deploy to the
  field.

- A Zephyr binary which is signed with your private key in
  :file:`outdir/zephyr-fota-samples/dm-lwm2m/nrf52_blenano2/app/zephyr/dm-lwm2m-nrf52_blenano2-signed.bin`. You
  can distribute this binary in FOTA updates.

To verify your setup, flash the custom MCUboot to your board, along
with the signed binary into the main firmware image area. For example,
using the ``zmp`` tool:

.. code-block:: console

   ./zmp flash -b nrf52_blenano2 zephyr-fota-samples/dm-lwm2m

Appendix: Boot Process Overview
-------------------------------

If you're unfamiliar with the overall boot process, this section may
help.

When your Zephyr microPlatform device boots, MCUboot_ checks for a
cryptographically signed firmware update, then installs and runs it if
one is available. Simplified, the boot process looks like this:

.. figure:: /_static/howto/mcuboot-boot.png
   :align: center

   Zephyr microPlatform boot decision tree.

The firmware update signature check uses a public key stored in the
MCUboot binary running on the device. MCUboot checks that the firmware
update is signed by the corresponding private key before booting
it. This mitigates against attacks which try to boot untrusted
firmware on your device.

.. figure:: /_static/howto/device-flash.png
   :align: center

   Zephyr microPlatform device flash layout.

To make getting started easy, the MCUboot repository's source code
contains a default public key, along with its private key in a data
file. Since the private key is not secret, this is not secure to use
in production. When deploying your devices, you need to use your own
key pair, with a private key that you must keep secret.

(If you're new to these ideas, check out the `Public-key
cryptography`_ and `Digital signature`_ pages on Wikipedia.)

.. _MCUboot: https://mcuboot.com

.. _Public-key cryptography:
   https://en.wikipedia.org/wiki/Public-key_cryptography

.. _Digital signature:
   https://en.wikipedia.org/wiki/Digital_signature
