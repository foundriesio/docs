.. _ref-rm_board_stm32mp15-disco:

STM32MP157 Discovery Kit
========================

FoundriesFactory CI Build
-------------------------

.. important::
   Including the STM™ OpenEmbedded layer requires accepting the EULA.
   When building locally, it is enough to accept the EULA from an interactive prompt.
   When building in CI, this is not possible.
   To enable EULA acceptance in the CI job, the variable ``EULA_stm32mp15disco`` needs to be set in the ``factory-config.yml``
   ::

      ...
      lmp:
        params:
          ...
          EULA_stm32mp15disco: "1"
          ...

  ``factory-config.yml`` can be found in the ``ci-scripts.git`` repo for your Factory.

.. include:: generic-prepare.rst

Flashing
--------

Flash  ``lmp-factory-image-stm32mp15-disco.wic.gz`` to an SD Card.
This contains the bootable :term:`system image`.

.. include:: generic-flashing.rst


Boot Mode
---------

The STM32MP157C-DK2 has a dip switch that controls boot mode.
The dip switch covers ``BOOT0`` and ``BOOT2`` signals.
Turn both ``ON`` for the board to boot from SD card.

.. figure:: /_static/boards/stm32mp1_boot_mode.png
     :width: 660
     :align: center
