.. _ref-rm_board_imx6ullevk:

i.MX 6ULL Evaluation Kit
========================

.. |board_name| replace:: imx6ullevk
.. |machine_name| replace:: imx6ullevk
.. |debug_port| replace:: **J1901**
.. |download_port| replace:: **USB OTG**
.. |power_jack| replace:: **J2001**
.. |power_switch| replace:: **SW2001**
.. |boot_mode_switch| replace:: **SW602**
.. |boot_mode_sdp| replace:: OFF, ON
.. |boot_mode_emmc| replace:: ON, OFF
.. |boot_mode_bits| replace:: 1-2
.. |imx_n_consoles| replace:: One
.. |imx_tty_device| replace:: ``ttyUSB2``
.. |imx_tty_port| replace:: ``if00``
.. |imx_usb_type_debug| replace:: micro-B
.. |imx_usb_type_sdp| replace:: micro-B
.. |imx_power_jack_type| replace:: 5V

.. |imx_lsusb| prompt:: bash $, auto

                $ lsusb | grep NXP
                  Bus 002 Device 052: ID 15a2:0080 Freescale Semiconductor, Inc.

.. |image_board_top| image:: /_static/boards/imx6ullevk.png
     :width: 600
     :align: middle

.. |image_board_SW| image:: /_static/boards/imx6ullevk_SW1.png
     :width: 600
     :align: middle

.. |imx_tty_list| prompt:: bash $, auto

        $ ls -l /dev/serial/by-id/
          total 0
          lrwxrwxrwx 1 root root 13 Dec  3 13:09 usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0 -> ../../ttyUSB2

.. |usb_device_windows| image:: /_static/boards/imx6_windows.png
          :width: 600
          :align: middle

.. |imx_file_list| prompt:: text

          ├── lmp-factory-image-imx6ullevk.wic.gz
          ├── u-boot-imx6ullevk.itb
          ├── sit-imx6ullevk.bin
          ├── SPL-imx6ullevk
          └── mfgtool-files-imx6ullevk
               ├── bootloader.uuu
               ├── full_image.uuu
               ├── SPL-mfgtool
               ├── u-boot-mfgtool.itb
               ├── uuu
               └── uuu.exe

.. |secure_boot_preparation_note| replace::
    The instructions in this section also applies to those boards with secure boot enabled.
    There are references on how to perform common instructions along with the flow.
    :ref:`ref-security`  details the required background for secure boot.

.. |secure_boot_pre_flash_note| replace:: For instructions on how to sign the
     required images before flashing them to the board with secure boot enabled,
     see :ref:`ref-secure-machines`.

Pre-Preparation
---------------

Before starting to work with |board_name|, 
switch **SW601** to device microSD by setting to OFF, OFF, ON, OFF (from 1–4 bit)

     .. figure:: /_static/boards/imx6_sw601.png
          :width: 300
          :align: center

          **SW601** settings

.. include:: imx-common-board.inc
