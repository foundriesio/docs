# Apalis iMX6 with the Ixora Carrier Board

## Hardware Preparation

Set up the board for updating using the manufacturing tools:

1.  Ensure that the power is off (SW1)

2.  Put the apalis-imx6 into Recovery Mode:

    > Remove the JP2 jumper from the board
    >
    > <figure>
    > <img src="/_static/boards/apalis-imx6-jp2.png" class="align-center" width="300" alt="JP2 location" /><figcaption aria-hidden="true">JP2 location</figcaption>
    > </figure>
    >
    > Connect the Micro-USB cable to the X9 connector
    >
    > <figure>
    > <img src="/_static/boards/apalis-imx6-usb.png" class="align-center" width="300" alt="USB location" /><figcaption aria-hidden="true">USB location</figcaption>
    > </figure>
    >
    > Connect the two bottom pads of JP4 as in the following images
    >
    > <figure>
    > <img src="/_static/boards/apalis-imx6-jp4.png" class="align-center" width="300" alt="Recovery jumper location" /><figcaption aria-hidden="true">Recovery jumper location</figcaption>
    > </figure>
    >
    > <figure>
    > <img src="/_static/boards/apalis-imx6-jp4-close.jpeg" class="align-center" width="300" alt="Recovery jumper setup" /><figcaption aria-hidden="true">Recovery jumper setup</figcaption>
    > </figure>

3.  Power on the board by pressing the SW1 button.

## Flashing

Once in serial downloader mode and connected to your PC, the evaluation
board should show up as a Freescale USB device.

Note

Device names and IDs can slightly differ from the steps below.

To go back to run mode, disconnect the jumper from the recovery pads
(JP4) and reconnect the JP2 jumper.

Power on the board to boot the new image.
