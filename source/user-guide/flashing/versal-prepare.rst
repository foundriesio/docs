Preparation
-----------

.. attention::
   Replace the ``<factory>`` placeholder below with the name of your Factory.

#. Download the necessary files from ``https://app.foundries.io/factories/<factory>/targets``:

     a. Click the latest :guilabel:`Target` with the ``platform-devel`` :guilabel:`Trigger`.

          .. figure:: /_static/boards/generic-steps-1.png
            :width: 769
            :align: center

     #. Expand the :guilabel:`Runs` section corresponding with the name of the board and **download the Factory image**.
        For reference on how to boot using the JTAG port, download ``boot.bin`` from the **other** folder:

        |     ``lmp-factory-image-<machine-name>.wic.gz``
	|     ``boot.bin``

          .. figure:: /_static/boards/versal-steps-2.png
            :width: 769
            :align: center

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


		
