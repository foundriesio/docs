Preparation
-----------

.. important::

   Ensure you replace ``<factory>`` With the name of your Factory.

#. Download the necessary files from ``https://app.foundries.io/factories/<factory>/targets``

     a. Click the latest Target with the ``platform`` Trigger.

     b. Expand the :guilabel:`Runs` section which corresponds with the board.
        **Download the Factory image for that machine**::

          lmp-partner-arduino-image-<machine-name>.wic.gz
          u-boot-<machine-name>.itb
          sit-<machine-name>.bin
          imx-boot-<machine-name>

#. Extract ``lmp-partner-arduino-image-<machine-name>.wic.gz``:
   
   .. code-block:: console
        
      $ gunzip lmp-partner-arduino-image-<machine-name>.wic.gz

#. Expand the :guilabel:`Runs` section which corresponds with the board.
   **Download the corresponding mfgtool files**, e.g., ``mfgtool-files-<machine-name>.tar.gz``.

#. Extract the files:

   .. code-block:: console

      $ tar -zxvf mfgtool-files-<machine-name>.tar.gz

#. Organize the files, mirroring the tree below::

      ├── lmp-partner-arduino-image-<machine-name>.wic
      ├── u-boot-<machine-name>.itb
      ├── sit-<machine-name>.bin 
      ├── imx-boot-<machine-name>
      └── mfgtool-files-<machine-name>
            ├── bootloader.uuu
            ├── full_image.uuu
            ├── imx-boot-mfgtool
            ├── uuu
            └── uuu.exe
