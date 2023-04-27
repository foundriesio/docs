.. _ref-rm_board_imx8ulp-lddr4-evk:

i.MX 8 ULP Evaluation Kit
=========================

.. |board_name| replace:: i.MX 8 ULP EVK
.. |machine_name| replace:: imx8ulp-lpddr4-evk
.. |debug_port| replace:: **J17**
.. |download_port| replace:: **J15**
.. |power_jack| replace:: **SW10**
.. |power_switch| replace:: **SW10**
.. |boot_mode_switch| replace:: **SW5**
.. |boot_mode_sdp| replace:: X, X, X, X, X, X, ON, OFF
.. |boot_mode_emmc| replace:: OFF, OFF, X, X, OFF, OFF, OFF, ON
.. |boot_mode_bits| replace:: 1-8
.. |imx_usb_type| replace:: micro-C
.. |imx_n_consoles| replace:: Three
.. |imx_tty_device| replace:: ``ttyUSB2``
.. |imx_tty_port| replace:: ``if02``
.. |imx_usb_type_debug| replace:: micro-B
.. |imx_usb_type_sdp| replace:: USB-C
.. |imx_power_jack_type| replace:: USB-C

.. |imx_lsusb| prompt:: bash $, auto

           $ lsusb | grep NXP
           Bus 001 Device 023: ID 1fc9:012b NXP Semiconductors i.MX 8M Dual/8M QuadLite/8M Quad Serial Downloader

.. |image_board_top| image:: /_static/boards/imx8ulp-lpddr4-evk.png
     :width: 600
     :align: middle

.. |image_board_SW| image:: /_static/boards/imx8ulp-lpddr4-evk_SW.png
     :width: 600
     :align: middle

.. |imx_tty_list| prompt:: bash $, auto

        $ ls -l /dev/serial/by-id/
        total 0
        lrwxrwxrwx 1 root root 13 Feb 13 12:59 usb-0403_FT4232H_9266A2-if00-port0 -> ../../ttyUSB0
        lrwxrwxrwx 1 root root 13 Feb 13 12:59 usb-0403_FT4232H_9266A2-if02-port0 -> ../../ttyUSB2
        lrwxrwxrwx 1 root root 13 Feb 13 12:59 usb-0403_FT4232H_9266A2-if03-port0 -> ../../ttyUSB3

.. |usb_device_windows| image:: /_static/boards/windows_verify.png
          :width: 600
          :align: middle

.. |imx_file_list| prompt:: text

          ├── lmp-factory-image-imx8ulp-lpddr4-evk.wic
          ├── u-boot-imx8ulp-lpddr4-evk.itb
          ├── imx-boot-imx8ulp-lpddr4-evk
          └── mfgtool-files-imx8ulp-lpddr4-evk
               ├── bootloader.uuu
               ├── full_image.uuu
               ├── SPL-mfgtool
               ├── u-boot-mfgtool.itb
               ├── uuu
               └── uuu.exe

.. |secure_boot_preparation_note| replace:: The instructions in this section
     show the preparation before the flashing procedure.

.. |secure_boot_pre_flash_note| replace:: Follow the instructios below.

.. include:: imx-common-board.inc