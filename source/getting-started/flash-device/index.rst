Flash your Device |:cloud_lightning:|
=====================================

.. note::
   To follow this section, you will need:
    - A supported board that can boot from an SD Card.
     
      **(Raspberry Pi 3 of any variant, or a Raspberry Pi 4 recommended)**

    - A `suitable Micro SD Card <https://elinux.org/RPi_SD_cards>`_ to flash
      your LmP target build to.
    - Wired or WiFi network with internet access.

      - Ethernet cable (if choosing Wired)
      - 3.3 volt USB to TTL Serial Cable (if choosing WiFi)

Download LmP system image
-------------------------

When you trigger a build, it produces build artifacts as an output which can be
downloaded from the **Targets** tab of your factory, as described in
:ref:`ref-watch-build`.

1. Navigate to the **Targets** section of your Factory.
   
2. Find your LmP platform build, denoted by the **trigger name**:
   ``platform-<tag>``. 

   E.G: ``lmp-factory-image-raspberrypi3-64.wic.gz``

3. Download it by clicking on its name in the list of artifacts

.. figure:: /_static/flash-device/artifacts.png
   :width: 769
   :align: center

Flash LmP system image
----------------------

Once you have downloaded your LmP system image, it can be written to an SD Card
and booted.

.. note:: 
   If you are developing on a platform that has EMMC available such as the NXP
   iMX8MM-EVK, it is recommended that you boot from EMMC rather than SD. Read the
   <placeholder> section for details on flashing your system-image using the vendor
   provided tools.

.. tabs::

   .. group-tab:: Linux

      1. Determine the disk you want to flash by its path. E.G: ``/dev/sda``::

           lsblk -po +MODEL

         **Example Output**::

           NAME                          MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINT MODEL
           /dev/sda                        8:0    0 465.8G  0 disk             HGST_HTS725050A7E630
           └─/dev/sda1                     8:1    0 465.8G  0 part  /mnt/hdd   
           /dev/sdb                        8:16   0 232.9G  0 disk             Samsung_SSD_860_EVO_mSATA_250GB
       
      2. Flash the disk.  
 
         | Replace ``<system-image>``
         | Replace ``/dev/sdX`` with your chosen disk path.
 
       .. code-block:: shell

          gunzip -c <system-image> | sudo dd of=/dev/sdX bs=4M iflag=fullblock oflag=direct status=progress

   .. group-tab:: macOS

      1. Determine the disk you want to flash by its path. E.G: ``/dev/disk3``::

           diskutil list
        
         .. highlight:: none

         **Example Output**::

           /dev/disk3 (internal, physical):
              #:                       TYPE NAME                    SIZE       IDENTIFIER
              0:     FDisk_partition_scheme                        *15.5 GB    disk3
              1:             Windows_FAT_32 boot                    45.7 MB    disk3s1
              2:                      Linux                         15.5 GB    disk3s2

      2. Flash the disk.  
 
         | Replace ``<system-image>``
         | Replace ``/dev/diskX`` with your chosen disk path.

        .. code-block:: shell
 
           gunzip -c <system-image> | sudo dd of=/dev/diskX bs=4M

   .. group-tab:: Windows

      Windows has no ``dd`` like tool built into the operating system to flash
      your image to disk. In this case, we recommend you download and use
      Etcher_.
     
      1. Download and run Etcher_.
      2. Select your ``<system-image>``.
      3. Select your disk.
      4. Flash it.

.. glossary::
  
  <system-image>
     Path to your LmP System image in ``wic.gz`` format.
    
