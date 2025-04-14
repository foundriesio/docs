Building
--------

When building the Cortex R5 U-Boot, all variants are built:

* ``hs-fs`` (High Security/Field Securable), also known as `SK-AM64B`_: This is a SoC/board state before a customer has blown the keys in the device,
  i.e., the state at which the HS device leaves TI factory.
  The device protects the ROM code, TI keys and certain security peripherals.
  In this state, devices do not force authentication for booting, however DMSC is locked.

* ``hs`` (High Security/Security Enforced), also known as `SK-AM64B`_: This is a SoC/board state after successfully blowning the keys and set “customer keys enable”.
  In HS-SE device all security features are enabled.
  All secrets within the device are fully protected and all of the security goals are fully enforced.
  The device also enforces secure booting.

* ``gp`` (General Purpose), also known as SK-AM64: This is a SoC/board state with no device protection and authentication is not enabled for booting the device.

The default variant is  ``hs-fs``.
To boot an image on other variants without pre-flash files manipulations on the target file-system, we need to change the ``SYSFW_SUFFIX`` variable.
The following changes the default to ``gp``, so that the image produced boots that variant:

.. code-block:: shell

   echo 'SYSFW_SUFFIX:am64xx-evm-k3r5 = "gp"' >> meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc

.. include:: generic-prepare.rst

#. Extract the file::

      gunzip lmp-factory-image-am64xx-evm.wic.gz

.. _SK-AM64B:
   https://www.ti.com/tool/SK-AM64B

