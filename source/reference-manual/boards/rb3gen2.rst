Preparation
-----------

#. Download and extract the necessary files from ``https://app.foundries.io/factories/<factory>/targets``:

     a. Click the latest Target with the :guilabel:`platform` trigger.

     b. Expand the **run** in the :guilabel:`Runs` section which corresponds with the name of the board.
        **Download the Factory image for that machine.**
        For example::

             lmp-factory-image-qcm6490.qcomflash.tar.gz

        .. note::
              The compressed archive contains the flashing tool ``qdl``.
              The tool from the build has the interpretter set incorrectly.

     c. Download and compile qdl tool for your platorm
        The ``qdl`` tool from the buils is compiled for x86_64 architecture.
        When trying to flash from the host running ARM64 it is necessary to compile the tool from sources

        .. parsed-literal::

         git clone https://github.com/linux-msm/qdl
         cd qdl
         make

      d. On some host systems it might be necessary to disable ModemManager

Hardware Preparation
--------------------

#. Set up DIP_SW_0 positions 1 and 2 to ON. This enables serial output to the debug port.

#. Connect the USB debug cable to the host

#. Serial connection is based on FTDI chip. The device should appear as:

   /dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_<serial ID>-if00-port0

#. Connect the power cable

#. Press and hold F_DL button

#. When holding F_DL button, plug in USB-C cable from the host

Flashing
--------

Once EDL mode device is detected on the host system, flash the board using ``qdl`` tool

./qdl prog_firehose_ddr.elf rawprogram*.xml patch*.xml
