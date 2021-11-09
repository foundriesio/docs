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

   | E.g: ``lmp-factory-image-am64xx-sk.wic.gz``
   
   .. figure:: /_static/boards/am64xx-sk-steps-2.png
      :align: center
      :width: 400
#. Extract the file ``lmp-factory-image-am64xx-sk.wic.gz``::

      gunzip lmp-factory-image-am64xx-sk.wic.gz