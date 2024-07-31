.. _ug-custom-sota-client:

Customizing Over the Air Updates
================================

By default, Secure Over The Air update (SOTA), operates as a daemon process (:ref:`ref-aktualizr-lite`) which
periodically checks for updates. If an update is available, it will automatically download, and install
it to a device that is following the update tag.

This is not always the desired operation. There are a couple ways to control this operation:

#. Callbacks
#. Custom Update Agent
#. Command Line Interface

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

Using The Custom SOTA Client Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The example `SOTA client`_ is a great place to start experimenting.
The ``meta-lmp`` layer includes a recipe_ that runs this example as the default SOTA client.
Later, this can serve as an example to copy/paste into a Factory specific recipe.

.. _recipe:
   https://github.com/foundriesio/meta-lmp/tree/main/meta-lmp-base/recipes-sota/custom-sota-client

.. _SOTA client:
   https://github.com/foundriesio/sotactl

Users can build this custom client into their LmP image with a small addition to ``meta-subscriber-overrides.git``:

.. prompt:: bash host:~$

    git clone -b devel https://source.foundries.io/factories/<factory>/meta-subscriber-overrides.git
    cd meta-subscriber-overrides
    echo 'SOTA_CLIENT = "custom-sota-client"' >> conf/machine/include/lmp-factory-custom.inc

Forking the Custom SOTA Client
""""""""""""""""""""""""""""""

Producing a factory-specific SOTA client can be done by:

 #. Creating a Git repository for your custom code.
    Cloning the `sotactl`_ repository and adding your repository as the remote is a good place to start.

 #. Copying the `custom-sota-client`_ recipe from ``meta-lmp`` into ``meta-subscriber-overrides/recipes-sota``.

 #. Changing the ``custom-sota-client_git.bb`` Git references (``SRC_URI``, ``BRANCH``, ``SRCREV``) to point at your new sources.

.. _sotactl:
   https://github.com/foundriesio/sotactl

.. _custom-sota-client:
   https://github.com/foundriesio/meta-lmp/tree/main/meta-lmp-base/recipes-sota/custom-sota-client

Custom SOTA Client Work Modes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
By default, the example `SOTA client`_ works as a daemon updating a device to the latest version once it becomes available.
In addition to the default daemon mode, users can run it as a CLI utility and perform specific steps of the update process separately.

.. prompt:: bash

    sotactl --help
    Usage:
        sotactl [cmd] [options]
    Supported commands: check install run pull daemon
    Default command is "daemon"


* ``check`` - updates the device's TUF repo with the latest Factory's TUF metadata or with the TUF metadata specified in the offline update bundle, and checks if there is a newer than currently installed Target.
* ``pull`` - pulls the delta between the currently installed and the specified one.
* ``install`` - installs the previously pulled Target; yields an error if the specified Target has not been pulled before.
* ``run`` - finalizes the installed Target; confirms an update after reboot on a new rootfs version and/or starts the updated apps.

Command Line Interface (experimental)
-------------------------------------
The `aktualizr-lite` daemon executable can be invoked to perform individual operations allowing more control over the update flow.
**This interface is subject to change over the next releases.**

.. prompt::

      $ aktualizr-lite --help
      aktualizr-lite command line options:
      --update-lockfile arg         If provided, an flock(2) is applied to this
                                    file before performing an update in daemon mode
      -h [ --help ]                 print usage
      -v [ --version ]              Current aktualizr version
      -c [ --config ] arg           configuration file or directory
      --loglevel arg                set log level 0-5 (trace, debug, info, warning,
                                    error, fatal)
      --repo-server arg             URL of the Uptane repo repository
      --ostree-server arg           URL of the Ostree repository
      --primary-ecu-hardware-id arg hardware ID of primary ecu
      --update-name arg             optional name of the update when running
                                    "update". default=latest
      --install-mode arg            Optional install mode. Supported modes:
                                    [delay-app-install]. By default both ostree and
                                    apps are installed before reboot
      --interval arg                Override uptane.polling_secs interval to poll
                                    for update when in daemon mode.
      --command arg                 Command to execute: run, status, finalize,
                                    check, list, install, pull, update, daemon

Available commands:

* ``list`` - lists the targets present in the currently stored TUF metadata.
* ``check`` - updates the device's TUF repo with the latest Factory's TUF metadata, and lists the available targets.
* ``pull`` - pulls the delta between the currently installed Target and the one specified with the `--update-name` option. If no target is specified, the latest one is used.
* ``install`` - installs the previously pulled Target; yields an error if the specified Target has not been pulled before.
* ``run`` - finalizes the installation of the Target; confirms an update after reboot on a new rootfs version and/or starts the updated apps. A ``finalize`` alias is provided for this command for backwards compatibility.
* ``update`` - performs a complete update process, including the ``check``, ``pull`` and ``install`` operations. The ``run`` operation still needs to be manually invoked after the reboot.

Exit Codes
^^^^^^^^^^
The commands set exit codes (``echo $?``) that can be used by the caller to act accordingly.
The possible return codes for the CLI commands are listed bellow:

**Return codes for** ``check``, ``pull``, ``install``, **and** ``update`` **commands:**

- *0*: Success
    - Operation executed successfully
- *3*: Success
    - Unable to fetch updated TUF metadata, but stored metadata is valid
- *4*: Failure
    - Failed to update TUF metadata
- *6*: Failure
    - There is no target in the device TUF repo that matches a device tag and/or hardware ID
- *8*: Failure
    - Failed to find the ostree commit and/or all Apps of the Target to be installed in the provided source bundle (offline mode only)
- *11*: Failure
    - Invalid TUF metadata
- *12*: Failure
    - TUF metadata is expired
- *13*: Failure
    - Unable to fetch TUF metadata
- *14*: Failure
    - TUF metadata not found in the provided path (offline mode only)
- *15*: Failure
    - The bundle metadata is invalid (offline mode only).There are a few reasons why the metadata might be invalid:
        1. One or more bundle signatures is/are invalid.
        2. The bundle targets' type, whether CI or production, differs from the device's type.
        3. The bundle targets' tag differs from the device's tag.
- *16*: Success
    - Update is required: new target version available
- *17*: Success
    - Update is required: apps need synchronization
- *18*: Success
    - Update is required: rollback to a previous target
- *20*: Failure
    - Selected target not found
- *1*: Failure
    - Unknown error

**Return codes for** ``pull``, ``install``, **and** ``update`` **commands:**

- *21*: Failure
    - Unable to find target to rollback to after a failure to start Apps at boot on a new version of sysroot
- *30*: Failure
    - Unable to pull/install: there is an installation that needs completion
- *50*: Failure
    - Unable to download target
- *60*: Failure
    - There is no enough free space to download the target
- *70*: Failure
    - The pulled target content is invalid, specifically App compose file is invalid
- *75*: Failure
    - Selected target is already installed
- *102*: Failure
    - Attempted to install a previous version

**Return codes for** ``install``, **and** ``update`` **commands:**

- *10*: Success
    - Execute the `run` subcommand to finalize installation
- *80*: Failure
    - Unable read target data, make sure it was pulled
- *90*: Failure
    - Reboot is required to complete the previous boot firmware update. After reboot the update attempt must be repeated from the beginning

**Return codes for** ``install``, ``run``,  **and** ``update`` **commands:**

- *100*: Success
    - Reboot to finalize installation
- *5*: Success
    - Reboot to finalize bootloader installation
- *120*: Failure
    - Installation failed, rollback initiated but requires reboot to finalize

**Return codes for** ``run`` **command:**

- *40*: Failure
    - No pending installation to run
- *99*: Failure
    - Offline installation failed, rollback performed
- *110*: Failure
    - Online installation failed, rollback performed
- *130*: Failure
    - Installation failed and rollback operation was not successful

Automating the use of CLI operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The individual command line interface operations, specially `check`, `pull`, `install` and `run`, can be used to
automate an update flow like to the one implemented by the main *aktualizr-lite* daemon, while allowing for limited
customizations.

.. highlight:: bash
   :linenothreshold: 1

Sample bash script illustrating usage of CLI operations and return codes handling::

    #!/bin/env bash

    # Relevant aktualizr-lite CLI return codes for controlling execution flow
    OK=0
    CHECKIN_OK_CACHED=3

    UPDATE_NEW_VERSION=16
    UPDATE_SYNC_APPS=17
    UPDATE_ROLLBACK=18

    REBOOT_REQUIRED_BOOT_FW=90
    REBOOT_REQUIRED_ROOT=100

    # Commands
    reboot_cmd="/sbin/reboot"
    aklite_cmd="/bin/aktualizr-lite"

    # Interval between each update server polling (seconds)
    interval=60

    # Complete previous installation, if pending
    $aklite run; ret=$?
    if [ $ret -eq $REBOOT_REQUIRED_ROOT ]; then
        echo "A system reboot is required to finalize the pending installation."
        exit 1
    fi

    while true; do
        echo "Checking for updates..."
        $aklite_cmd check; ret=$?
        if [ $ret -eq $UPDATE_NEW_VERSION -o $ret -eq $UPDATE_SYNC_APPS -o $ret -eq $UPDATE_ROLLBACK ]; then
            echo "There is a target that is meant to be installed (check returned $ret). Pulling..."
            $aklite_cmd pull; ret=$?
            if [ $ret -eq $OK ]; then
                echo "Pull operation successful. Installing..."
                $aklite_cmd install; ret=$?
                if [ $ret -eq $REBOOT_REQUIRED_ROOT -o $ret -eq $REBOOT_REQUIRED_BOOT_FW ]; then
                    echo "Installation completed, reboot required ($ret)"
                    break
                elif [ $ret -eq $OK ]; then
                    echo "Installation completed, no reboot needed"
                    continue
                else
                    echo "Installation failed with error $ret"
                fi
            else
                echo "Pull operation failed with error $ret"
            fi
        elif [ $ret -eq $OK -o $ret -eq $CHECKIN_OK_CACHED ]; then
            echo "No update is needed"
        else
            echo "Check operation failed with error $ret"
        fi
        echo "Sleeping $interval seconds..."
        sleep $interval
    done

    echo "Rebooting ($aklite_cmd)..."
    $aklite_cmd
