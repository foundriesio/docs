.. _ug-custom-sota-client:

Customizing Over The Air Updates
================================

By default, Secure Over The Air update (SOTA), operates as a daemon process (ref:`ref-aktualizr-lite`) which
periodically checks for updates. If an update is available, it will automatically download, and install
it to a device that is following the update tag.

This is not always the desired operation. There are a couple ways to control this operation:

#. Callbacks
#. Custom Update Agent

Callbacks
---------

Aktualizr-lite provides the ability to run an executable at the following OTA operations:

* Before checking in — check-for-update-pre  return: none
* After checking in  — check-for-update-post return: OK or FAILED: reason
* Before a download  — download-pre          return: none
* After a download   — download-post         return: OK or FAILED: reason
* Before an install  — install-pre           return: none
* After an install   — install-post          return: NEEDS_COMPLETION, OK, or FAILED: reason
* After a reboot     — install-final-pre     return: none

A simple recipe is in `aktualizr-callback`_ and a sample script is in `callback-handler`_.

.. _`aktualizr-callback`:
   https://github.com/foundriesio/meta-lmp/blob/main/meta-lmp-base/recipes-sota/aktualizr/aktualizr-callback_1.0.bb

.. _`callback-handler`:
   https://github.com/foundriesio/meta-lmp/blob/main/meta-lmp-base/recipes-sota/aktualizr/aktualizr-callback/callback-handler

Custom Update Agents
--------------------

This section shows how to create a custom update agent—"SOTA client"—for your platform.
:ref:`ref-aktualizr-lite` is a general purpose SOTA client that fits many needs.
However, some cases require more control over the update agent than aktualizr-lite and the "hooks" system can provide.
In these cases, a custom SOTA client can be written in C++ using the aktualizr-lite API_.

.. _API:
   https://github.com/foundriesio/aktualizr-lite/blob/master/include/aktualizr-lite/api.h

Using the Custom SOTA Client Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The example `SOTA client`_ in aktualizr-lite is a great place to start experimenting.
The ``meta-lmp`` layer includes a recipe_ that runs this example as the default SOTA client.
Later, this can serve as an example to copy/paste into a Factory specific recipe.

.. _recipe:
   https://github.com/foundriesio/meta-lmp/tree/main/meta-lmp-base/recipes-sota/custom-sota-client

.. _SOTA client:
   https://github.com/foundriesio/aktualizr-lite/tree/master/examples/custom-client-cxx

Users can build this custom client into their LmP image with a small addition to ``meta-subscriber-overrides.git``:

.. prompt:: bash host:~$

    git clone -b devel https://source.foundries.io/factories/<factory>/meta-subscriber-overrides.git
    cd meta-subscriber-overrides
    echo 'SOTA_CLIENT = "custom-sota-client"' >> conf/machine/include/lmp-factory-custom.inc

Forking the custom SOTA Client
""""""""""""""""""""""""""""""

Producing a factory-specific SOTA client can be done by:

 #. Creating a Git repository for your custom code.
    Copying the `examples/custom-client-cxx`_ directory is a good place to start.

 #. Copying the `custom-sota-client`_ recipe from ``meta-lmp`` into ``meta-subscriber-overrides/recipes-sota``.

 #. Changing the ``custom-sota-client_git.bb`` Git references (``SRC_URI``, ``BRANCH``, ``SRCREV``) to point at your new sources.

.. _examples/custom-client-cxx:
   https://github.com/foundriesio/aktualizr-lite/tree/master/examples/custom-client-cxx

.. _custom-sota-client:
   https://github.com/foundriesio/meta-lmp/tree/main/meta-lmp-base/recipes-sota/custom-sota-client

Custom SOTA Client Work Modes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
By default, the example `SOTA client`_ works as a daemon updating a device to the latest version once it becomes available.
In addition to the default daemon mode, users can run it as a CLI utility and perform specific steps of the update process separately.

.. prompt:: bash

    /build-custom/custom-sota-client --help
    Usage:
        custom-sota-client [cmd] [options]
    Supported commands: check install run pull daemon
    Default command is "daemon"

* ``check`` - updates the device's TUF repo with the latest Factory's TUF metadata or with the TUF metadata specified in the offline update bundle, and checks if there is a newer than currently installed Target.
* ``pull`` - pulls the delta between the currently installed and the specified one.
* ``install`` - installs the previously pulled Target; yields an error if the specified Target has not been pulled before.
* ``run`` - finalizes the installed Target; confirms an update after reboot on a new rootfs version and/or starts the updated apps.