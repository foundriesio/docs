Preparation
-----------

Ensure you replace the ``<factory>`` placeholder below with the name of your
Factory.

Download necessary files from ``https://app.foundries.io/factories/<factory/targets``

#. Click the latest Target with the :guilabel:`platform-devel` trigger.

   .. figure:: /_static/boards/generic-steps-1.png
      :align: center
      :width: 300

#. Expand the **run** in the :guilabel:`Runs` section (by clicking on the ``+`` sign) which corresponds
   with the name of the board and **download the Factory image for that
   machine.**

   | E.g: ``lmp-factory-image-<machine_name>.wic.gz``
   | and: ``imx-boot-<machine_name>``

   .. figure:: /_static/boards/imx-steps-2.png
      :align: center
      :width: 300
#. Extract the file ``lmp-factory-image-<machine_name>.wic.gz``::

      gunzip lmp-factory-image-<machine_name>.wic.gz

#. Expand the **run** in the :guilabel:`Runs` section which corresponds
   with the name of the board mfgtool-files and **download the tools for that
   machine.**

   E.g: ``<machine_name>-mfgtools``

#. Download and extract the file ``mfgtool-files-<machine_name>.tar.gz``::

      tar -zxvf mfgtool-files-<machine_name>.tar.gz


#. Organize all the files like the tree below::

      ├── imx-boot-<machine_name>
      ├── lmp-factory-image-<machine_name>.wic
      └── mfgtool-files-<machine_name>
            ├── bootloader.uuu
            ├── full_image.uuu
            ├── imx-boot-mfgtool
            ├── uuu
            └── uuu.exe
