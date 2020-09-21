.. _linux-supported:

Supported Machines
==================

The :ref:`ref-factory-definition` (``ci-scripts.git``) contains a ``machines:``
key value pair in the ``factory-config.yml`` file. When the value is changed,
the next build you perform by pushing to the ``lmp-manifest.git`` or
``meta-subscriber-overrides.git`` repositories will pass the updated value to
Yocto and begin producing targets for the ``MACHINE`` you have set.

.. note::

   If you are switching machines and your new machine has a different
   architecture, you will need to adjust the value of ``containers.platforms``
   in your ``factory-config.yml`` accordingly, otherwise Docker containers will
   continue to be built for the previous architecture.

.. csv-table:: **Supported Boards**
   :file: ../../_static/csv/supported-boards.csv
   :widths: 30, 30
   :header-rows: 1
