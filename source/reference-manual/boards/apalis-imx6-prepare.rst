Preparation
-----------

Ensure you replace the ``<factory>`` placeholder below with the name of your
Factory.

Download necessary files from ``https://app.foundries.io/factories/<factory>/targets``

#. Click the latest Target with the :guilabel:`platform-devel` trigger.

   .. figure:: /_static/boards/generic-steps-1.png
      :align: center
      :width: 300

#. Expand the **run** in the :guilabel:`Runs` section (by clicking on the ``+`` sign) which corresponds
   with the name of the board and **download the Factory image for that
   machine.**

   | E.g: ``lmp-factory-image-apalis-imx6.wic.gz``
   |      ``SPL-apalis-imx6``
   |      ``u-boot-apalis-imx6.itb``

   .. figure:: /_static/boards/apalis-imx6-steps-2.png
      :align: center
      :width: 400
#. Extract the file ``lmp-factory-image-apalis-imx6.wic.gz``::

      gunzip lmp-factory-image-apalis-imx6.wic.gz

#. Expand the **run** in the :guilabel:`Runs` section which corresponds
   with the name of the board mfgtool-files and **download the tools for that
   machine.**

   E.g: ``apalis-imx6-mfgtools``

#. Download and extract the file ``mfgtool-files-apalis-imx6.tar.gz``::

      tar -zxvf mfgtool-files-apalis-imx6.tar.gz

#. Organize all the files like the tree below::

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
