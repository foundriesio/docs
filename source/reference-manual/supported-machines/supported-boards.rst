.. _ref-linux-supported:

Supported Machines
==================

.. important::
   Not all boards listed here may have a equal level of support.
   Please reach out to us if you have any questions or need assistance.

The :ref:`ref-factory-definition` (``ci-scripts.git``) contains a ``machines:``
key value pair in the ``factory-config.yml`` file. When the value is changed,
the next build you perform by pushing to the ``lmp-manifest.git`` or
``meta-subscriber-overrides.git`` repositories will pass the updated value to
the Yocto Project's tools
and begin producing targets for the ``MACHINE`` you have set.

.. note::

   If you are switching machines and your new machine has a different
   architecture, you will need to adjust the value of ``containers.platforms``
   in your ``factory-config.yml`` accordingly, otherwise Docker containers will
   continue to be built for the previous architecture.

.. csv-table:: **Supported Boards**
   :file: supported-boards.csv
   :widths: 30, 30
   :header-rows: 1
