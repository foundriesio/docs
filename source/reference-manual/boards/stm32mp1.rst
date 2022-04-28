.. _ref-rm_board_stm32mp1-disco:

STM32MP157 Discovery Kit
========================

FoundriesFactory CI Build
-------------------------

Including STM OpenEmbedded layer requires accepting EULA. When building locally
it is enough to accept EULA using interactive prompt. When building in CI this
isn't possible. To enable EULA acceptance in the CI job, ``EULA:stm32mp1disco``
variable needs to be set in the ``factory-config.yml``::

    ...
    lmp:
      params:
        ...
        EULA:stm32mp1disco: "1"
        ...

``factory-config.yml`` can be found in ci-scripts.git repository that is
created for each factory.

.. include:: generic-prepare.rst

Flashing
--------

Now, flash the ``lmp-factory-image-stm32mp1-disco.wic.gz`` retrieved from the
previous section to an SD Card. This contains the :term:`system image` that the
device will boot.

.. include:: generic-flashing.rst


Boot mode
---------

STM32MP157C-DK2 board has a dip switch that controls boot mode. Dip switch
covers BOOT0 and BOOT2 signals. They both have to be turned ON for the board
to boot from SD card.

.. figure:: /_static/boards/stm32mp1_boot_mode.png
     :width: 660
     :align: center
