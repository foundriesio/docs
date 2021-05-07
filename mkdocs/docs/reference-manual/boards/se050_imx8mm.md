# i.MX 8MMini Evaluation Kit with SE050ARD

This document will walk a developer through the steps of installing a
FoundriesFactory image with the SE050 hardware enabled onto the NXP
imx8mmevk that is connected to the NXP OM-SE050ARD development platform.

An image created in the factory with the SE050 enabled will not boot on
boards without the SE050 properly attached.

## Attaching the SE050

Connect the OM-SE050ARD Arduino Compatible Development Kit to the
imx8mmevk as follows:

Using four male to male jumper wires (Arduino Compatible Pin size)
connect the two boards.

<figure>
<img src="/_static/boards/imx8mmevk_J1004.png" class="align-center" width="400" alt="imx8mmevk" /><figcaption aria-hidden="true">imx8mmevk</figcaption>
</figure>

<figure>
<img src="/_static/boards/imx8mmevk_J1004_pinout.png" class="align-center" width="400" alt="imx8mmevk i2c pinout" /><figcaption aria-hidden="true">imx8mmevk i2c pinout</figcaption>
</figure>

<figure>
<img src="/_static/boards/se050ard.png" class="align-center" width="400" alt="SE050ARD" /><figcaption aria-hidden="true">SE050ARD</figcaption>
</figure>

Connect the signals as follows:

<table style="width:57%;">
<colgroup>
<col style="width: 15%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr class="header">
<th>Signal</th>
<th>imx8mmevk</th>
<th>OM-SE050ARD</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>SCL</td>
<td>J1004 pin 3</td>
<td>J2 pin 10</td>
</tr>
<tr class="even">
<td>SDA</td>
<td>J1004 pin 5</td>
<td>J2 pin 9</td>
</tr>
<tr class="odd">
<td>VDD_3V3</td>
<td>J1004 pin 1</td>
<td>J8 pin 5</td>
</tr>
<tr class="even">
<td>GND</td>
<td>J1004 pin 7</td>
<td>J2 pin 7</td>
</tr>
</tbody>
</table>

Alternatively use J22 on OM-SE050ARD and connect as follows

<table style="width:53%;">
<colgroup>
<col style="width: 13%" />
<col style="width: 19%" />
<col style="width: 19%" />
</colgroup>
<thead>
<tr class="header">
<th>Signal</th>
<th>imx8mmevk</th>
<th>OM-SE050ARD</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>SCL</td>
<td>J1004 pin 3</td>
<td>J22 pin 4</td>
</tr>
<tr class="even">
<td>SDA</td>
<td>J1004 pin 5</td>
<td>J22 pin 1</td>
</tr>
<tr class="odd">
<td>VDD_3V3</td>
<td>J1004 pin 1</td>
<td>J22 pin 2</td>
</tr>
<tr class="even">
<td>GND</td>
<td>J1004 pin 7</td>
<td>J22 pin 3</td>
</tr>
</tbody>
</table>

Be sure that the jumpers on the SE050 evaluation board are set as
follows:

<figure>
<img src="/_static/boards/se050ard_jumpers.png" class="align-center" width="400" alt="SE050 Jumper Settings" /><figcaption aria-hidden="true">SE050 Jumper Settings</figcaption>
</figure>

Lastly the connected boards should look like this:

<figure>
<img src="/_static/boards/se050ard_imx8mm.png" class="align-center" width="400" alt="Wire Connections Between Boards" /><figcaption aria-hidden="true">Wire Connections Between Boards</figcaption>
</figure>

## Installing the FoundriesFactory Image

Download the images that have the SE050 enabled from the factory
following the instructions in the iMX8MMevk board.
