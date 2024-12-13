.. _gs-flash-device:

Flashing Your Device
====================

.. note::

  The initial Factory setup and build is finished very quick.
  Follow its status with steps listed in :ref:`gs-watch-build` page.

Prerequisites and Pre-Work
--------------------------

   - A :ref:`supported board <ref-linux-supported>` which is either:

      - Capable of booting from eMMC **(supported by default if available)**
      - **Or** capable of booting from a suitable `microSD Card <https://elinux.org/RPi_SD_cards>`_

   - Wired or WiFi network with internet access.

      - Ethernet cable (if choosing Wired)
      - Console access to your hardware via UART serial (if choosing WiFi)

.. note::

   If you're starting out and prefer emulation over a physical board, refer to the guide :ref:`gs-emulation-with-qemu`.
   This guide will walk you through "Flashing the Image," allowing you to move on to :ref:`gs-register`.

.. _gs-download:

Downloading the System Image
----------------------------

After a successful build, the FoundriesFactory™ Platform produces build artifacts which can be downloaded from the :guilabel:`Targets` tab of your :term:`Factory`.

#. Navigate to the :guilabel:`Targets` tab of your Factory.

    .. figure:: /_static/flash-device/devel.png
        :width: 769
        :align: center
        :alt: Targets tab showing prebuilt-target

        Target tab

#. Expand the Target information by clicking on the one named ``prebuilt-target`` on it.
   This shows a link to the Factory image artifact.
   Download the Factory image for your machine:

    | E.g: ``lmp-base-console-image-<machine_name>.wic.gz``

    .. figure:: /_static/flash-device/artifacts.png
        :width: 769
        :align: center
        :alt: Targets tab displaying available artifacts

        Target artifacts

.. note::
    Most platforms require more than the ``lmp-base-console-image-<machine_name>.wic.gz`` artifact for flashing.
    The required artifacts are board specific and listed on respective pages under :ref:`ref-boards` or under :ref:`ref-qemu`.
    Targets publish all needed files for each platform under :guilabel:`Runs`.

.. important::
    When you create platform builds later on, the Factory image and artifacts may follow a slightly different naming pattern, such as ``lmp-factory-image-<machine_name>``.

.. _gs-flash-image:

Flashing the Image
------------------

The flashing procedure is board specific and we cover separate steps in :ref:`ref-boards`.
Please refer to this section for specifics on flashing your system image using the vendor provided tools.
See :ref:`ref-qemu` for booting Qemu images.

.. note::
   The :term:`Linux microPlatform` (LmP) enforces eMMC boot whenever possible as this is the path to enable all security features it provides. So for platforms with available eMMC, such as the NXP® i.MX EVKs, booting from eMMC rather than SD is highly recommended and enabled by default.

.. _gs-boot:

Booting and Connecting to the Network
-------------------------------------

After flashing and booting the board with the respective steps for your hardware, follow these steps to connect to the network.

.. note::
    By default, the ``username`` and ``password`` to log in your device after boot are ``fio``/``fio``. We recommend changing them once you are in development.

.. content-tabs::

   .. tab-container:: ethernet
      :title: Ethernet (Recommended)

      Ethernet works out of the box if a DHCP server is available on the local network.

      Connect an Ethernet cable to the board. Your board will connect to the network via Ethernet soon after booting.

   .. tab-container:: wifi
      :title: WiFi

      LmP uses ``nmcli`` and ``NetworkManager`` to manage network connectivity.

      If you are starting without any network connectivity that would give you shell access to your device (like SSH), you will need to **connect via UART serial** before setting up a WiFi connection.
      You may need to refer to your hardware vendor's documentation on UART serial access. We cover the steps to access UART serial for some platforms in :ref:`ref-boards`.

      Once you have gained shell access to the device, log in with ``fio``/``fio`` username and password. After logged, you can add a new WiFi SSID by using ``nmcli``:

      .. prompt:: bash device:~$, auto

         device:~$ sudo nmcli device wifi connect NETWORK_SSID password NETWORK_PASSWORD

.. _gs-login:

Logging in via SSH
^^^^^^^^^^^^^^^^^^

To login via SSH, run:

.. prompt:: bash host:~$, auto

   host:~$ ssh fio@<machine-name>.local

Where ``fio`` is the username and ``<machine-name>`` is the hostname of your device. The default password is ``fio``.

By default, your device hostname is set to a unique string that specify the platform chosen during Factory creation (``machine``). Check :ref:`ref-linux-supported` for a list of supported platform and their ``machine`` values.

.. tip::
   Here are some examples of default hostnames:

   | ``raspberrypi4-64.local``
   | ``intel-corei7-64.local``
   | ``imx8mm-lpddr4-evk.local``

.. note::
    For this to work, your PC needs to support zeroconf_. The hostname must be unclaimed.

    If this does not work, see :ref:`Troubleshooting <gs-troubleshooting>` below for advice.

.. _gs-troubleshooting:

Troubleshooting
"""""""""""""""

If the above methods to SSH into your board do not work, there are additional things to try.

1. Get the IP address of your device:

- Temporarily enable and connect to the UART serial (detailed steps for some platforms can be found in :ref:`ref-boards`) and determine available IP addresses with:

  * Ethernet:

    .. prompt:: bash device:~$, auto

       device:~$ ip addr show eth0 scope global

  * WiFi:

    .. prompt:: bash device:~$, auto

       device:~$ ip addr show wlan0 scope global

- **Or** list the connected devices and their local IP addresses on your network router's administrative interface.

2. Connect to the device by IP address:

 .. prompt:: bash host:~$, auto

    host:~$ ssh fio@<ip-address>

.. _zeroconf:
   https://en.wikipedia.org/wiki/Zero-configuration_networking

.. _Adafruit USB to TTL Serial Cable:
   https://www.adafruit.com/product/954

.. _the Adafruit guide:
   https://learn.adafruit.com/adafruits-raspberry-pi-lesson-5-using-a-console-cable/connect-the-lead

.. _Win32 Disk Imager: https://sourceforge.net/projects/win32diskimager/files/Archive/

.. _7zip: https://www.7-zip.org/download.html

.. _Rufus: https://rufus.ie

