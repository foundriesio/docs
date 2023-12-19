.. _ref-rm_board_imx8mqevk:

i.MX 8M Quad Evaluation Kit
===========================

.. |board_name| replace:: i.MX 8M Quad EVK
.. |machine_name| replace:: imx8mq-evk
.. |debug_port| replace:: **J1701**
.. |download_port| replace:: **J901**
.. |power_jack| replace:: **J902**
.. |power_switch| replace:: **SW701**
.. |boot_mode_switch| replace:: **SW802**
.. |boot_mode_sdp| replace:: OFF, ON
.. |boot_mode_emmc| replace:: ON, OFF
.. |boot_mode_bits| replace:: 1-2
.. |imx_n_consoles| replace:: Two
.. |imx_tty_device| replace:: ``ttyUSB0``
.. |imx_tty_port| replace:: ``if00``
.. |imx_usb_type_debug| replace:: micro-B
.. |imx_usb_type_sdp| replace:: USB-C
.. |imx_power_jack_type| replace:: 12V

.. |imx_lsusb| prompt:: bash $, auto

           $ lsusb | grep NXP
             Bus 001 Device 023: ID 1fc9:012b NXP Semiconductors i.MX 8M Dual/8M QuadLite/8M Quad Serial Downloader

.. |image_board_top| image:: /_static/boards/imx8mqevk.png
     :width: 600
     :align: middle

.. |image_board_SW| image:: /_static/boards/imx8mqevk_SW2.png
     :align: middle

.. |imx_tty_list| prompt:: bash $, auto

     $ ls -l /dev/serial/by-id/
     total 0
     lrwxrwxrwx 1 root root 13 Nov 16 23:45 usb-Silicon_Labs_CP2105_Dual_USB_to_UART_Bridge_Controller_007FC3F4-if00-port0 -> ../../ttyUSB0
     lrwxrwxrwx 1 root root 13 Nov 16 23:45 usb-Silicon_Labs_CP2105_Dual_USB_to_UART_Bridge_Controller_007FC3F4-if01-port0 -> ../../ttyUSB2

.. |usb_device_windows| image:: /_static/boards/windows_verify.png
          :width: 600
          :align: middle

.. |imx_file_list| prompt:: text

          ├── lmp-factory-image-imx8mq-evk.wic.gz
          ├── u-boot-imx8mq-evk.itb
          ├── sit-imx8mq-evk.bin
          ├── imx-boot-imx8mq-evk or imx-boot-imx8mq-evk-nohdmi
          └── mfgtool-files-imx8mq-evk
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
     see:ref:`ref-secure-machines`

.. include:: imx-common-board.inc
