.. _ref-pg-spl-uboot:

U-Boot
======

Get the latest U-Boot support from either the board vendor or the community.
The current U-Boot versions supported in meta-lmp (u-boot-fio)
can be found `here <https://github.com/foundriesio/meta-lmp/tree/master/meta-lmp-base/recipes-bsp/u-boot>`_.
If there is no U-Boot support for the target board or if it supports an
old U-Boot version, the user should update/port to a newer U-Boot
version as supported in ``u-boot-fio``.

.. toctree::
   :maxdepth: 2

   pg-spl
   pg-spl-optee
   pg-spl-uboot-fragments
   pg-spl-uboot-env
