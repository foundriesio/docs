.. _ref-configuring-devices:

Configuring Devices
===================

Device configuration can be managed with :ref:`ug-fioctl`.
There are three types of configuration supported:

  #. Fleet-wide — Configuration gets sent to all devices in a Factory.
  #. Device group specific — Configuration gets sent to all devices in a device group.
  #. Device specific — This overrides fleet-wide and device group configuration in the event they collide.

.. tip::
   Configuration files set in this section can be found in ``/var/run/secrets`` after delivered to the device.

Fleet-Wide Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

Configuration common to all Factory devices can be set with ``fioctl config`` subcommands::

  # View log of config changes (similar to "git log")
  fioctl config log

  # Add a config file to the entire fleet
  fioctl config set --reason "for docs" AWS_REGION="us-east-2"

The configuration reason specified via ``--reason`` is visible in the output of ``fioctl config log``::

  Created At:    2021-03-06T00:46:02
  Applied At:    2021-03-06T00:49:24
  Change Reason: for docs
  Files:
          z-50-fioctl.toml - [/usr/share/fioconfig/handlers/aktualizr-toml-update]
  ...

Device Group Specific Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Similar to fleet-wide configurations, device group specific configuration is managed with the ``fioctl config`` subcommands using the ``--group`` parameter::

  # View log of config changes made to the device group
  fioctl config log --group <group-name>

  # Add a config file to the device group
  fioctl config set --group <group-name> --reason "for docs" secret="doc-secret"

Device Specific Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Device configuration is managed with the ``fioctl devices config`` subcommands::

  # View log of config changes made to device
  fioctl devices config log <device-name>

  # Add a config file to device
  fioctl devices config set <device-name> --reason "for docs" \
    githubapitoken="really secure value"

"Raw" Configuration
~~~~~~~~~~~~~~~~~~~

The ``config set`` commands only expose part of what is possible with
configuration. Advanced use cases require the ``--raw`` option.

Two interesting things that can be done with this include ``on-changed`` and ``unencrypted``::

  cat >tmp.json <<EOF
  {
    "reason": "for docs",
    "files": [
      {
        "name": "newconfig",
        "value": "root (this will get encrypted by tooling)",
        "on-changed": ["/usr/share/fioconfig/handlers/<new-script>"]
      },
      {
        "name": "A-Readable-Value",
        "value": "This won't be encrypted and will be visible from the API",
        "unencrypted": true
      }
    ]
  }
  EOF

The ``on-changed`` parameter allows to run commands upon receiving configuration fragments.
The `fioconfig` may only run "trusted" scripts from the ``/usr/share/fioconfig/handlers/`` folder to protect devices from arbitrary script execution.
As such, a custom handler should be created in this folder.
See `fioconfig_git.bb <https://github.com/foundriesio/meta-lmp/blob/main/meta-lmp-base/recipes-support/fioconfig/fioconfig_git.bb>`_ for reference.

.. tip::
  For testing purposes, it is possible to use the ``on-changed`` parameter to run commands outside of the ``/usr/share/fioconfig/handlers`` folder.
  This is done by running ``fioconfig --unsafe-handlers daemon``.
  We do not recommend doing that in production.
  This allows running configurations as::

      cat >tmp.json <<EOF
      {
        "reason": "for docs",
        "files": [
          {
            "name": "npmtok",
            "value": "secret-token",
            "on-changed": ["/usr/bin/touch", "/tmp/npmtok-changed"]
          }
        ]
      }
      EOF

.. note::

   In case there are configuration conflicts in a device, the priority order is: device specific configuration, which takes precedence over device group specific configuration, which takes precedence over fleet-wide configuration.

   For example:

   * Fleet-wide configuration sets App A
   * Device group specific configuration sets Apps A and B
   * Device specific configuration sets Apps A, B and C

   By default, the device runs the Apps A, B and C. In case the device specific configuration is removed, then the device will run the device group configuration, with Apps A and B. If this device specific configuration gets deleted, the configuration will fall back to the fleet-wide settings, then running App A only.

.. seealso::
   :ref:`ref-fioconfig`
