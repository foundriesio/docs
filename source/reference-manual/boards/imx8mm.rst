.. _ref-rm_board_imx8mmevk:

i.MX 8M Mini Evaluation Kit
===========================

.. |board_name| replace:: i.MX 8 M Mini EVK
.. |machine_name| replace:: imx8mm-lpddr4-evk
.. |debug_port| replace:: **J901**
.. |download_port| replace:: **J301**
.. |power_jack| replace:: **J302**
.. |power_switch| replace:: **SW101**
.. |boot_mode_switch| replace:: **SW1101**
.. |boot_mode_sdp| replace:: ON, OFF, ON, OFF
.. |boot_mode_emmc| replace:: OFF, ON, ON, OFF
.. |boot_mode_bits| replace:: **1-4**
.. |imx_n_consoles| replace:: Two
.. |imx_tty_device| replace:: ``ttyUSB1``
.. |imx_tty_port| replace:: ``if01``
.. |imx_usb_type_debug| replace:: micro-B
.. |imx_usb_type_sdp| replace:: USB-C
.. |imx_power_jack_type| replace:: USB-C

.. |imx_lsusb| prompt:: bash $, auto

     lsusb | grep NXP
     Bus 001 Device 023: ID 1fc9:012b NXP Semiconductors i.MX 8M Dual/8M QuadLite/8M Quad Serial Downloader

.. |image_board_top| image:: /_static/boards/imx8mmevk.png
     :width: 600
     :align: middle

.. |image_board_SW| image:: /_static/boards/imx8mmevk_SW.png
     :width: 600
     :align: middle

.. |imx_tty_list| prompt:: bash $, auto

          $ ls -l /dev/serial/by-id/
            total 0
            lrwxrwxrwx 1 root root 13 Dec 18 11:09 usb-FTDI_Dual_RS232-if00-port0 -> ../../ttyUSB0
            lrwxrwxrwx 1 root root 13 Dec 18 11:09 usb-FTDI_Dual_RS232-if01-port0 -> ../../ttyUSB1


.. |usb_device_windows| image:: /_static/boards/windows_verify.png
          :width: 600
          :align: middle

.. |imx_file_list| prompt:: text

          ├── lmp-factory-image-imx8mm-lpddr4-evk.wic
          ├── u-boot-imx8mm-lpddr4-evk.itb
          ├── sit-imx8mm-lpddr4-evk.bin
          ├── imx-boot-imx8mm-lpddr4-evk
          └── mfgtool-files-imx8mm-lpddr4-evk
               ├── bootloader.uuu
               ├── full_image.uuu
               ├── imx-boot-mfgtool
               ├── uuu
               └── uuu.exe

.. |secure_boot_preparation_note| replace::
    The instructions in this section also apply to those boards with secure
    boot enabled. There are references on how to perform common instructions
    along with the flow. The :ref:`ref-security` Reference Manual details the
    required background for secure boot.

.. |secure_boot_pre_flash_note| replace:: For instructions on how to sign the
     required images before flashing them to the board with secure boot enabled,
     follow the instructions from :ref:`ref-secure-machines`.

.. include:: imx-common-board.inc
