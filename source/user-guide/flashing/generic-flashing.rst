.. tabs::

   .. group-tab:: Linux

      1. Determine which disk to flash by finding the device with the ``SIZE`` that matches that of your flash drive.
         Ignore partitions (indicated by ``part`` under ``TYPE``).
         Note the ``NAME`` of the flash drive (e.g., ``/dev/mmcblk0``, ``/dev/sdb``), as it will be used for the disk path::

           lsblk -po +MODEL

         .. highlight:: none

         ::

           $ lsblk -po +MODEL
           NAME             MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT                 MODEL
           /dev/mmcblk0     179:0    0  29.8G  0 disk
           ├─/dev/mmcblk0p1 179:1    0  41.6M  0 part /mnt/boot
           └─/dev/mmcblk0p2 179:2    0  29.8G  0 part /mnt/otaroot
           /dev/zram0       254:0    0    26G  0 disk /out
           /dev/nvme0n1     259:0    0 953.9G  0 disk                            SSDPEKKF010T8 NVMe INTEL 1024GB

      2. Flash the disk.

         | Replace ``<system-image>`` with the path to your system image.
         | Replace ``/dev/mmcblk<X>`` with your chosen disk path.

       .. code-block:: shell

          gunzip -c <system-image> | sudo dd of=/dev/mmcblk<X> bs=4M iflag=fullblock oflag=direct status=progress

   .. group-tab:: macOS

      1. Determine which disk you want to flash by finding the device with the ``SIZE`` that matches that of your flash drive.
         Ignore partitions (lines without ``*`` in the ``SIZE``).
         Note the ``IDENTIFIER`` of the flash drive, (e.g., ``/dev/disk3``) as it will be used for the disk path::

           ``diskutil list``:

         .. highlight:: none

         ::

           $ diskutil list
           /dev/disk3 (internal, physical):
              #:                       TYPE NAME                    SIZE       IDENTIFIER
              0:     FDisk_partition_scheme                        *15.5 GB    disk3
              1:             Windows_FAT_32 boot                    45.7 MB    disk3s1
              2:                      Linux                         15.5 GB    disk3s2

      2. Flash the disk.

         | Replace ``<system-image>`` with the path to your system image.
         | Replace ``/dev/disk<X>`` with your chosen disk path.

        .. code-block:: shell

           gunzip -c <system-image> | sudo dd of=/dev/disk<X> bs=4M

   .. group-tab:: Windows

      Windows has no built in tools for flashing the image to disk.
      We recommend you download and use either **Win32 Disk Imager** or **Rufus**.

      .. note:: 

           Your system image is in a compressed ``wic.gz`` format.
           To follow these next steps, you must extract it using a tool like 7zip_ which will leave you with a ``.wic`` image file.

      **Using Rufus**:

      #. Download and run Rufus_.
      #. Select your disk.
      #. :guilabel:`SELECT` your ``<system-image>``.
      #. :guilabel:`START` the flash procedure.

      **Using Win32 Disk Imager**

      #. Download and run `Win32 Disk Imager`_ as **Administrator**. 
      #. Click the blue folder icon.
      #. Select your ``<system-image>``
      #. Select your disk via the :guilabel:`Device` dropdown.
      #. Click :guilabel:`Write`
      #. Wait for the image to finish writing.
         A **Write Successful** dialog will appear.

1. Remove the flash drive and connect it to the board.

2. Power on the board to boot the new image.


.. _Win32 Disk Imager: https://sourceforge.net/projects/win32diskimager/files/Archive/

.. _7zip: https://www.7-zip.org/download.html

.. _Rufus: https://rufus.ie
