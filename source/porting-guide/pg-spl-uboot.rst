.. _ref-pg-spl-uboot:

U-Boot
======

You can get the latest U-Boot support from either the board vendor, or the community.
The current U-Boot versions supported in ``meta-lmp`` (``u-boot-fio``)
can be found `in the repo <https://github.com/foundriesio/meta-lmp/tree/main/meta-lmp-base/recipes-bsp/u-boot>`_.

It is possible that there is no U-Boot support for the target board, or there is only support for an old U-Boot version.
In this case, you should update/port to a newer U-Boot version, as supported in ``u-boot-fio``.

.. toctree::
   :maxdepth: 2

   pg-spl
   pg-spl-optee
   pg-spl-uboot-fragments
   pg-spl-uboot-env
