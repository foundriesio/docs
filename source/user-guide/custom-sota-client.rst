.. _ug-custom-sota-client:

Custom Update Agents
====================

This section shows how to create a custom update agent, "SOTA client"
for your platform. :ref:`ref-aktualizr-lite` is a general purpose
SOTA client that fits many needs. However, some types of products
require more control over the update agent than aktualizr-lite and
it's "hooks" system provides. In these cases, a custom SOTA client
can be written in C++ using the aktualizr-lite API_.

.. _API:
   https://github.com/foundriesio/aktualizr-lite/blob/master/include/aktualizr-lite/api.h


Using the custom-sota-client
----------------------------

The meta-lmp layer includes a recipe_ that will run aktualizr-lite's
example `SOTA client`_. This serves as a great starting place to
experiment. Later, it can serve as an example to copy/paste into
Factory specific recipe.

.. _recipe:
   https://github.com/foundriesio/meta-lmp/tree/master/meta-lmp-base/recipes-sota/custom-sota-client

.. _SOTA client:
   https://github.com/foundriesio/aktualizr-lite/tree/master/examples/custom-client-cxx

Setting up the files
--------------------

Users can build the custom client into their LmP image with a simple
change to ``meta-subscriber-overrides.git``:

.. prompt:: bash host:~$

    git clone -b devel https://source.foundries.io/factories/<factory>/meta-subscriber-overrides.git
    cd meta-subscriber-overrides
    echo 'SOTA_CLIENT = "custom-sota-client"' >> conf/machine/include/lmp-factory-custom.inc

Forking the custom-sota-client
------------------------------

The procedure for producing a factory-specific SOTA client can
be by:

 #. Create a Git repository with custom code. Copying the
    ``examples/custom-client-cxx`` directory is a good place to start.

 #. Copy the ``custom-sota-client`` recipe from meta-lmp into the
    factory's meta-subscriber-overrides.git's ``recipes-sota`` directory.

 #. Custom the ``custom-sota-client_git.bb`` Git references to point
    at the new repository.

