How to plan the porting
-----------------------

So according to the boot flow described on :numref:`ref-pg-boot-flow-diagram`, some packages needed are clear, for example U-Boot, OP-TEE, TF-A and Linux
Kernel. The recommendation is to start with the porting of these packages just
after creating a machine configuration file.

Once the basic integration is complete, make sure to enable additional
features, including the firmware not critical for the boot (such as
Bluetooth or Wi-Fi firmware), porting the applications, and then
continuing development as needed.

In short, the recommended order is:

1. Machine configuration file
2. SPL and U-Boot proper
3. OP-TEE and TF-A
4. Linux Kernel

.. note::

   It is recommended to use ``DISTRO=lmp-base`` during the porting task.

In the next sections each of the steps listed are detailed, focusing on
the recommendations to work with each package. It is important to note
that there are use cases when a board has peculiarities which may not be
listed here, but it is important to understand and cover them during the
port.