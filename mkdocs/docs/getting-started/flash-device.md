# Flash your Device

Note

To follow this section, you will need: - A
`supported board <ref-linux-supported>`.

-   Capable of booting from eMMC **(recommended if available)**
-   **Or** capable of booting from a suitable [microSD
    Card](https://elinux.org/RPi_SD_cards)
-   Wired or WiFi network with internet access.
-   Ethernet cable (if choosing Wired)
-   Console access to your hardware via display/keyboard **or** serial
    (if choosing WiFi)

## Download LmP system image

When you trigger a build, it produces build artifacts as an output which
can be downloaded from the `Targets` tab of your factory, as described
in `gs-watch-build`.

1.  Navigate to the `Targets` section of your Factory.

2.  Find your LmP platform build, denoted by the `Trigger` name:
    `platform-<tag>`.

    e.g: `lmp-factory-image-machine-name.wic.gz`

3.  Download it by clicking on its name in the list of artifacts.

<figure>
<img src="/_static/flash-device/artifacts.png" class="align-center" width="769" />
</figure>

## Flash LmP system image

Note

If you are developing on a platform that has eMMC available such as the
NXP iMX8MM-EVK, it is recommended that you boot from eMMC rather than
SD. Read the `ref-linux-supported` section for specific details on
flashing your system-image using the vendor provided tools.

We should provide a more comprehensive section specific to each device.
Essentially, we should overhaul the linux-targets section to include
device images, more details about each device, and bring it up to date
with what we support today

Linux

1.  Determine the disk you want to flash by finding the device with the
    `SIZE` that matches your SD card in the list below. Be sure to
    ignore partitions (where `TYPE` is `part`). Save the `NAME` for your
    SD card device to be used in a later step as the disk path. e.g:
    `/dev/mmcblk0`:

    bash host:~$, auto

    host:~$ lsblk -po +MODEL

    **Example Output**:

    bash host:~$, auto

    host:~$ lsblk -po +MODEL  
    NAME MAJ:MIN RM SIZE RO TYPE MOUNTPOINT MODEL /dev/mmcblk0 179:0 0
    29.8G 0 disk ├─/dev/mmcblk0p1 179:1 0 41.6M 0 part /mnt/boot
    └─/dev/mmcblk0p2 179:2 0 29.8G 0 part /mnt/otaroot /dev/zram0 254:0
    0 26G 0 disk /out /dev/nvme0n1 259:0 0 953.9G 0 disk SSDPEKKF010T8
    NVMe INTEL 1024GB

2.  Flash the disk.

    Replace `<system-image>`  
    Replace `/dev/mmcblk<X>` with your chosen disk path.

> bash host:~$, auto
>
> host:~$ gunzip -c &lt;system-image&gt; | sudo dd
> of=/dev/mmcblk&lt;X&gt; bs=4096k iflag=fullblock oflag=direct
> status=progress

macOS

1.  Determine the disk you want to flash by finding the device with the
    `SIZE` that matches your SD card in the list below. Be sure to
    ignore partitions (lines without the \* in the `SIZE`). Save the
    `IDENTIFIER` for your SD card device to be used in a later step as
    the disk path. e.g: `/dev/disk3`:

    bash host:~$, auto

    host:~$ diskutil list

    **Example Output**:

    bash host:~$, auto

    host:~$ diskutil list  
    /dev/disk3 (internal, physical):  
    \#: TYPE NAME SIZE IDENTIFIER 0: FDisk\_partition\_scheme \*15.5 GB
    disk3 1: Windows\_FAT\_32 boot 45.7 MB disk3s1 2: Linux 15.5 GB
    disk3s2

2.  Flash the disk.

    Replace `<system-image>`  
    Replace `/dev/disk<X>` with your chosen disk path.

> Warning
>
> It may be necessary to unmount the disk if macOS has auto-mounted it
> like so: `sudo diskutil unmount /dev/disk<X>`
>
> bash host:~$, auto
>
> host:~$ gunzip -c &lt;system-image&gt; | sudo dd of=/dev/disk&lt;X&gt;
> bs=4096k

Windows

Windows has no `dd` like tool built into the operating system to flash
your image to disk. In this case, we recommend you download and use
either **Win32 Disk Imager** or **Rufus**.

Note

Your system image is in a compressed wic.gz format. To follow these next
steps, you must extract it using a tool like
[7zip](https://www.7-zip.org/download.html) which will leave you with a
.wic image file.

**Using Rufus**

1.  Download and run [Rufus](https://rufus.ie).
2.  Select your disk.
3.  `SELECT` your `<system-image>`.
4.  `START` the flash procedure.

**Using Win32 Disk Imager**

1.  Download and run [Win32 Disk
    Imager](https://sourceforge.net/projects/win32diskimager/files/Archive/)
    as **Administrator**.
2.  Click the blue folder icon.
3.  Select your `<system-image>`
4.  Select your disk via the `Device` dropdown.
5.  Click `Write`
6.  Wait for the image to finish writing, and a **Write Successful**
    dialog will appear.

## Boot Device and Connect to the Network

ethernet

Ethernet works out of the box if a DHCP server is available on the local
network.

1.  Connect an Ethernet cable to the board.
2.  Remove the SD card from your computer, and insert it into the board.
3.  Apply power to the board.

Your board will connect to the network via Ethernet and will be ready to
connect within a minute or two of booting.

wifi

Generic

The LmP uses `nmcli` and `NetworkManager` to manage network  
connectivity. Once you have gained shell access to the device, you can
add a new WiFi SSID to connect to by using `nmcli`:

    sudo nmcli device wifi connect NETWORK_SSID password NETWORK_PASSWORD

**Access via Serial**

If you are starting without any network connectivity that could give you
shell access to your device, you will need to

**connect via serial** to execute the command. You may need to  
refer to your hardware vendor's documentation on serial access.

**Access interactively**

If your device has a video interface, you can attach it to a  
display, plug in a USB Keyboard and **execute the command
interactively**. Be sure to log out from your shell session after
completion when using this method.

Raspberry Pi 3/4

If you don't have Ethernet connectivity, you can connect to a WiFi
network by temporarily enabling the UART console on your Raspberry Pi
and running a command to connect to your WiFi network.

Note

While a hardware serial port is available, enabling it unfortunately
requires this device to run at significantly reduced speeds, and causes
serious Bluetooth instability. Make sure to disable the console and
reboot before proceeding.

You'll need a 3.3 volt USB to TTL serial adapter, such as this [Adafruit
USB to TTL Serial Cable](https://www.adafruit.com/product/954).

1.  Mount the micro SD card containing the SD image you flashed on your
    workstation PC.

2.  Edit the `config.txt` file on the VFAT `boot/` partition, adding a
    new line with the following content:

        enable_uart=1

3.  Safely unmount the micro SD card, remove it from your workstation,
    and insert it into the Raspberry Pi.

4.  Connect the adapter to your Raspberry Pi's UART and to your
    workstation computer via USB, e.g. by following [this Adafruit
    guide](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-5-using-a-console-cable/connect-the-lead).

5.  Connect a serial console program on your workstation to the adapter,
    and power on the Raspberry Pi.

6.  When prompted, log in via the console. The default username is
    `fio`, and the default password is `fio`. You should change the
    password before connecting to the network.

7.  Connect to the network using the following command:

        sudo nmcli device wifi connect NETWORK_SSID password NETWORK_PASSWORD

    Where `NETWORK_SSID` is your WiFi network's SSID, and
    `NETWORK_PASSWORD` is the password.

8.  Safely shut down the Raspberry Pi, re-mount the SD card on your host
    workstation, and delete the line you added to `config.txt`.

9.  Unmount the SD card from your workstation, insert it into the
    Raspberry Pi, and reboot it.

Warning

Do not skip the final steps. Functionality with the serial console
enabled is severely degraded.

Your board will connect to the network you've saved after rebooting. You
can now log in using SSH.

### Log in via SSH

Use `fio` as the username and `machine-name.local` as the hostname:

bash host:~$, auto

host:~$ ssh fio@&lt;machine-name&gt;.local

The default password is `fio`; we recommend changing it once logged in.

Note

Your device hostname will be defaulted to the value of the `machine:`
key value from your `factory-config.yml` Read the `ref-linux-supported`
section for a list of supported hardware and their `MACHINE` value.

**Here are some examples:**

`raspberrypi3-64.local`  
`imx8mmevk.local`  
`beaglebone-yocto.local`  
`intel-corei7-64.local`

For this to work, your PC needs to support
[zeroconf](https://en.wikipedia.org/wiki/Zero-configuration_networking)
the hostname must be otherwise unclaimed. If this doesn't work, you can
also log in by IP address. See `Troubleshooting <gs-troubleshooting>`
below for advice.

### Troubleshooting

If the above methods to connect your device to the network don't work,
try one of the following.

-   Temporarily enable and connect to the UART (see directions above in
    the WiFi section) and determine available IP addresses with:

Ethernet:

> bash host:~$, auto
>
> host:~$ ip addr show eth0 scope global

WiFi:

> bash host:~$, auto
>
> host:~$ ip addr show wlan0 scope global

-   Then connect by IP address:

> bash host:~$, auto
>
> host:~$ ssh fio@&lt;ip-address&gt;

-   List connected devices and their local IP addresses on your network
    router's administrative interface, and log in by IP address as
    above.

Make a section dedicated to the i.MX platform to link to in the "Flash
LmP system image" section note, regarding flashing eMMC.
