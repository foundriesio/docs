.. _ref-rm_board_imx93evk:

i.MX 93 Evaluation Kit
======================

.. |board_name| replace:: i.MX 93 EVK
.. |machine_name| replace:: imx93-11x11-lpddr4x-evk
.. |debug_port| replace:: **J1401**
.. |download_port| replace:: **J401**
.. |power_jack| replace:: **J301**
.. |power_switch| replace:: **SW301**
.. |boot_mode_switch| replace:: **SW1301**
.. |boot_mode_sdp| replace:: OFF, OFF, ON, ON
.. |boot_mode_emmc| replace:: ON, ON, ON, ON
.. |boot_mode_bits| replace:: 1-4
.. |imx_n_consoles| replace:: Four
.. |imx_tty_device| replace:: ``ttyUSB2``
.. |imx_tty_port| replace:: ``if02``
.. |imx_usb_type_debug| replace:: USB-C
.. |imx_usb_type_sdp| replace:: USB-C
.. |imx_power_jack_type| replace:: USB-C

.. |imx_lsusb| prompt:: bash $, auto

                $ lsusb | grep NXP
                  Bus 001 Device 018: ID 1fc9:014e NXP Semiconductors OO Blank 93

.. |image_board_top| image:: /_static/boards/imx93evk.png
     :width: 600
     :align: middle

.. |image_board_SW| image:: /_static/boards/imx93evk_SW.png
     :width: 600
     :align: middle

.. |imx_tty_list| prompt:: bash $, auto

          ls -l /dev/serial/by-id/
           total 0
           lrwxrwxrwx 1 root root 13 abr 20 16:20 usb-FTDI_Quad_RS232-HS-if00-port0 -> ../../ttyUSB0
           lrwxrwxrwx 1 root root 13 abr 20 16:20 usb-FTDI_Quad_RS232-HS-if01-port0 -> ../../ttyUSB1
           lrwxrwxrwx 1 root root 13 abr 20 16:20 usb-FTDI_Quad_RS232-HS-if02-port0 -> ../../ttyUSB2
           lrwxrwxrwx 1 root root 13 abr 20 16:20 usb-FTDI_Quad_RS232-HS-if03-port0 -> ../../ttyUSB3

.. |usb_device_windows| image:: /_static/boards/windows_verify.png
          :width: 600
          :align: middle

.. |imx_file_list| prompt:: text

          ├── lmp-factory-image-imx93-11x11-lpddr4x-evk.rootfs.wic.gz
          ├── u-boot-imx93-11x11-lpddr4x-evk.itb
          ├── imx-boot-imx93-11x11-lpddr4x-evk
          └── mfgtool-files-imx93-11x11-lpddr4x-evk
               ├── bootloader.uuu
               ├── full_image.uuu
               ├── SPL-mfgtool
               ├── u-boot-mfgtool.itb
               ├── uuu
               └── uuu.exe

.. |secure_boot_preparation_note| replace:: The instructions in this section
     show the preparation before the flashing procedure.

.. |secure_boot_pre_flash_note| replace:: Follow the instructions below.

.. include:: imx-common-board.inc
