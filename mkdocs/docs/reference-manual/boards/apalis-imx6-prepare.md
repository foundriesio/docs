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

    E.g: `lmp-factory-image-apalis-imx6.wic.gz`  
         `SPL-apalis-imx6`  
         `u-boot-apalis-imx6.itb`

    <figure>
    <img src="/_static/boards/apalis-imx6-steps-2.png" class="align-center" width="400" />
    </figure>

3.  Extract the file `lmp-factory-image-apalis-imx6.wic.gz`:

        gunzip lmp-factory-image-apalis-imx6.wic.gz

4.  Expand the **run** in the `Runs` section which corresponds with the
    name of the board mfgtool-files and **download the tools for that
    machine.**

    E.g: `apalis-imx6-mfgtools`

5.  Download and extract the file `mfgtool-files-apalis-imx6.tar.gz`:

        tar -zxvf mfgtool-files-apalis-imx6.tar.gz

6.  Organize all the files like the tree below:

        ├── lmp-factory-image-apalis-imx6.wic
        ├── mfgtool-files-apalis-imx6
        │   ├── bootloader.uuu
        │   ├── full_image.uuu
        │   ├── SPL-mfgtool
        │   ├── u-boot-mfgtool.itb
        │   ├── uuu
        │   └── uuu.exe
        ├── SPL-apalis-imx6
        └── u-boot-apalis-imx6.itb
