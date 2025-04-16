.. _gs-emulation-with-qemu:

Emulation With QEMU
=========================

.. note::

  This tutorial is designed to assist you in getting started with using :term:`QEMU` to emulate devices on your desktop.
  Please note that we are selecting a specific machine to establish an environment for experimenting with the FoundriesFactory™ Platform.
  This approach will enable you to engage with subsequent tutorials and enhance your skills.

Prerequisites and Pre-Work
---------------------------

   - Ensure that you have installed `QEMU <https://www.qemu.org/download/>`_ 5.2 or later.
   - Create a :ref:`ref-factory` for the ``QEMU Arm 64 bit`` platform as described in the guide :ref:`gs-select-platform`:

.. figure:: /_static/getting-started/qemu/example_factory_arm64.png
   :width: 900
   :align: center
   :alt: QEMU Arm 64 bit example Factory

   QEMU ARM Example Factory

Emulating Device
----------------

1. Go to the `Targets` tab of your Factory and download ``lmp-base-console-image-qemuarm64-secureboot.wic.gz`` and ``flash.bin``:

.. figure:: /_static/getting-started/qemu/example_required_artefacts.png
   :width: 900
   :align: center
   :alt: Artifacts which are required to run the image with QEMU

   Required QEMU artifacts

2. Make a directory for the artifacts and cd into it:

.. code-block:: shell

    mkdir -p lmp-qemu/arm64
    cd lmp-qemu/arm64

3. Copy the Artifacts to the ``lmp-qemu/arm64`` directory :

.. code-block:: shell

    cp <path-where-dir>/lmp-base-console-image-qemuarm64-secureboot.wic.gz .
    cp <path-where-dir>/flash.bin .

4. Decompress the image:

.. code-block:: shell

    gunzip lmp-base-console-image-qemuarm64-secureboot.wic.gz

5. Convert the Disk to QCOW2 Format:

Use ``qemu-img`` to convert your raw disk image to the QCOW2 format.
This step can sometimes make the image more amenable to virtualization.

.. code-block:: shell

    qemu-img convert -f raw -O qcow2 lmp-base-console-image-qemuarm64-secureboot.wic lmp-base-console-image-qemuarm64-secureboot.qcow2

6. Resize the Image:

Resize the new QCOW2 image to a size that’s a multiple of the sector size.
Let us resize it to 4GB for simplicity.

.. code-block:: shell

    qemu-img resize lmp-base-console-image-qemuarm64-secureboot.qcow2 4G

7. Run QEMU with the New Image:

Once you’ve converted and resized the image, you can then use it with your QEMU command.

.. code-block:: shell

    qemu-system-aarch64 \
    -m 2048 \
    -cpu cortex-a57 \
    -smp 2 \
    -machine acpi=off \
    -bios flash.bin \
    -device virtio-net-device,netdev=net0,mac=52:54:00:12:35:02 \
    -device virtio-serial-device \
    -drive id=disk0,file=lmp-base-console-image-qemuarm64-secureboot.qcow2,if=none,format=qcow2 \
    -device virtio-blk-device,drive=disk0 \
    -netdev user,id=net0,hostfwd=tcp::2222-:22 \
    -object rng-random,filename=/dev/urandom,id=rng0 \
    -device virtio-rng-pci,rng=rng0 \
    -chardev null,id=virtcon \
    -machine virt,secure=on \
    -nographic

8. Log into the booted system:

   By default, the ``username`` and ``password`` to log in your device after boot are ``fio/fio``.
   We recommend changing them once you are in development.

   .. figure:: /_static/getting-started/qemu/example_login.png
      :width: 900
      :align: center
      :alt: Login

      QEMU device login

.. note::

   If you are not prompted for login, press ``Enter`` to check if it gets displayed.

.. note::

   If you encounter a QEMU terminal where common commands like ``ls`` are unresponsive, it may indicate an issue.
   A missing login prompt likely means that your image did not boot successfully.

   For this specific platform, we use the ``-bios=flash.bin`` flag to boot the system.
   However, the flags and configurations may vary based on the selected platform.

.. note::

   To emulate multiple devices, ensure that you convert to the QCOW2 format.
   Each image converted and subsequently run with QEMU will be recognized as a distinct device.

Next Step
--------------------------

At this point, you have successfully set up the device.
You are now able to :ref:`gs-register` and proceed with the following tutorials.
