.. _ref-rm_board_stm32mp1-disco:

STM32MP157 Discovery Kit
========================

CI Build
--------

Including STM OpenEmbedded layer requires accepting EULA. To enable EULA
acceptance in the CI job, EULA_stm32mp1disco variable needs to be set in the
factory-config.yml::

    ...
    lmp:
      params:
        ...
        EULA_stm32mp1disco: "1"
        ...


.. include:: generic-prepare.rst

Flashing
--------

Now, flash the ``lmp-factory-image-stm32mp1-disco.wic.gz`` retrieved from the
previous section to an SD Card. This contains the :term:`system image` that the
device will boot.

.. include:: generic-flashing.rst
