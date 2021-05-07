# i.MX 6ULL Evaluation Kit

## Hardware Preparation

Set up the board for updating using the manufacturing tools:

<figure>
<img src="/_static/boards/imx6ullevk.png" class="align-center" width="400" alt="imx6ullevk" /><figcaption aria-hidden="true">imx6ullevk</figcaption>
</figure>

1.  **OPTIONAL** - Only required if you have a problems and/or want to
    see the boot console output.

    > Connect the micro-B end of the USB cable into debug port J1901.
    > Connect the other end of the cable to a PC acting as a host
    > terminal. One UART connection will appear on the PC. On a Linux
    > host for example:
    >
    >     $ ls -l /dev/serial/by-id/
    >     total 0
    >     lrwxrwxrwx 1 root root 13 Dec  3 13:09 usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0 -> ../../ttyUSB2
    >
    > Using a serial terminal program like minicom, connect to the port
    > with `if00` in the name (in this example ttyUSB2) and apply the
    > following configuration
    >
    > > -   Baud rate: 115200
    > > -   Data bits: 8
    > > -   Stop bit: 1
    > > -   Parity: None
    > > -   Flow control: None

2.  Ensure that the power is off (SW2001)

3.  Put the imx6ullevk into programing mode:

    > Switch SW602 to boot from serial downloader by setting to OFF, ON
    > (from 1-2 bit)
    >
    > <figure>
    > <img src="/_static/boards/imx6ullevk_SW1.png" class="align-center" width="300" alt="SW602 settings" /><figcaption aria-hidden="true">SW602 settings</figcaption>
    > </figure>

<table style="width:65%;">
<colgroup>
<col style="width: 15%" />
<col style="width: 16%" />
<col style="width: 33%" />
</colgroup>
<thead>
<tr class="header">
<th>D1/MODE1</th>
<th>D2/MODE0</th>
<th>BOOT MODE</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><blockquote>
<p>OFF</p>
</blockquote></td>
<td><blockquote>
<p>OFF</p>
</blockquote></td>
<td>Boot From Fuses</td>
</tr>
<tr class="even">
<td><strong>OFF</strong></td>
<td><strong>ON</strong></td>
<td><strong>Serial Downloader</strong></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>ON</p>
</blockquote></td>
<td><blockquote>
<p>OFF</p>
</blockquote></td>
<td>Internal Boot</td>
</tr>
<tr class="even">
<td><blockquote>
<p>ON</p>
</blockquote></td>
<td><blockquote>
<p>ON</p>
</blockquote></td>
<td>Reserved</td>
</tr>
</tbody>
</table>

> Switch SW601 to device microSD by setting to OFF, OFF, ON, OFF (from
> 1-4 bit)
>
> <figure>
> <img src="/_static/boards/imx6_sw601.png" class="align-center" width="300" alt="SW601 settings" /><figcaption aria-hidden="true">SW601 settings</figcaption>
> </figure>

<table style="width:97%;">
<colgroup>
<col style="width: 15%" />
<col style="width: 16%" />
<col style="width: 15%" />
<col style="width: 16%" />
<col style="width: 33%" />
</colgroup>
<thead>
<tr class="header">
<th>D1</th>
<th>D2</th>
<th>D3</th>
<th>D4</th>
<th>BOOT MODE</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><strong>OFF</strong></td>
<td><strong>OFF</strong></td>
<td><strong>ON</strong></td>
<td><strong>OFF</strong></td>
<td><strong>MicroSD</strong></td>
</tr>
<tr class="even">
<td>OFF</td>
<td>OFF</td>
<td>OFF</td>
<td>OFF</td>
<td>QSPI</td>
</tr>
<tr class="odd">
<td>OFF</td>
<td>ON</td>
<td>ON</td>
<td>OFF</td>
<td>EMMC</td>
</tr>
<tr class="even">
<td><blockquote>
<p>ON</p>
</blockquote></td>
<td><blockquote>
<p>ON</p>
</blockquote></td>
<td>OFF</td>
<td>ON</td>
<td>NAND</td>
</tr>
</tbody>
</table>

1.  Connect your computer to the EVK board via the USB OTG jack.
2.  Connect the plug of the 5V power supply to the DC power jack J2001.
3.  Power on the EVK board by sliding power switch SW2001 to ON.

## Flashing

Once in serial downloader mode and connected to your PC the evaluation
board should show up as a Freescale USB device.

To put the EVK into run mode, switch SW602 to `internal boot` by setting
to ON, OFF (from 1-2bit). This is the opposite of programming mode
described previously.

Power on the EVK board by sliding power switch SW2001 to ON.
