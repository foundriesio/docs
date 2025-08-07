Preparation
-----------

.. important::
   Ensure you replace the ``<factory>`` placeholder below with the name of your Factory.

#. Download necessary files from ``https://app.foundries.io/factories/<factory>/targets``

     a. Click the latest Target with the :guilabel:`platform` trigger.

     b. Expand the **run** in the :guilabel:`Runs` section which corresponds with the name of the board.
        **Download the Factory image for that machine.**
        For example::

             lmp-factory-image-<machine-name>.wic.gz
             u-boot-<machine-name>.itb
             imx-boot-<machine-name>

#. Extract the file ``lmp-factory-image-<machine-name>.wic.gz``::

      gunzip lmp-factory-image-<machine-name>.wic.gz

#. Expand the **run** in the :guilabel:`Runs` section which corresponds with the name of the board.
   Download the **mfgtools** for that machine, e.g., ``mfgtool-files-<machine-name>.tar.gz``.

#. Extract the file
   
   .. code-block:: console
      
         $ tar -zxvf mfgtool-files-<machine-name>.tar.gz

#. Organize all the files, mirroring the tree below::

      ├── lmp-factory-image-<machine-name>.wic.gz
      ├── u-boot-<machine-name>.itb
      ├── imx-boot-<machine-name>
      └── mfgtool-files-<machine-name>
          ├── bootloader.uuu
          ├── full_image.uuu
          ├── SPL-mfgtool
          ├── u-boot-mfgtool.itb
          ├── uuu
          └── uuu.exe
