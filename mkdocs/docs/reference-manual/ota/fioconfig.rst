.. _ref-fioconfig:

fioconfig
=========

Configuration Storage
~~~~~~~~~~~~~~~~~~~~~

Configuration data is assumed to be sensitive unless the ``unencrypted``
attribute is explicitly set to true in a configuration JSON payload.
Fleet-wide configuration is uploaded to the server and then encrypted with a
secret symmetric encryption key. Later, when a device requests this
information, the server will decrypt it and deliver it to the device over its
TLS encrypted connection. Device configuration has a much better approach.
The contents of each configuration file will be encrypted with the device's
public key using the `Elliptical Curve Integrated Encryption Scheme`_ by
fioctl. This means only the user of fioctl and the device will be able to
decrypt the value. foundries.io can't.

The Factory will keep track of the last 10 config changes made to the
fleet and each device so that some basic change history can be tracked.
Additionally, the maximum size of a "config" (files and data) is 1Mb.

The device stores configuration persistently under
``/var/sota/config.encrypted``. Device specific configuration options will
be encrypted. At boot, each file in the configuration is extracted into
``/var/run/secrets/<filename>``. This is tmpfs and is only available when the
the device is running.

Implementation
~~~~~~~~~~~~~~

Configuration is managed by fioctl which communicates via the
Foundries.io `REST API`_.

LmP devices run a configuration daemon, `fioconfig`_. This daemon checks in
with the server every 5 minutes. The HTTP request includes a timestamp of its
current configuration. The server will send back one of two responses:

 * **304** - This means nothing has changed since the last request. There will
   be an empty response body.

 * **200** - Something has changed since the last request. The response body will
   be the updated configuration.

Fioconfig’s logic for a configuration change is:

 * Save "encrypted" file to /var/sota (fleet-wide and "unencrypted" values
   aren't encrypted).

 * For each file in the new configuration:

   * Decrypt if needed

   * If different from ``/var/run/secrets/<file>``

     * Write new file
     * Call the the on-changed handler (if provided)

Since ``/var/run/secrets`` is lost between boots, a systemd oneshot job is
invoked during the boot process to extract the "encrypted" persistent
configuration. It will call "onchanged" handlers.

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
