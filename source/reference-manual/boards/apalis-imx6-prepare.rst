Preparation
-----------

.. important:: 
   Ensure you replace the ``<factory>`` placeholder below with the name of your Factory.

#. Download necessary files from ``https://app.foundries.io/factories/<factory>/targets``:

   a. Click the latest Target with a ``platform`` trigger.

   b. Expand **run** in the :guilabel:`Runs` section corresponding with the name of the board.
   **Download the Factory image for that machine.**

   For example::

        lmp-factory-image-<machine-name>.wic.gz
        u-boot-<machine-name>.itb
        sit-<machine-name>.bin
        SPL-<machine-name>

#. Extract the file ``lmp-factory-image-apalis-imx6.wic.gz``::

      gunzip lmp-factory-image-apalis-imx6.wic.gz

#. Expand the **run** in the :guilabel:`Runs` section which corresponds with the board's mfgtool-files.
   **Download the tools for that machine.**


#. Extract ``mfgtool-files-apalis-imx6.tar.gz``:

   .. prompt::

         tar -zxvf mfgtool-files-apalis-imx6.tar.gz

#. Organize the files as in the tree below::

      ├── lmp-factory-image-<machine-name>.wic.gz
      ├── u-boot-<machine-name>.itb
      ├── sit-<machine-name>.bin
      ├── SPL-<machine-name>
      └── mfgtool-files-<machine-name>
          ├── bootloader.uuu
          ├── full_image.uuu
          ├── SPL-mfgtool
          ├── u-boot-mfgtool.itb
          ├── uuu
          └── uuu.exe
