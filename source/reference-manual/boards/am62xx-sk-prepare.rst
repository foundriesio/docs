Building
--------

When building the Cortex R5 u-boot, it builds for all different variants:

* ``hs-fs`` (High Security/Field Securable) also known as `SK-AM62B`_: This is a SoC/board state before a customer has blown the keys in the device. i.e. the state at which HS device leaves TI factory. In this state, the device protects the ROM code, TI keys and certain security peripherals. In this state, device do not force authentication for booting, however DMSC is locked.

* ``hs`` (High Security/Security Enforced) also known as `SK-AM62B`_: This is a SoC/board state after a customer has successfully blown the keys and set “customer keys enable”. In HS-SE device all security features are enabled. All secrets within the device are fully protected and all of the security goals are fully enforced. The device also enforces secure booting.

* ``gp`` (General Purpose) variant also known as `SK-AM62`_: This is a SoC/board state where there is no device protection and authentication is not enabled for booting the device.

The default variant is the ``hs-fs``. To boot an image on the others variants without pre-flash files manipulations
on the target file-system we need to change the ``SYSFW_SUFFIX`` variable.
The following changes the default to ``gp`` so the image produced boots on that variant:

.. code-block:: shell

   echo 'SYSFW_SUFFIX:am62xx-evm-k3r5 = "gp"' >> meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc

Preparation
-----------

Ensure you replace the ``<factory>`` placeholder below with the name of your
Factory.

Download necessary files from ``https://app.foundries.io/factories/<factory>/targets``

#. Click the latest Target with the :guilabel:`platform-devel` trigger.

   .. figure:: /_static/boards/generic-steps-1.png
      :align: center
      :width: 300

#. Expand the **run** in the :guilabel:`Runs` section (by clicking on the ``+`` sign) which corresponds
   with the name of the board and **download the Factory image for that
   machine.**

   | E.g: ``lmp-factory-image-am62xx-evm.wic.gz``

   .. figure:: /_static/boards/am62xx-sk-steps-2.png
      :align: center
      :width: 600
#. Extract the file ``lmp-factory-image-am62xx-evm.wic.gz``::

      gunzip lmp-factory-image-am62xx-evm.wic.gz

#. Expand the **run** in the :guilabel:`Runs` section which corresponds
   with the name of the board ti-mfgtool-files and **download the tools for that
   machine.**

   E.g: ``ti-mfgtool-files-am62xx-evm.tar.gz``

#. Download and extract the file ``ti-mfgtool-files-am62xx-evm.tar.gz``::

      tar -zxvf ti-mfgtool-files-am62xx-evm.tar.gz

#. Organize all the files like the tree below::

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
