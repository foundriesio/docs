.. _ref-rm_board_imx8mp-lpddr4-evk:

i.MX 8M Plus Evaluation Kit
===========================

.. |board_name| replace:: i.MX 8M Plus EVK
.. |machine_name| replace:: imx8mp-lpddr4-evk
.. |debug_port| replace:: **J23**
.. |download_port| replace:: **J6**
.. |power_jack| replace:: **J5**
.. |power_switch| replace:: **SW3**
.. |boot_mode_switch| replace:: **SW4**
.. |boot_mode_sdp| replace:: OFF, OFF, OFF, ON
.. |boot_mode_emmc| replace:: OFF, ON, OFF, OFF
.. |boot_mode_bits| replace:: **1-4**
.. |imx_n_consoles| replace:: Four
.. |imx_tty_device| replace:: ``ttyUSB2``
.. |imx_tty_port| replace:: ``if02``
.. |imx_usb_type_debug| replace:: micro-B
.. |imx_usb_type_sdp| replace:: USB-C
.. |imx_power_jack_type| replace:: USB-C

.. |imx_lsusb| prompt:: bash $, auto

     $ lsusb | grep NXP
       Bus 001 Device 023: ID 1fc9:012b NXP Semiconductors i.MX 8M Dual/8M QuadLite/8M Quad Serial Downloader

.. |image_board_top| image:: /_static/boards/imx8mp-lpddr4-evk.png
     :width: 600
     :align: middle

.. |image_board_SW| image:: /_static/boards/imx8mp-lpddr4-evk_SW.png
     :width: 600
     :align: middle

.. |imx_tty_list| prompt:: bash $, auto

          $ ls -l /dev/serial/by-id/
          total 0
          lrwxrwxrwx 1 root root 13 jan 24 10:24 usb-FTDI_Quad_RS232-HS-if00-port0 -> ../../ttyUSB0
          lrwxrwxrwx 1 root root 13 jan 24 10:24 usb-FTDI_Quad_RS232-HS-if01-port0 -> ../../ttyUSB1
          lrwxrwxrwx 1 root root 13 jan 24 10:24 usb-FTDI_Quad_RS232-HS-if02-port0 -> ../../ttyUSB2
          lrwxrwxrwx 1 root root 13 jan 24 10:24 usb-FTDI_Quad_RS232-HS-if03-port0 -> ../../ttyUSB3

.. |usb_device_windows| image:: /_static/boards/windows_verify.png
          :width: 600
          :align: middle

.. |imx_file_list| prompt:: text

          ├── lmp-factory-image-imx8mp-lpddr4-evk.wic.gz
          ├── u-boot-imx8mp-lpddr4-evk.itb
          ├── sit-imx8mp-lpddr4-evk.bin
          ├── imx-boot-imx8mp-lpddr4-evk
          └── mfgtool-files-imx8mp-lpddr4-evk
               ├── bootloader.uuu
               ├── full_image.uuu
               ├── imx-boot-mfgtool
               ├── uuu
               └── uuu.exe

.. |secure_boot_preparation_note| replace::
    The instructions in this section also applies to those boards with secure boot enabled.
    There are references on how to perform common instructions along with the flow.
    :ref:`ref-security`  details the required background for secure boot.

.. |secure_boot_pre_flash_note| replace:: For instructions on how to sign the
    required images before flashing them to the board with secure boot enabled,
    see :ref:`ref-secure-machines`

.. include:: imx-common-board.inc
