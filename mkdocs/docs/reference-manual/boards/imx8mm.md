# i.MX 8M Mini Evaluation Kit

## Hardware Preparation

Set up the board for updating using the manufacturing tools:

<figure>
<img src="/_static/boards/imx8mmevk.png" class="align-center" width="600" alt="imx8mmevk" /><figcaption aria-hidden="true">imx8mmevk</figcaption>
</figure>

1.  **OPTIONAL** - Only required if you have a problems and/or want to
    see the boot console output.

    > Connect the micro-B end of the USB cable into debug port J901.
    > Connect the other end of the cable to a PC acting as a host
    > terminal. Two UART connections will appear on the PC. On a Linux
    > host for example:
    >
    >     $ ls -l /dev/serial/by-id/
    >     total 0
    >     lrwxrwxrwx 1 root root 13 Dec 18 11:09 usb-FTDI_Dual_RS232-if00-port0 -> ../../ttyUSB0
    >     lrwxrwxrwx 1 root root 13 Dec 18 11:09 usb-FTDI_Dual_RS232-if01-port0 -> ../../ttyUSB1
    >
    > Using a serial terminal program like minicom, connect to the port
    > with `if01` in the name (in this example ttyUSB0) and apply the
    > following configuration
    >
    > > -   Baud rate: 115200
    > > -   Data bits: 8
    > > -   Stop bit: 1
    > > -   Parity: None
    > > -   Flow control: None

2.  Ensure that the power is off (SW101)

3.  Put the imx8mmevk into programing mode:

    > Switch SW1101 to ON, OFF, ON, OFF (from 1-4 bit) and switch SW1102
    > bit 10 to OFF as shown below.
    >
    > <figure>
    > <img src="/_static/boards/imx8mmevk_SW.png" class="align-center" width="600" alt="SW1101 and SW1102 programing settings" /><figcaption aria-hidden="true">SW1101 and SW1102 programing settings</figcaption>
    > </figure>

4.  Connect your computer to the EVK board via the USB Type-C port 1
    `Download` J301 jack.

5.  Connect the USB Type-C power plug to the port 2 `Power` J302 jack.

6.  Power on the EVK board by sliding power switch SW101 to ON.

## Flashing

Once in serial downloader mode and connected to your PC the evaluation
board should show up as an NXP USB device.

To put the EVK into run mode, switch SW1101 and SW1102 to eMMC setting.

Power on the EVK board by sliding power switch SW101 to ON.
