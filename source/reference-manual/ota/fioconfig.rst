.. _ref-fioconfig:

Fioconfig
=========

Configuration Storage
~~~~~~~~~~~~~~~~~~~~~

Configuration data is assumed to be sensitive unless ``unencrypted`` is explicitly set to true in a configuration JSON payload.
Fleet-wide configuration is uploaded to the server unencrypted, then encrypted with a secret symmetric key at back-end.
Note: even in unencrypted form the configuration is still protected by the TLS encryption at both upload and fetch time.
When a device requests this information, the server will decrypt it and deliver it over its TLS encrypted connection.

Device configuration has a better approach.
The contents of each config file gets encrypted with the device's public key, using the `Elliptical Curve Integrated Encryption Scheme`_ by Fioctl.
This means only someone owning the device's private key, and the device itself, can decrypt the value;
Foundries.io, without the symmetric key, can not.

Your Factory tracks the last 10 config changes made to both the fleet, and each device.
Your Factory keeps track of the last 10 config changes made to each device or device group config.

.. important::
   The maximum size of a total "config" (files and data combined) is 1Mb.

A device stores its config persistently under ``/var/sota/config.encrypted``.
Device specific config options get encrypted.
At boot, each file in the config is extracted into ``/var/run/secrets/<filename>``.
This is tmpfs, only available when the device is running.

Implementation
~~~~~~~~~~~~~~

Configuration is managed by Fioctl, which communicates via the Foundries.io `REST API`_.

LmP devices run a configuration daemon, `fioconfig`_.
This daemon checks in with the server every 5 minutes.
The HTTP request includes a timestamp of its current configuration.
The server will send back one of two responses:

 * **304** — This means nothing has changed since the last request.
   There will be an empty response body.

 * **200** — Something has changed since the last request.
   The response body will be the updated configuration.

 * **204** — No config for a given device.

Fioconfig’s logic for a configuration change is:

 * Save "encrypted" file to `/var/sota` (fleet-wide and "unencrypted" values are not encrypted).

 * For each file in the new configuration:

   * Decrypt if needed

   * If different from ``/var/run/secrets/<file>``, then:

     * Write a new file
     * Call the on-changed handler (if provided).

Since ``/var/run/secrets`` is lost between boots, a systemd oneshot job is invoked during the boot process, to extract the "encrypted" persistent configuration.
It will call "onchanged" handlers.

Diagram
~~~~~~~
             
::

                fioctl
                  +
                  |
                  |
         +--------v---------+
         |                  |
         | api.foundries.io |
         |                  |
         +-^------------^---+
           |            |
           |            |
           |            |
           |            |
 +---------+----+    +--+-----------+
 |              |    |              |
 | LmP Device   |    | LmP Device   |    . . .
 |              |    |              |
 +--------------+    +--------------+


.. _Elliptical Curve Integrated Encryption Scheme:
   https://en.wikipedia.org/wiki/Integrated_Encryption_Scheme

.. _fioconfig:
   https://github.com/foundriesio/fioconfig

.. _REST API:
   https://api.foundries.io/ota
