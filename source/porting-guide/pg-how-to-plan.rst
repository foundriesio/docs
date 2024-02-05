How to Plan the Porting
-----------------------

According to the boot flow described in :numref:`ref-pg-boot-flow-diagram`, some required packages are clear:
U-Boot, OP-TEE, TF-A, and the Linux® Kernel.
The recommendation is to start with the porting of these packages directly after creating a machine configuration file.

Once the basic integration is complete, you will want to enable additional features.
This includes firmware not critical for boot, such as Bluetooth or Wi-Fi firmware.
Next, port any applications, and continue development as needed.

In short, the recommended order is:

1. Machine configuration file
2. SPL and U-Boot proper
3. OP-TEE and TF-A
4. Linux Kernel

.. note::

   Remember, it is recommended to use ``DISTRO=lmp-base`` during the porting task.

Next in this guide, each of the steps listed are detailed, focusing on the recommendations to work with each package.
It is important to note that there are use cases when a board has peculiarities which may not be listed here.
You will need to understand and cover them during the port.
