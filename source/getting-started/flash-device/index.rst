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
    
Boot Device and Connect to the Network
--------------------------------------

.. content-tabs::

   .. tab-container:: ethernet
      :title: Ethernet (Recommended)

      Ethernet works out of the box if a DHCP server is available on the
      local network.

      #. Connect an Ethernet cable to the board.
      #. Remove the SD card from your computer, and insert it into
         the board.
      #. Apply power to the board.

      Your board will connect to the network via Ethernet and will
      be ready to connect within a minute or two of booting.

   .. tab-container:: wifi
      :title: WiFi

      .. tabs::

          .. tab:: Raspberry Pi 3/4

              If you don't have Ethernet connectivity, you can connect to a
              WiFi network by temporarily enabling the UART console on your
              Raspberry Pi and running a command to connect to your WiFi
              network.
        
              .. note::
        
                 While a hardware serial port is available, enabling it
                 unfortunately requires this device to run at significantly
                 reduced speeds, and causes serious Bluetooth instability.
                 Make sure to disable the console and reboot before
                 proceeding.
        
              You'll need a 3.3 volt USB to TTL serial adapter, such as this
              `SparkFun FTDI Basic Breakout 3.3V`_.
        
              #. Mount the micro SD card containing the SD image you
                 flashed on your workstation PC.
        
              #. Edit the ``config.txt`` file on the VFAT partition,
                 adding a new line with the following content::
        
                    enable_uart=1
        
              #. Safely unmount the micro SD card, remove it from your
                 workstation, and insert it into the Raspberry Pi.
        
              #. Connect the adapter to your Raspberry Pi's UART and
                 to your workstation computer via USB, e.g. by following
                 `this AdaFruit guide`_.
        
              #. Connect a serial console program on your workstation to
                 the adapter, and power on the Raspberry Pi.
        
              #. When prompted, log in via the console. The default
                 username is ``fio``, and the default password is
                 ``fio``. You should change the password before
                 connecting to the network.
        
              #. Connect to the network using the following command::
        
                    sudo nmcli device wifi connect NETWORK_SSID password NETWORK_PASSWORD
        
                 Where ``NETWORK_SSID`` is your WiFi network's SSID, and
                 ``NETWORK_PASSWORD`` is the password.
        
              #. Safely shut down the Raspberry Pi, re-mount the SD
                 card on your host workstation, and delete the line you
                 added to ``config.txt``.
        
              #. Unmount the SD card from your workstation, insert it
                 into the Raspberry Pi, and reboot it.
        
              .. warning::
        
                 Do not skip the final steps. Functionality with the
                 serial console enabled is severely degraded.
        
              Your board will connect to the network you've saved after
              rebooting. You can now log in using SSH.
        
