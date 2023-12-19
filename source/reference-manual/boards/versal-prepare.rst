Preparation
-----------

.. important::
   Replace  ``<factory>`` with the name of your Factory.

#. Download the necessary files from ``https://app.foundries.io/factories/<factory>/targets``:

     a. Click the latest :guilabel:`Target` with the ``platform`` trigger.

     b. Expand the :guilabel:`Runs` section corresponding with the board.
        **Download the Factory image.** For example, ``lmp-factory-image-<machine-name>.wic.gz``.
        
        .. note::
           For reference on how to boot using the JTAG port, download ``boot.bin`` from the **other** folder.

#. Extract the file ``lmp-factory-image-<machine-name>.wic.gz``::

      gunzip lmp-factory-image-<machine-name>.wic.gz

#. Write the file to an SD card::

      dd if=lmp-factory-image-<machine-name>.wic of=/dev/xxx bs=1M status=progress

#. Plug the SD card in the Micro SD Versal slot.

   .. figure:: /_static/boards/vck190-slot.png
	:width: 400
	:align: center
      
#. Set the boot switches to SD mode.

    .. figure:: /_static/boards/vck190-sd-boot.png
	:width: 400
	:align: center

#. Power up the board.
