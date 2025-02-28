.. _ug-custom-sota-client:

Customizing Over the Air Updates
================================

By default, Secure Over The Air (SOTA) update operates as a daemon process (:ref:`ref-aktualizr-lite`) which
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


* ``check`` - updates the device's repo for The Update Framework (TUF) with the latest Factory's TUF metadata or with the TUF metadata specified in the offline update bundle, and checks if there is a newer than currently installed Target.
* ``pull`` - pulls the delta between the currently installed and the specified one.
* ``install`` - installs the previously pulled Target; yields an error if the specified Target has not been pulled before.
* ``run`` - finalizes the installed Target; confirms an update after reboot on a new rootfs version and/or starts the updated apps.

Command Line Interface - CLI (Aktualizr-lite Manual Mode)
---------------------------------------------------------

The ``aktualizr-lite`` executable can be invoked to perform individual operations allowing more control over the update flow.

.. note:: In order to use the run individual `aktualizr-lite` commands,
    the ``aktualizr-lite`` service needs to be stopped with ``sudo systemctl stop aktualizr-lite``
    and/or disabled with ``sudo systemctl disable aktualizr-lite``.

.. note:: If lmp-device-register is used,
    Using ``--start-daemon 0`` is recommended
    in order to avoid starting the aktualizr-lite daemon automatically.

.. prompt::

      $ aktualizr-lite --help
      Usage:
        aktualizr-lite [command] [flags]

      Commands:
        daemon      Start the update agent daemon
        update      Update TUF metadata, download and install the selected target
        pull        Download the selected target data to the device, to allow a install operation to be performed
        install     Install a previously pulled target
        list        List the available targets, using current TUF metadata information. No TUF update is performed
        check       Update the device TUF metadata, and list the available targets
        status      Show information of the target currently running on the device
        finalize    Finalize installation by starting the updated apps
        run         Alias for the finalize command
        rollback    Rollback to the previous successfully installed target [experimental]

      Flags:
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
        --command arg         Command to be executed


Available commands for CLI
^^^^^^^^^^^^^^^^^^^^^^^^^^

update
""""""

The ``update`` command pulls and installs the latest available update to the device,
after updating the TUF metadata.
This includes both OSTree and Docker app Targets::

   sudo aktualizr-lite update

To update to a specific build number or Target name,
the ``--update-name`` option can be used::

   sudo aktualizr-lite update --update-name <build_number_or_name>

.. warning::
   Downgrading to a older Target is neither recommended or supported by our team;
   doing so may lead to unverified corner cases.
   Only choose to do so mindfully.
   For any update, always test before rolling out to production devices.

.. note::
   Since LmP v95, aktualizr-lite won't automatically do a downgrade
   when all available targets have a version lower than the current one.
   In order to allow an automatic downgrade to occur in such situations,
   the ``auto-downgrade`` package option has to be set in the aktualizr recipe::

      $ cat meta-subscriber-overrides.git/recipes-sota/aktualizr/aktualizr_%.bbappend
      PACKAGECONFIG:append = " auto-downgrade"

When the OSTree image was changed,
a reboot command is be required after installing the update,
followed by the execution on the  ``run`` command to finalize the update process.
The exit code can be used to identify if such reboot is or not required.

The command line interface also allows the update steps to be performed individually,
by calling the ``check``, ``pull`` and ``install`` commands individually.
This allows for a higher level of control over the update process.

**Exit Codes**

- *0*: Success
   - Installation successful. No reboot needed
- *100*: Success
   - Installation succeeded. Reboot to finalize
- *5*: Success
   - Installation succeeded. Reboot to finalize bootloader installation
- *4*: Failure
   - Failure to handle TUF metadata: Check logs for more information
- *6*: Failure
   - There is no target in the device TUF repo that matches a device tag and/or hardware ID
- *8*: Failure
   - Failed to find the OSTree commit and/or all Apps of the Target to be installed in the provided source bundle (offline mode only)
- *11*: Failure
   - Failed to update TUF metadata: TUF metadata is invalid
- *12*: Failure
   - Failed to update TUF metadata: TUF metadata is expired
- *13*: Failure
   - Failed to update TUF metadata: Download error
- *14*: Failure
   - Failed to update TUF metadata: TUF metadata not found in the provided path (offline mode only)
- *15*: Failure
   - The bundle metadata is invalid (offline mode only).There are a few reasons why the metadata might be invalid:
       1. One or more bundle signatures is/are invalid.
       2. The bundle targets` type, whether CI or production, differs from the device`s type.
       3. The bundle targets` tag differs from the device`s tag.
- *20*: Failure
   - There is no target that matches the specified name or version
- *21*: Failure
   - Unable to find target to rollback to after a failure to start Apps at boot on a new version of sysroot
- *30*: Failure
   - Unable to perform operation: there is an installation that needs completion
- *50*: Failure
   - Unable to download target
- *60*: Failure
   - There is not enough free space to download the target
- *70*: Failure
   - The pulled target content is invalid: App compose file is invalid
- *110*: Failure
   - Installation failed, rollback done successfully
- *120*: Failure
   - Installation failed, rollback initiated but requires reboot to finalize
- *130*: Failure
   - Installation failed and rollback operation was not successful
- *1*: Failure
   - An error occurred while running the command. Check logs for more information

run
"""

Finalize the installation or rollback when a reboot was required,
starting the target applications.
It is possible that an error is detected at this stage,
which may lead to a rollback being initiated. 

**Exit Codes**

- *0*: Success
   - Installation / rollback finalized successfully
- *110*: Failure
   - Finalization failed. A rollback was performed successfully
- *120*: Failure
   - Finalization failed. A rollback was started but requires a reboot to finalize
- *130*: Failure
   - Finalization failed. A rollback was attempted and failed
- *40*: Failure
   - There is no pending installation to be finished
- *1*: Failure
   - An error occurred while running the command. Check logs for more information

check
"""""

The ``check`` command will refresh the Targets metadata from the OTA server,
and present a list of available Targets::

   sudo aktualizr-lite check

It can used in conjunction with the ``--json 1`` option,
which will change the output format to JSON,
and will, by default, omit other log outputs.

**Exit Codes**

- *0*: Success
   - TUF is up to date. No Target update required
- *3*: Success
   - Unable to update TUF metadata, using cached metadata
- *16*: Success
   - Update is required - new target version available
- *17*: Success
   - Update is required - apps need synchronization
- *18*: Success
   - Update is required - rollback to a previous target
- *4*: Failure
   - Failure to handle TUF metadata: Check logs for more information
- *6*: Failure
   - There is no target in the device TUF repo that matches a device tag and/or hardware ID
- *8*: Failure
   - Failed to find the OSTree commit and/or all Apps of the Target to be installed in the provided source bundle (offline mode only)
- *11*: Failure
   - Failed to update TUF metadata: TUF metadata is invalid
- *12*: Failure
   - Failed to update TUF metadata: TUF metadata is expired
- *13*: Failure
   - Failed to update TUF metadata: Download error
- *14*: Failure
   - Failed to update TUF metadata: TUF metadata not found in the provided path (offline mode only)
- *15*: Failure
   - The bundle metadata is invalid (offline mode only).There are a few reasons why the metadata might be invalid:
       1. One or more bundle signatures is/are invalid.
       2. The bundle targets` type, whether CI or production, differs from the device`s type.
       3. The bundle targets` tag differs from the device`s tag.
- *1*: Failure
   - An error occurred while running the command. Check logs for more information

list
""""

The ``list`` command works in a similar way as ``check``,
presenting the same type of output,
but will **not** refresh the Targets metadata from the OTA server::

   sudo aktualizr-lite list

This command also allows the use of the ``--json 1`` option.

**Exit Codes**

- *3*: Success
   - Cached TUF metadata is valid. No Target update is required
- *16*: Success
   - Update is required - new target version available
- *17*: Success
   - Update is required - apps need synchronization
- *18*: Success
   - Update is required - rollback to a previous target
- *4*: Failure
   - Failure to handle TUF metadata: Check logs for more information
- *6*: Failure
   - There is no target in the device TUF repo that matches a device tag and/or hardware ID
- *8*: Failure
   - Failed to find the OSTree commit and/or all Apps of the Target to be installed in the provided source bundle (offline mode only)
- *1*: Failure
   - An error occurred while running the command. Check logs for more information

pull
""""

Download the update data to the device,
allowing a ``install`` operation to be called next.

**Exit Codes**

- *0*: Success
   - Target successfully downloaded
- *4*: Failure
   - Failure to handle TUF metadata: Check logs for more information
- *6*: Failure
   - There is no target in the device TUF repo that matches a device tag and/or hardware ID
- *8*: Failure
   - Failed to find the OSTree commit and/or all Apps of the Target to be installed in the provided source bundle (offline mode only)
- *20*: Failure
   - There is no target that matches the specified name or version
- *21*: Failure
   - Unable to find target to rollback to after a failure to start Apps at boot on a new version of sysroot
- *30*: Failure
   - Unable to perform operation: there is an installation that needs completion
- *50*: Failure
   - Unable to download target
- *60*: Failure
   - There is not enough free space to download the target
- *70*: Failure
   - The pulled target content is invalid: App compose file is invalid
- *1*: Failure
   - An error occurred while running the command. Check logs for more information

install
"""""""

Install a previously pulled target.

A reboot and finalization using the ``run`` is required when the OSTree image was changed.
This is indicated by the command exit code.

**Exit Codes**

- *0*: Success
   - Installation successful. No reboot needed
- *100*: Success
   - Installation succeeded. Reboot to finalize
- *5*: Success
   - Installation succeeded. Reboot to finalize bootloader installation
- *4*: Failure
   - Failure to handle TUF metadata: Check logs for more information
- *6*: Failure
   - There is no target in the device TUF repo that matches a device tag and/or hardware ID
- *8*: Failure
   - Failed to find the OSTree commit and/or all Apps of the Target to be installed in the provided source bundle (offline mode only)
- *20*: Failure
   - There is no target that matches the specified name or version
- *21*: Failure
   - Unable to find target to rollback to after a failure to start Apps at boot on a new version of sysroot
- *30*: Failure
   - Unable to perform operation: there is an installation that needs completion
- *50*: Failure
   - Target download data not found. Make sure to call pull operation first
- *110*: Failure
   - Installation failed, rollback done successfully
- *120*: Failure
   - Installation failed, rollback initiated but requires reboot to finalize
- *130*: Failure
   - Installation failed and rollback operation was not successful
- *1*: Failure
   - An error occurred while running the command. Check logs for more information


.. _ref-aklite-command-line-interface-rollback:

rollback
""""""""

.. warning:: The rollback command is in beta stage,
    and is subject to change.

The ``rollback`` command can be used to cancel the current installation and revert the system to the previous successfully installed Target.
No download operation is done in that case.

If there is no installation being done, the current running Target is marked as failing.
This avoids having it automatically installed again,
and an installation of the previous successful Target is performed.
In that situation, the installation is preceded by a download (pull) operation.

Like in a regular installation, the exit code can be used to identify if a reboot is required in to finalize the rollback.

**Exit Codes**

- *0*: Success
   - Rollback executed successfully. No reboot required
- *100*: Success
   - Rollback installation started successfully. Reboot required
- *5*: Success
   - Rollback installation started successfully. Reboot required to update bootloader
- *8*: Failure
   - Failed to find the OSTree commit and/or all Apps of the Target to be installed in the provided source bundle (offline mode only)
- *21*: Failure
   - Unable to find target to rollback to after a failure to start Apps at boot on a new version of sysroot
- *50*: Failure
   - Unable to download target
- *60*: Failure
   - There is not enough free space to download the target
- *70*: Failure
   - The pulled target content is invalid: App compose file is invalid
- *110*: Failure
   - Rollback failed, reverted back to previous running version
- *120*: Failure
   - Rollback failed, reverting back to previous running version. A reboot is required
- *130*: Failure
   - Rollback failed, and failed to revert back to previous running version
- *1*: Failure
   - An error occurred while running the command. Check logs for more information

Automating the use of CLI Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The individual command line interface operations,
especially ``check``, ``pull``, ``install`` and ``run``,
can be used to automate an update flow like to the one implemented by the main *aktualizr-lite* daemon,
while allowing for limited customizations.

This `sample bash script
<https://raw.githubusercontent.com/foundriesio/sotactl/main/scripts/aklite-cli-example.sh>`_
illustrates the usage of CLI operations and proper return codes handling.

Creating Custom Logic for Update Decision
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The exit code of ``check`` and ``list`` commands
can be used to decide if an ``update`` should be performed,
as exemplified in the previous section.
By using this code,
a script can easily use the same decision logic that is employed by aktualizr-lite daemon.

If a custom decision process is required,
the use of the JSON output of both commands is recommended, enabled with ``--json 1``.
When enabling this command line option,
additional output is suppressed by default,
and the standard output text of the command can be parsed directly.
The format of the JSON output can be relied upon when creating a custom script.
Future versions will keep compatibility with the current format.

Here is an example of JSON output.

.. code-block:: json

    [
        {
            {
                "apps" :
                [
                        {
                                "name" : "app_100",
                                "on" : true,
                                "uri" : "hub.foundries.io/my-factory/app_100@sha256:<value>"
                        }
                ],
                "name" : "intel-corei7-64-lmp-92",
                "version" : 92
        },
        {
                "apps" :
                [
                        {
                                "name" : "app_100",
                                "on" : true,
                                "uri" : "hub.foundries.io/my-factory/app_100@sha256:<value>"
                        },
                        {
                                "name" : "app_200",
                                "on" : true,
                                "uri" : "hub.foundries.io/my-factory/app_200@sha256:<value>"
                        },
                        {
                                "name" : "app_300",
                                "on" : true,
                                "uri" : "hub.foundries.io/my-factory/app_300@sha256:<value>"
                        }
                ],
                "current" : true,
                "name" : "intel-corei7-64-lmp-93",
                "version" : 93
        },
        {
                "apps" :
                [
                        {
                                "name" : "app_100",
                                "on" : true,
                                "uri" : "hub.foundries.io/my-factory/app_100@sha256:<value>"
                        },
                        {
                                "name" : "app_200",
                                "on" : true,
                                "uri" : "hub.foundries.io/my-factory/app_200@sha256:<value>"
                        },
                        {
                                "name" : "app_300",
                                "on" : true,
                                "uri" : "hub.foundries.io/my-factory/app_300@sha256:<value>"
                        }
                ],
                "name" : "intel-corei7-64-lmp-94",
                "newer" : true,
                "version" : 94
        },
        {
                "apps" :
                [
                        {
                                "name" : "app_100",
                                "on" : true,
                                "uri" : "hub.foundries.io/my-factory/app_100@sha256:<value>"
                        },
                        {
                                "name" : "app_200",
                                "on" : true,
                                "uri" : "hub.foundries.io/my-factory/app_200@sha256:<value>"
                        },
                        {
                                "name" : "app_300",
                                "on" : true,
                                "uri" : "hub.foundries.io/my-factory/app_300@sha256:<value>"
                        }
                ],
                "failed" : true,
                "name" : "intel-corei7-64-lmp-99",
                "newer" : true,
                "version" : 99
        },
        {
                "apps" :
                [
                        {
                                "name" : "app_100",
                                "on" : true,
                                "uri" : "hub.foundries.io/my-factory/app_100@sha256:<value>"
                        },
                        {
                                "name" : "app_200",
                                "on" : true,
                                "uri" : "hub.foundries.io/my-factory/app_200@sha256:<value>"
                        },
                        {
                                "name" : "app_300",
                                "on" : true,
                                "uri" : "hub.foundries.io/my-factory/app_300@sha256:<value>"
                        }
                ],
                "name" : "intel-corei7-64-lmp-100",
                "newer" : true,
                "reason" : "Updating from intel-corei7-64-lmp-93 to intel-corei7-64-lmp-100",
                "selected" : true,
                "version" : 100
        }
    ]


In this scenario, the ``intel-corei7-64-lmp-93`` Target is running.
Its entry is marked with ``"current" : true``.
The exit code for the command would be ``16 - Update is required: new target version available``,
as target ``intel-corei7-64-lmp-100`` is available.
If we look into the target ``intel-corei7-64-lmp-100`` entry, we can notice that is has ``"selected" : true``,
meaning this is the target that would be selected by default by ``aktualizr-lite`` to be installed.
A ``selected`` target always has has a ``reason`` field set as well,
which describes why this target is supposed to be installed.
All targets with ``version`` higher than the current one
are marked as ``"newer": true``.

One additional information that the JSON output presents is if the Target is a failing Target.
I.e., if the installation of this Target was attempted, but led to a rollback.
This is the case of Target ``intel-corei7-64-lmp-99``,
with  ``"failed" : true``.
A custom script could, for example, retry the installation of a failed Target,
according to arbitrary criteria.

When customizing the selection of which target has to be installed,
the Target name, or its version, needs to be passed as a parameter.
For example, in order to attempt to install Target ``intel-corei7-64-lmp-99``,
``aktualizr-lite update intel-corei7-64-lmp-99`` or ``aktualizr-lite update 99`` would be used.

Alternatively, to have the download and install operations be performed as separate steps,
``aktualizr-lite pull 99`` followed by ``aktualizr-lite install 99``
could also be used.