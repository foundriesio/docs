Configuring Devices
===================

Device configuration can be managed with the `fioctl command line tool`_.
There are two types of configuration supported:

  #. Fleet-wide - Configuration set here gets sent to all devices in a Factory.
  #. Device specific - This overrides fleet-wide configuration in the
     event they collide.

Fleet Wide Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

Configuration common to all factory devices can be done with ``fioctl config``
subcommands::

  # View log of config changes (similar to "git log")
  fioctl config log

  # Add a config file to the entire fleet
  fioctl config set --reason "for docs" AWS_REGION="us-east-2"

Device Specific Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Device configuration is managed with the ``fioctl devices config``
subcommands::

  # View log of config changes made to device
  fioctl devices config log <device name>

  # Add a config file to device
  fioctl devices config set <device name> --reason "for docs" \
    githubapitoken="really secure value"

"Raw" Configuration
~~~~~~~~~~~~~~~~~~~
The ``config set`` commands only expose part of what is possible with
configuration. Advanced use cases require the ``--raw`` option. Two
interesting things that can be done with this include "on-changed" and
"unencrypted"::

  cat >tmp.json <<EOF
  {
    "reason": "for docs",
    "files": [
      {
        "name": "npmtok",
        "value": "root (this will get encrypted by tooling)",
        "on-changed": ["/usr/bin/touch", "/tmp/npmtok-changed"]
      },
      {
        "name": "A-Readable-Value",
        "value": "This won't be encrypted and will be visible from the API",
        "unencrypted": true
      }
    ]
  }
  EOF

Further Reading
~~~~~~~~~~~~~~~

More details can be found in :ref:`ref-fioconfig`.

.. _fioctl command line tool:
   https://github.com/foundriesio/fioctl/releases
