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

   | E.g: ``lmp-factory-image-imx6ullevk.wic.gz``
   |      ``SPL-imx6ullevk``
   |      ``u-boot-imx6ullevk.itb``

   .. figure:: /_static/boards/imx6-steps-2.png
      :align: center
      :width: 400
#. Extract the file ``lmp-factory-image-imx6ullevk.wic.gz``::

      gunzip lmp-factory-image-imx6ullevk.wic.gz

#. Expand the **run** in the :guilabel:`Runs` section which corresponds
   with the name of the board mfgtool-files and **download the tools for that
   machine.**

   E.g: ``imx6ullevk-mfgtools``

#. Download and extract the file ``mfgtool-files-imx6ullevk.tar.gz``::

      tar -zxvf mfgtool-files-imx6ullevk.tar.gz


#. Organize all the files like the tree below::

      ├── lmp-factory-image-imx6ullevk.wic
      ├── mfgtool-files-imx6ullevk
      │   ├── bootloader.uuu
      │   ├── full_image.uuu
      │   ├── SPL-mfgtool
      │   ├── u-boot-mfgtool.itb
      │   ├── uuu
      │   └── uuu.exe
      ├── SPL-imx6ullevk
      └── u-boot-imx6ullevk.itb
