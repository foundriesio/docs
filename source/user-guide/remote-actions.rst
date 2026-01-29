.. _ref-remote-actions:

Remote Actions
==============

Remote actions allow you to execute pre-configured scripts on a device and view the results.
Default LmP builds include:

 * ``diag`` - Run the fio-diag.sh_ script.
   This also collects ``dmesg`` output as an artifact.
 * ``reboot`` - Instruct the system to reboot.

.. note::
   This feature was added to LmP version **v97**. Prior versions do not support this.

.. _fio-diag.sh:
   https://github.com/foundriesio/meta-lmp/blob/main/meta-lmp-base/recipes-support/fio-diag/fio-diag_0.1.bb

Basic Usage
-----------

Listing Available Actions
~~~~~~~~~~~~~~~~~~~~~~~~~

You can see if a device supports remote actions and which ones are available using the Fioctl® CLI tool::

  fioctl devices triggers list-configured <device>

Triggering an Action
~~~~~~~~~~~~~~~~~~~~

You can schedule an action to be run with::

  fioctl devices triggers run <device> <action>

For example:

.. code-block:: console

    # Run the "diag" action on "my-device".
    $ fioctl devices triggers run my-device diag
    Config change submitted. Command ID is: diag_TS4AAYDMOGTMN7U
    # Use 'fioctl devices tests my-device diag_TS4AAYDMOGTMN7U' to check results.

Viewing Results
~~~~~~~~~~~~~~~

Remote actions are sent to the device using :ref:`ref-fioconfig`.
This means that the action will be run and reported asynchronously. By default, Fioconfig will check in with the server every 5 minutes.
The results of the action will be available from the ``fioctl devices tests`` command.
For example:

.. code-block:: console

    $ fioctl devices tests my-device
    NAME       STATUS  ID                                    CREATED AT
    ----       ------  --                                    ----------
    diag       PASSED  diag_8u_42JiMRZ9VAhR                  2025-12-12 23:13:04 +0000 UTC
    reboot     PASSED  reboot_fZA31Esg2tGRxRY                2025-12-12 23:30:08 +0000 UTC

Details of a specific item can be viewed with:

.. code-block:: console

    $ fioctl devices tests my-device diag_8u_42JiMRZ9VAhR
    Name:      diag
    Status:    PASSED
    Created:   2025-12-12 23:13:04 +0000 UTC
    Completed: 2025-12-12 23:13:04 +0000 UTC
    Details:
    /usr/share/fioconfig/actions/diag
    Artifacts:
           dmesg.log
           console.log

Artifacts can be viewed with:

.. code-block:: console

    $ fioctl devices tests qc-t14-qemu diag_8u_42JiMRZ9VAhR console.log
    + /usr/sbin/fio-diag.sh
    *** diag tool version ***
    Version: 1.0

    *** os-release ***
    ID=lmp
    NAME="Linux-microPlatform"
    ...

How It Works
------------

The remote actions feature is implemented with :term:`Fioconfig`.
When Fioconfig starts up, it will look under ``/usr/share/fioconfig/actions`` to find actions it can perform.
This list will be uploaded to the server if/when it changes.
You can see this with:

.. code-block:: console

    $ fioctl devices config log -n1 my-device
    Created At:    2026-01-29T15:20:08+00:00
    Created By:    59db9c9a1c85010019e023cc / Andy Doan
    Applied At:
    Change Reason:
    Files:
	  fio-remote-actions
	   | diag
	   | reboot
    ...

This file lets Fioctl know what actions it can trigger.
Triggering an action creates a Fioconfig file with a change-handler, fioconfig-oneshot_.
This handler has logic to make sure a remote action is triggered and run one time per request.
The content of the file used by the handler includes:

 * ``COMMAND_ID`` - This tells Fioconfig what "test ID" to upload results to.
   It also is used by ``fioconfig devices tests`` when looking up results.
 * ``COMMAND_CAPTURE`` - Tells Fioconfig to capture and report the output of the action.

.. _fioconfig-oneshot:
   https://github.com/foundriesio/fioconfig/blob/main/contrib/fioconfig-oneshot

Implementing an Action
----------------------

An action is simply an executable file found under ``/usr/share/fioconfig/actions``.
The standard output and error will be included in the `console.log`` artifact for its results.
You can also attach additional artifacts by placing them under the directory pointed to by the ``${ARTIFACTS}`` environment variable.

Looking into the Fioconfig actions_ is also a good way to learn.

Actions can be added/removed from your image by extending the Fioconfig recipe_.

.. _actions:
  https://github.com/foundriesio/fioconfig/tree/main/contrib/actions
.. _recipe:
   https://github.com/foundriesio/meta-lmp/tree/main/meta-lmp-base/recipes-support/fioconfig
