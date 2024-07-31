.. _ug-custom-sota-client:

Customizing Over the Air Updates
================================

By default, Secure Over The Air update (SOTA), operates as a daemon process (:ref:`ref-aktualizr-lite`) which
periodically checks for updates. If an update is available, it will automatically download, and install
it to a device that is following the update tag.

This is not always the desired operation. There are a couple ways to control this operation:

#. Callbacks
#. Custom Update Agent
#. Command Line Interface - CLI (Aktualizr-lite Manual Mode)

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

Command Line Interface - CLI (Aktualizr-lite Manual Mode)
---------------------------------------------------------

The `aktualizr-lite` executable can be invoked to perform individual operations allowing more control over the update flow.

.. warning:: The Command Line Interface is on beta stage,
    and is subject to change over the next releases.

.. note:: In order to use the run individual `aktualizr-lite` commands,
    the `aktualizr-lite` service needs to be stopped with ``sudo systemctl stop aktualizr-lite``
    and/or disabled with ``sudo systemctl disable aktualizr-lite``.

.. note:: If lmp-device-register is used,
    the `--start-daemon 0` is recommended
    in order to avoid starting aktualizr-lite daemon automatically.

.. prompt::

      $ aktualizr-lite --help
      aktualizr-lite command line options:
      -h [ --help ]         Print usage
      -v [ --version ]      Prints current aktualizr-lite version
      -c [ --config ] arg   Configuration file or directory path
      --loglevel arg        Set log level 0-5 (trace, debug, info, warning, error,
                            fatal)
      --update-name arg     Name or version of the target to be used in pull,
                            install, and update commands. default=latest
      --install-mode arg    Optional install mode. Supported modes:
                            [delay-app-install]. By default both ostree and apps
                            are installed before reboot
      --interval arg        Override uptane.polling_secs interval to poll for
                            updates when in daemon mode
      --json arg            Output targets information as json when running check
                            and list commands
      --src-dir arg         Directory that contains an offline update bundle.
                            Enables offline mode for check, pull, install, and
                            update commands
      --command arg         Command to execute: run, status, finalize, check, list,
                            install, pull, update, daemon


View Current Status
^^^^^^^^^^^^^^^^^^^

To view the current status of the device::

    sudo aktualizr-lite status

Fetch TUF Metadata and List Updates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``check`` command will refresh the Targets metadata from the OTA server,
and present you with a list of available Targets::

   sudo aktualizr-lite check

The ``list`` command will present the same output,
but will **not** refresh the Targets metadata from the OTA server::

   sudo aktualizr-lite list

Both commands can be used in conjunction with the ``--json 1`` option,
which will change the output format to JSON,
and will by default omit other log outputs.


Apply Update
^^^^^^^^^^^^

The ``update`` command pulls and installs the latest available update to the device,
after updating the TUF metadata.
This includes both OSTree and Docker app Targets::

   sudo aktualizr-lite update

To update to a specific build number or target name,
the ``--update-name`` option can be used::

   sudo aktualizr-lite update --update-name <build_number_or_name>

A reboot command will be required after installing an update,
followed by the execution on the  ``run`` command to finalize the update process::

   sudo aktualizr-lite run


.. warning::
   Downgrading to a older Target is neither recommended or supported by our team;
   doing so may lead to unverified corner cases.
   Only choose to do so mindfully.
   For any update, always test before rolling out to production devices.

The command line interface also allows the update steps to be performed individually,
by calling the ``check``, ``pull`` and ``install`` commands individually.
This allows for a higher level of control over the update process.

The ``check`` command updates the Targets metadata.

The ``pull`` command pulls the delta between the currently installed Target and the one specified with the ``--update-name`` option.
If no target is specified, the latest one is used.

The ``install``  command installs the Target, which should have been previously pulled.
It yields an error if the specified Target has not been pulled before, and also supports the ``--update-name`` option.

It is necessary to verify the return codes for each command to guarantee the correct update process flow,
as detailed in the next section.

Exit Codes
^^^^^^^^^^

The commands set exit codes (``echo $?``) that can be used by the caller to act accordingly.
The possible return codes for the CLI commands are listed below:

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

Automating the use of CLI Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The individual command line interface operations,
especially ``check``, ``pull``, ``install`` and ``run``,
can be used to automate an update flow like to the one implemented by the main *aktualizr-lite* daemon,
while allowing for limited customizations.

This `sample bash script
<https://raw.githubusercontent.com/foundriesio/sotactl/main/scripts/aklite-cli-example.sh>`_
illustrates the usage of CLI operations and proper return codes handling.
