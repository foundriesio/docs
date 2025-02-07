Building
--------

When building the Cortex R5 U-Boot, all variants are built:

* ``hs-fs`` (High Security/Field Securable), also known as `SK-AM62B`_: The SoC/board state before blowing the keys on the device,
  i.e., the state at which the HS device leaves the TI factory.
  The device protects the ROM code, TI keys, and certain security peripherals.
  In this state, devices do not force authentication for booting, however DMSC is locked.

* ``hs`` (High Security/Security Enforced), also known as `SK-AM62B`_: This is the SoC/board state after successfully blowing the keys and setting “customer keys enable”.
  In HS-SE, all security features are enabled.
  Secrets within the device are fully protected and all security goals are enforced.
  The device enforces secure booting.

* ``gp`` (General Purpose), also known as `SK-AM62`_: This is a SoC/board state with no device protection and authentication is not enabled for booting the device.

The default variant is  ``hs-fs``.
To boot an image on other variants without pre-flash files manipulations on the target file-system, we need to change the ``SYSFW_SUFFIX`` variable.
The following changes the default to ``gp``, so that the image produced boots that variant:

.. code-block:: shell

   echo 'SYSFW_SUFFIX:am62xx-evm-k3r5 = "gp"' >> meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc

.. include:: generic-prepare.rst

#. Extract the file::

      gunzip lmp-factory-image-am62xx-evm.rootfs.wic.gz

#. Expand the **run** in the :guilabel:`Runs` section corresponding with the name of the board.
   Download ``ti-mfgtool-files-am62xx-evm.tar.gz``.

#. Extract the file::

      tar -zxvf ti-mfgtool-files-am62xx-evm.tar.gz

#. Organize the files as in the tree below::

      ├── lmp-factory-image-am62xx-evm.wic
      └── ti-mfgtool-files-am62xx-evm
          ├── flash.sh
          ├── tiboot3.bin
          ├── tispl.bin
          └── uboot.img

.. _SK-AM62B:
   https://www.ti.com/tool/SK-AM62B

.. _SK-AM62:
   https://www.ti.com/tool/SK-AM62
