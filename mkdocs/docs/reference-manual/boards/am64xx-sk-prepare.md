# Preparation

Ensure you replace the `<factory>` placeholder below with the name of
your Factory.

Download necessary files from
`https://app.foundries.io/factories/<factory>/targets`

1.  Click the latest Target with the `platform-devel` trigger.

    <figure>
    <img src="/_static/boards/generic-steps-1.png" class="align-center" width="300" />
    </figure>

2.  Expand the **run** in the `Runs` section (by clicking on the `+`
    sign) which corresponds with the name of the board and **download
    the Factory image for that machine.**

    E.g: `lmp-factory-image-am64xx-sk.wic.gz`

    <figure>
    <img src="/_static/boards/am64xx-sk-steps-2.png" class="align-center" width="400" />
    </figure>

3.  Extract the file `lmp-factory-image-am64xx-sk.wic.gz`:

        gunzip lmp-factory-image-am64xx-sk.wic.gz
