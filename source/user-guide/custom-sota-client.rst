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


Using the custom-sota-client Example
------------------------------------

We provide a `SOTA client`_ example in aktualizr-lite that serves as a great
starting place to experiment. The **meta-lmp** layer includes a recipe_ that
runs this example as the default SOTA client. Later, this serves as an example
to copy/paste into a Factory specific recipe.

.. _recipe:
   https://github.com/foundriesio/meta-lmp/tree/main/meta-lmp-base/recipes-sota/custom-sota-client

.. _SOTA client:
   https://github.com/foundriesio/aktualizr-lite/tree/master/examples/custom-client-cxx

Users can build this custom client into their LmP image with a small addition
to ``meta-subscriber-overrides.git``:

.. prompt:: bash host:~$

    git clone -b devel https://source.foundries.io/factories/<factory>/meta-subscriber-overrides.git
    cd meta-subscriber-overrides
    echo 'SOTA_CLIENT = "custom-sota-client"' >> conf/machine/include/lmp-factory-custom.inc

Forking the custom-sota-client
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Producing a factory-specific SOTA client can be done by:

 #. Creating a Git repository for your custom code. Copying the
    `examples/custom-client-cxx`_ directory is a good place to start.

 #. Copying the `custom-sota-client`_ recipe from **meta-lmp** into
    ``meta-subscriber-overrides/recipes-sota``.

 #. Changing the ``custom-sota-client_git.bb`` Git references (``SRC_URI``,
    ``BRANCH``, ``SRCREV``) to point at your new sources.

.. _examples/custom-client-cxx:
   https://github.com/foundriesio/aktualizr-lite/tree/master/examples/custom-client-cxx

.. _custom-sota-client:
   https://github.com/foundriesio/meta-lmp/tree/main/meta-lmp-base/recipes-sota/custom-sota-client
