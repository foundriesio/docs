.. _ref-rm_board_stm32mp15-eval:

STM32MP15 EV1 Evaluation Board
==============================

This page covers flashing an STM32MP15 EV1 board with LmP artifacts.

Getting the Required Software
-----------------------------

**STM32CubeProgrammer** is used to flash the STM32MP15 EV1 board.
This section shows how to download and set it up.
Skip to the next section if you already have **STM32CubeProgrammer** installed.


.. tabs::

    .. group-tab:: Linux

			1. Download the `STM32CubeProgrammer`_ software for Linux®.

			2. Unzip it to a known location:

				.. prompt:: bash host:~$, auto
						
						host:~$ mkdir <STM32CubeProgrammer_path>
						host:~$ unzip en.stm32cubeprg-lin_v*.zip -d <STM32CubeProgrammer_path>

			3. Run the installer and follow the instructions on screen:

				.. prompt:: bash host:~$, auto

						host:~$ ./SetupSTM32CubeProgrammer*.linux

			4. Export the ``STM32CubeProgrammer_path`` to the system path:

				.. prompt:: bash host:~$, auto

						host:~$ export PATH=<STM32CubeProgrammer_path>/bin:$PATH

			5. To allow **STM32CubeProgrammer** to access the USB port through low-level commands, proceed as follows:

				.. prompt:: bash host:~$, auto

						host:~$ cd <STM32CubeProgrammer_path>/Drivers/rules
						host:~$ sudo cp *.* /etc/udev/rules.d/

    .. group-tab:: Windows

			1. Download the `STM32CubeProgrammer`_ software for Windows.

			2. Unzip it to a known location.

			3. Execute the Windows installer and follow the instructions on screen.

			4. Run ``STM32 Bootloader.bat`` to install the required DFU drivers and	activate the STM32 device in USB DFU mode.

For more information, check the `STM32CubeProgrammer Installation page`_.

Preparation
-----------

1. In your Factory, click on the latest ``platform`` build.

2. Expand the run for ``stm32mp15-eval``, and under the ``other`` folder, find and download ``flashlayouts-stm32mp15-eval.tar.gz``.

3. Unzip the file: ::

	   tar -xvf flashlayouts-stm32mp15-eval.tar.gz

The file used for flashing is ``FlashLayout_stm32mp1-optee.tsv``

Hardware Preparation
--------------------

1. Connect the USB OTG cable in the base board to the host machine.

2. Set the boot switches in the CPU board to Serial Download Mode, **0000**:

	 .. figure:: /_static/boards/stm32-ev1_sdp.jpg
	    :width: 350
	    :align: center

	    stm32mp15-ev1 SDP mode

3. **OPTIONAL**: For UART output in the USB connector on the CPU board, remove **JP1** jumper and move **JP4** and **JP5** to the 2–3 position:

	.. figure:: /_static/boards/stm32-ev1_jp1.jpg
	   :width: 50%
	   :align: center

	   stm32mp15-ev1 JP1

	.. figure:: /_static/boards/stm32-ev1_jp4-jp5.jpg
	   :width: 350
	   :align: center

	   stm32mp15-ev1 JP4 and JP5

Flashing
--------

1. Turn on the board and verify that it is set for serial download mode:

.. prompt:: bash host:~$, auto

	host:~$ STM32_Programmer_CLI -l usb
	      -------------------------------------------------------------------
		                STM32CubeProgrammer v2.11.0
	      -------------------------------------------------------------------

	 =====  DFU Interface   =====

	 Total number of available STM32 device in DFU mode: 1

	  Device Index           : USB1
	  USB Bus Number         : 001
	  USB Address Number     : 001
	  Product ID             : DFU in HS Mode @Device ID /0x500, @Revision ID /0x0000
	  Serial number          : 002B00323438511836383238
	  Firmware version       : 0x0110

2. Flash the board. Make sure to replace the command below with the USB ``Device
Index`` from the previous step if needed:

.. prompt:: bash host:~$, auto

	host:~$ STM32_Programmer_CLI -c port=usb1 -w FlashLayout_stm32mp1-optee.tsv

This can take a few minutes to complete. The process can be watched from the
host console, UART output, or board display.

3. Once the flashing procedure finishes, change the boot switches to eMMC boot, **0100**:

	.. figure:: /_static/boards/stm32-ev1_boot.jpg
	  :width: 350
	  :align: center

	  stm32mp15-ev1 eMMC boot

4. Reset the board to boot the installed LmP image.

.. _STM32CubeProgrammer: https://www.st.com/en/development-tools/stm32cubeprog.html
.. _STM32CubeProgrammer Installation page: https://wiki.st.com/stm32mpu/wiki/STM32CubeProgrammer#STM32CubeProgrammer_installation
