Preparation
-----------

|secure_boot_preparation_note|

.. important::
   Ensure you replace ``<factory>`` placeholder below with the name of your Factory.

#. Download the necessary files from ``https://app.foundries.io/factories/<factory>/targets``:

     a. Click the latest Target with the :guilabel:`platform` trigger.

     b. Expand the **run** in the :guilabel:`Runs` section which corresponds with the name of the board.
        **Download the Factory image for that machine.**
        For example::
        
             lmp-factory-image-<machine_name>.wic.gz
             u-boot-<machine_name>.itb
             imx-boot-<machine_name>

      .. note::
            The compressed image (``.wic.gz``) is used since LmP **v92**.
            Before, the scripts required a compressed file image (``.wic``).

#. Download and extract the file ``mfgtool-files-<machine_name>.tar.gz``:

     .. parsed-literal::

      tar -zxvf mfgtool-files-|machine_name|.tar.gz

#. Organize all the files, mirroring the tree below:

     |imx_file_list|

Hardware Preparation
--------------------

Set up the board for updating using the manufacturing tools:

|image_board_top|

Top view of |board_name|

#. **OPTIONAL**. Only required if you have problems or want to see the boot console output.

     Connect the |imx_usb_type_debug| end of the USB cable into debug port |debug_port|.
     Connect the other end of the cable to a PC acting as a host terminal.
     |imx_n_consoles| UART connections will appear on the PC. For example, on a Linux host:

     |imx_tty_list|

     Using a serial terminal program like `minicom <https://salsa.debian.org/minicom-team/minicom>`_,
     connect to the port with |imx_tty_port| in the name (in this example |imx_tty_device|).
     Apply the following configuration:

          - Baud rate: 115200
          - Data bits: 8
          - Stop bit: 1
          - Parity: None
          - Flow control: None

#. Ensure that the power is off (|power_switch|)

#. Put the |board_name| into programing mode:

     Switch |boot_mode_switch| to |boot_mode_sdp| (from |boot_mode_bits| bit) to Download Mode.

     |image_board_SW|

     Location of |boot_mode_switch| dip switch on |board_name|

#. Connect your computer to the |board_name| board via the |imx_usb_type_sdp| port 1 ``Download`` |download_port| jack.

#. Connect the |imx_power_jack_type| power plug to the port 2 ``Power`` |power_jack| jack.

#. Power on the |board_name| board by sliding power switch |power_switch| to ON.

Flashing
--------

Once in serial downloader mode and connected to your PC, the evaluation board should show up as an NXP® USB device.

|secure_boot_pre_flash_note|

.. tabs::

   .. group-tab:: Linux

      #. Verify target is present:

         |imx_lsusb|

         In this mode you will use the ``uuu`` tools to program the images to the eMMC. 
         The ``USB ID`` may differ if a different SoC is used.

      #. To program the LmP to the EMMC run

          .. parsed-literal::

           $ sudo mfgtool-files-|machine_name|/uuu mfgtool-files-|machine_name|/full_image.uuu
             uuu (Universal Update Utility) for nxp imx chips -- libuuu_1.4.243-0-ged48c51

             Success 1    Failure 0


             1:92     6/ 6 [Done                                  ] FB: done

      #. Turn off the power
      #. Put the board into run mode

   .. group-tab:: Windows

      #. Start the ``Device Manager``
      #. Select ``View``
      #. Select ``Devices by container``
      #. Verify a device like the following:  |usb_device_windows|
      #. Run the command below to program the LmP to the EMMC:

          .. parsed-literal::

           C:\\Users\\Someone> mfgtool-files-|machine_name|\\uuu.exe mfgtool-files-|machine_name|\\full_image.uuu
             uuu (Universal Update Utility) for nxp imx chips -- libuuu_1.4.243-0-ged48c51

             Success 1    Failure 0


             1:92     6/ 6 [Done                                  ] FB: done

      #. Turn off the power.
      #. Put the board into run mode

Put the |board_name| into run mode by switching |boot_mode_switch|
to |boot_mode_emmc| to set the board to boot from eMMC.

Power on the |board_name| board by sliding the power switch |power_switch| to ON.
