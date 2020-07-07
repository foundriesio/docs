.. _ref-fioctl:

fioctl
======

fioctl_ is a command line tool to help remotely manage 
a FoundriesFactory.

The tool is a reference implementation of the Foundries.io 
"ota-lite" API_.

Download
--------

Download the latest release of fioctl_ to your x86 host system. 

  * fioctl-linux-amd64 - 64bit Linux
  * fioctl-darwin-amd64 - 64bit MacOSX
  * fioctl-windows-amd64.exe - 64bit Windows

Rename the application to ``fioctl`` and move it to an executable ``PATH``

Example on Linux:

``mv fioctl-linux-amd64 /usr/bin/fioctl``

TODO: What about Windows and MacOSX?

Build from Source
-----------------

If you wish to build from source code, please review the README_.

Authenticate
------------

You must first authenticate with the server before using this tool with:

``fioctl login``

Devices
-------

Every device registered to a factory can be managed with fioctl.

List All Devices
~~~~~~~~~~~~~~~~

Show all registered devices for every factory you are a user of.

``fioctl devices list``

List Devices By Factory
~~~~~~~~~~~~~~~~~~~~~~~

Show all registered devices for a specific factory.

Targets
-------

List Targets
~~~~~~~~~~~~

Show all targets for a specific factory.

``fioctl targets list -f <factory>``

TODO: Document how to enable/disable wireguard

TODO: Document how to update apps

TODO: Document how to update tags

TODO: Document how to introspect targets

TODO: Document how to list device config

.. _README:
    https://github.com/foundriesio/fioctl/blob/master/README.md
.. _API:
   https://app.swaggerhub.com/apis/foundriesio/ota-lite/
.. _fioctl:
   https://github.com/foundriesio/fioctl/releases
