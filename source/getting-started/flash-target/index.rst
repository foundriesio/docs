Flash your Device |:cloud_lightning:|
=====================================

.. note::
   To follow this section, you will need:
    - A Raspberry Pi 3 of any variant, or a Raspberry Pi 4.
    - A `suitable Micro SD Card <https://elinux.org/RPi_SD_cards>`_ to flash
      your LmP target build to.
    - Wired or WiFi network with internet access.

      - Ethernet cable (if choosing Wired)

Download LmP system image
-------------------------

When you trigger a build, it produces build artifacts as an output which can be
downloaded from the **Targets** tab of your factory, as shown in
:ref:`ref-watch-build`.

1. Navigate to the **Targets** section
   
2. Find your initial LmP platform build, denoted by the trigger name
   ``platform-<tag>``

.. figure:: /_static/flash-target/artifacts.png
   :width: 769
   :align: center

Flash LmP system image
----------------------




     sudo dd if=<lmp-factory-image.wic.gz> of=/dev/mmcblkX bs=4M iflag=fullblock oflag=direct status=progress

.. tabs::

   .. group-tab:: Linux

      1. | Determine the disk you want to flash. E.G ``/dev/sda``
         | ``lsblk -po +MODEL``

         **Example Output**::

          matthew@thinkpad ~ $ lsblk -po +MODEL
          NAME                          MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINT MODEL
          /dev/sda                        8:0    0 465.8G  0 disk             HGST_HTS725050A7E630
          └─/dev/sda1                     8:1    0 465.8G  0 part  /mnt/hdd   
          /dev/sdb                        8:16   0 232.9G  0 disk             Samsung_SSD_860_EVO_mSATA_250GB
       
      2. Flash the disk with your factory image, replacing ``<factory-image>``
         with the path to your downloaded LmP wig.gz image and ``/dev/sdX`` with your chosen
         disk path.
 
       .. code-block:: shell

          sudo dd if=<lmp-factory-image.wic.gz> of=/dev/mmcblkX bs=4M iflag=fullblock oflag=direct status=progress

   .. group-tab:: macOS

      1. | Determine the disk you want to flash by its path. E.G ``/dev/disk3``
         | ``diskutil list``

         **Example Output**::

          /dev/disk3 (internal, physical):
             #:                       TYPE NAME                    SIZE       IDENTIFIER
             0:     FDisk_partition_scheme                        *15.5 GB    disk3
             1:             Windows_FAT_32 boot                    45.7 MB    disk3s1
             2:                      Linux                         15.5 GB    disk3s2

       2. Flash the disk with your factory image, replacing ``<factory-image>``
          with the path to your downloaded LmP wic.gz image and ``diskX`` with your
          chosen disk path.

        .. code-block:: shell
 
           sudo dd if=<lmp-factory-image.wic.gz> of=/dev/diskX bs=4M

   .. group-tab:: Windows

      Windows has no ``dd`` like tool built into the operating system to flash
      your image to disk. In this case, we recommend you download and use
      Etcher_.
      
      1. Download Etcher_

         An example path string if installing to a folder on the desktop would
         look like this.

         ``C:\Users\Stetson\Desktop\fio\bin``

      You should now be able to open ``cmd.exe`` or ``powershell.exe`` and type
      ``fioctl``.
      
.. _Etcher: https://www.balena.io/etcher/


Register your device
--------------------

``lmp-device-register``
