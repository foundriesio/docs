.. highlight:: sh

FOTA Demonstration System
=========================

Overview
--------

From here, you can follow instructions to set up and use an end-to-end
firmware over the air (FOTA) update system.

Using this system, you can upload a cryptographically signed firmware
image to a server. You can then use its web interface to push that new
firmware image to an IoT device. The device will then install and run
the new image after verifying the signature is valid.

In the demonstration system you will set up:

- the IoT Device is a `96Boards Nitrogen
  <https://www.seeedstudio.com/BLE-Nitrogen-p-2711.html>`_,
- the IoT Gateway is a `96Boards HiKey
  <http://www.96boards.org/product/hikey/>`_, and
- the Device Management Backend is a Docker container running hawkBit
  on a developer workstation.

A rough block diagram of the demonstration system is:

.. image:: /_static/fota-demo/block-diagram.png
   :align: center

Support for additional system components is in development. See the
:ref:`fota-demo` for additional information.

System Setup
------------

To create this system, follow these sub-guides in order:

1. Set up your :ref:`device-mgmt-hawkbit` for local development
#. Set up your :ref:`iot-device-96b_nitrogen`
#. Set up your :ref:`iot-gateway-96b_hikey`

System Usage
------------

Now that your system is fully set up, you should see the 96Boards
device show up in the "Targets" view of the hawkBit administrator
UI. It will look something like this, though the exact string may
change on your system:

.. image:: /_static/fota-demo/96b-target.png
   :align: center

To finish using the system, build a Zephyr image which contains a
simple shell application and upload it to the hawkBit server. You'll
then send it to the connected IoT Device using the hawkBit UI.::

    # Build Zephyr shell app
    $ cd <zephyr>
    $ make BOARD=96b_nitrogen -C samples/shell/

The resulting binary is stored in
``<zephyr>/samples/shell/outdir/96b_nitrogen/zephyr.bin``.

Next, upload this to the hawkBit server. An upload script,
:download:`test_hawkbit.sh </_static/fota-demo/test_hawkbit.sh>`, is
available; it will work unmodified if you used the default passwords,
but if you chose your own, you may need to modify it using the
information in the :ref:`hawkBit <device-mgmt-hawkbit-developers>`
page.

Upload the binary to your hawkBit server from the zephyr directory (10
is an arbitrary version number)::

    $ test_hawkbit.sh samples/shell/outdir/96b_nitrogen/zepyr.bin 10
    Created DS 1, SM 1 and uploaded artifact zephyr/samples/shell/outdir/96b_nitrogen/zephyr.bin

You will see updates in the hawkBit UI when the image is uploaded:

.. image:: /_static/fota-demo/distribution.png
   :align: center

Before updating the IoT Device, connect to its serial console via USB
at 115200 baud (which should be at ``/dev/ttyACM0`` or so on Linux
systems).

Now, click on the "Zephyr RPB" distribution, and drag it over the line
in "Targets" which represents your IoT Device. The next time the
Nitrogen board polls your hawkBit server for an update, you will see
it download this image, verify it, and reboot into the shell
application.

A video showing this in operation is available at `End to end Demo
video
<https://collaborate.linaro.org/download/attachments/74187413/Demo-1.mp4>`_.

**TODO sample console output when this is all working**

.. _fota-demo:

FOTA Demonstration System Index
-------------------------------

This section links to additional information about development not
covered by the instructions above.

.. toctree::
   :maxdepth: 2

   device-mgmt/index
   iot-device/index
   iot-gateway/index
