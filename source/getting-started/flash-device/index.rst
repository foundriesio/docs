.. _getting-started-flash-device:

Flash your Device
=================

.. note::
   To follow this section, you will need:
    - A supported board.

      - Capable of booting from eMMC **(recommended if available)**
      - **Or** capable of booting from a suitable `microSD Card <https://elinux.org/RPi_SD_cards>`_

    - Wired or WiFi network with internet access.

      - Ethernet cable (if choosing Wired)
      - 3.3 volt USB to TTL Serial Cable (if choosing WiFi)

.. todo:: Link 'supported board' to section on supported boards when written.

.. _getting-started-download:

Download LmP system image
-------------------------

When you trigger a build, it produces build artifacts as an output which can be
downloaded from the **Targets** tab of your factory, as described in
:ref:`ref-watch-build`.

1. Navigate to the **MICROPLATFORM** section of your Factory.

2. Find your ``master``  LmP platform build, denoted by the **trigger name**:
   ``platform-master``.

   e.g: ``lmp-factory-image-machine-name.wic.gz``

3. Download it by clicking on its name in the list of artifacts.

.. figure:: /_static/flash-device/artifacts.png
   :width: 769
   :align: center

.. _getting-started-flash-image:

Flash LmP system image
----------------------

.. note::
   If you are developing on a platform that has eMMC available such as the NXP
   iMX8MM-EVK, it is recommended that you boot from eMMC rather than SD. Read the
   :ref:`ref-linux-targets` section for details on flashing your system-image using the vendor
   provided tools.

.. todo:: We should provide a more comprehensive section specific to each
   device. Essentially, we should overhaul the linux-targets section to include
   device images, more details about each device, and bring it up to date with
   what we support today

.. tabs::

   .. group-tab:: Linux

      1. Determine the disk you want to flash by finding the device with the
         ``SIZE`` that matches your SD card in the list below.  Be sure to ignore
         partitions (where ``TYPE`` is ``part``).  Save the ``NAME`` for your SD card device to
         be used in a later step as the disk path. e.g: ``/dev/mmcblk0``::

           lsblk -po +MODEL

         .. highlight:: none

         **Example Output**::

           $ lsblk -po +MODEL
           NAME             MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT                 MODEL
           /dev/mmcblk0     179:0    0  29.8G  0 disk
           ├─/dev/mmcblk0p1 179:1    0  41.6M  0 part /mnt/boot
           └─/dev/mmcblk0p2 179:2    0  29.8G  0 part /mnt/otaroot
           /dev/zram0       254:0    0    26G  0 disk /out
           /dev/nvme0n1     259:0    0 953.9G  0 disk                            SSDPEKKF010T8 NVMe INTEL 1024GB

      2. Flash the disk.

         | Replace ``<system-image>``
         | Replace ``/dev/mmcblk<X>`` with your chosen disk path.

       .. code-block:: shell

          gunzip -c <system-image> | sudo dd of=/dev/mmcblk<X> bs=4M iflag=fullblock oflag=direct status=progress

   .. group-tab:: macOS

      1. Determine the disk you want to flash by finding the device with the
         ``SIZE`` that matches your SD card in the list below.  Be sure to ignore
         partitions (lines without the * in the ``SIZE``).  Save the ``IDENTIFIER`` for your
         SD card device to be used in a later step as the disk path. e.g:
         ``/dev/disk3``::

           diskutil list

         .. highlight:: none

         **Example Output**::

           $ diskutil list
           /dev/disk3 (internal, physical):
              #:                       TYPE NAME                    SIZE       IDENTIFIER
              0:     FDisk_partition_scheme                        *15.5 GB    disk3
              1:             Windows_FAT_32 boot                    45.7 MB    disk3s1
              2:                      Linux                         15.5 GB    disk3s2

      2. Flash the disk.

         | Replace ``<system-image>``
         | Replace ``/dev/disk<X>`` with your chosen disk path.

        .. code-block:: shell

           gunzip -c <system-image> | sudo dd of=/dev/disk<X> bs=4M

   .. group-tab:: Windows

      Windows has no ``dd`` like tool built into the operating system to flash
      your image to disk. In this case, we recommend you download and use
      Etcher_.

      1. Download and run Etcher_.
      2. Select your ``<system-image>``.
      3. Select your disk.
      4. Flash it.

.. _getting-started-boot:

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

          .. tab:: Generic

	     The LmP uses ``nmcli`` and ``NetworkManager`` to manage network
             connectivity. Once you have gained shell access to the device, you can add a new
             WiFi SSID to connect to by using ``nmcli``::

                sudo nmcli device wifi connect NETWORK_SSID password NETWORK_PASSWORD

             **Access via Serial**

             If you are starting without any network connectivity that
             could give you shell access to your device, you will need to
	     **connect via serial** to execute the command. You may need to
             refer to your hardware vendor's documentation on serial access.

             **Access interactively**

	     If your device has a video interface, you can attach it to a
             display, plug in a USB Keyboard and **execute the command interactively**. Be
             sure to log out from your shell session after completion when using this method.

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
              `Adafruit USB to TTL Serial Cable`_.

              #. Mount the micro SD card containing the SD image you
                 flashed on your workstation PC.

              #. Edit the ``config.txt`` file on the VFAT ``boot/`` partition,
                 adding a new line with the following content::

                    enable_uart=1

              #. Safely unmount the micro SD card, remove it from your
                 workstation, and insert it into the Raspberry Pi.

              #. Connect the adapter to your Raspberry Pi's UART and
                 to your workstation computer via USB, e.g. by following
                 `this Adafruit guide`_.

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

.. _getting-started-login:

Log in via SSH
^^^^^^^^^^^^^^

.. highlight:: none

Use ``fio`` as the username and ``machine-name.local`` as the
hostname::

  ssh fio@<machine-name>.local

The default password is ``fio``; we recommend changing it once logged in.

.. note::
   Your device hostname hostname will be defaulted to the value of the
   ``machine:`` key value from your ``factory-config.yml`` e.g:

   | ``raspberrypi3-64.local``
   | ``imx8mmevk.local``
   | ``beaglebone-yocto.local``
   | ``intel-corei7-64.local``

.. todo::

   Link to section on machine names for each of our supported boards. This will
   probably be something we add in the "supported boards" section when we write
   it.

For this to work, your PC needs to support zeroconf_ the hostname must be
otherwise unclaimed. If this doesn't work, you can also log in by IP address. See
:ref:`Troubleshooting <getting-started-troubleshooting>` below for
advice.

.. _getting-started-troubleshooting:

Troubleshooting
^^^^^^^^^^^^^^^

If the above methods to connect your device to the network don't work, try one
of the following.

- Temporarily enable and connect to the UART (see directions above in
  the WiFi section) and determine available IP addresses with::

    # Ethernet
    ip addr show eth0 scope global

    # WiFi
    ip addr show wlan0 scope global

  Then connect by IP address::

    ssh fio@<ip-address>

- List connected devices and their local IP addresses on your network
  router's administrative interface, and log in by IP address as
  above.

.. _zeroconf:
   https://en.wikipedia.org/wiki/Zero-configuration_networking

.. _Adafruit USB to TTL Serial Cable:
   https://www.adafruit.com/product/954

.. _this Adafruit guide:
   https://learn.adafruit.com/adafruits-raspberry-pi-lesson-5-using-a-console-cable/connect-the-lead

.. _Etcher: https://www.balena.io/etcher/

.. todo::

     Make a section on our other supported boards to link to in the note in
     the header

.. todo::

     Make a section dedicated to the i.MX platform to link to in the "Flash LmP
     system image" section note, regarding flashing eMMC.

.. todo::

     Make links open in a new tab, rather than swallow the current window.
