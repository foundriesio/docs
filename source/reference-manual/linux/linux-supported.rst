.. _ref-linux-supported:

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

Changing Machines
-----------------

Changing the Machine your Factory is configured to produce builds for is as
simple as changing the value of ``machines:`` in your ``factory-config.yml``
file which is part of the ``ci-scripts.git`` repo. 

First, clone your ci-scripts repository. Replace ``<factory>`` with the name of
your own Factory::

  git clone https://source.foundries.io/factories/<factory>/ci-scripts.git

Then, to change from an ``imx8mmevk`` to ``raspberrypi4-64`` for example, commit
and push the following change to ``factory-config.yml``:

**Before:**

.. code-block::
   :linenos:
   :emphasize-lines: 7

     lmp:
       params:
         IMAGE: lmp-factory-image
         DOCKER_COMPOSE_APP: "1"
     
       machines:
       - imx8mmevk

**After:**

.. code-block::
   :linenos:
   :emphasize-lines: 7 

     lmp:
       params:
         IMAGE: lmp-factory-image
         DOCKER_COMPOSE_APP: "1"
     
       machines:
       - raspberrypi4-64

Demonstration
~~~~~~~~~~~~~

  .. asciinema:: ../../_static/asciinema/change-machine.cast
     :rows: 24
     :cols: 80
