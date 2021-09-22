Preparation
-----------

Ensure you replace the ``<factory>`` placeholder below with the name of your
Factory.

#. Download necessary files from ``https://app.foundries.io/factories/<factory>/targets``

     a. Click the latest :guilabel:`Target` with the ``platform-devel`` :guilabel:`Trigger`.

          .. figure:: /_static/boards/generic-steps-1.png
            :width: 769
            :align: center

     #. Expand the **run** in the :guilabel:`Runs` section which corresponds
        with the name of the board and **download the Factory image for that
        machine.**

        | E.g: 
        |     ``lmp-factory-image-<machine-name>.wic.gz``
        |     ``u-boot-<machine-name>.itb``
        |     ``sit-<machine-name>.bin``
        |     ``imx-boot-<machine-name>`` or ``imx-boot-<machine-name>-nohdmi``

          .. figure:: /_static/boards/imx-steps-2.png
            :width: 769
            :align: center

#. Extract the file ``lmp-factory-image-<machine-name>.wic.gz``::

      gunzip lmp-factory-image-<machine-name>.wic.gz

#. Expand the **run** in the :guilabel:`Runs` section which corresponds
   with the name of the board mfgtool-files and **download the tools for that
   machine.**

   E.g: ``mfgtool-files-<machine-name>.tar.gz``

#. Download and extract the file ``mfgtool-files-<machine-name>.tar.gz``::

      tar -zxvf mfgtool-files-<machine-name>.tar.gz

#. Organize all the files like the tree below::

      ├── lmp-factory-image-<machine-name>.wic
      ├── u-boot-<machine-name>.itb
      ├── sit-<machine-name>.bin 
      ├── imx-boot-<machine-name> or imx-boot-<machine-name>-nohdmi
      └── mfgtool-files-<machine-name>
            ├── bootloader.uuu
            ├── full_image.uuu
            ├── imx-boot-mfgtool
            ├── uuu
            └── uuu.exe
