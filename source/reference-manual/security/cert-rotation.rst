.. _ref-cert-rotation:

Device Certificate Rotation
===========================

Factory devices communicate with the :ref:`device gateway <ref-device-gateway>` via mutual TLS where both the device and server establish trust with each other.
A device receives an x509 client certificate during device registration that is valid for 20 years.
This validity period is common in IoT, but security bodies like NIST_ recommend changing such keys on a yearly basis.
Certificate rotation is the process you can use to do this.

The FoundriesFactory® process for rotating device certificates is based on the industry standard `RFC 7030`_ Enrollment over Secure Transport (EST).

.. _NIST:
   https://www.nist.gov/
.. _RFC 7030:
   https://www.rfc-editor.org/rfc/rfc7030.html

How It Works
------------

The certificate rotation process is handled by :ref:`ref-fioconfig` on devices.
Fioconfig carefully executes a sequence of atomic operations that can withstand unexpected power failures and reboots.
When triggered a device will:

 * Obtain a new keypair (private key and client certificate) from its configured EST server

 * Inform the device gateway of this new key in order to:

   * Provide some 2FA guarantees—device must prove possession of both keys

   * Let the backend know that configuration operations should be rejected until the new key is in use

 * Re-encrypts its configuration values

 * Reconfigures aktualizr-lite and fioconfig to use the new keypair

 * Restarts fioconfig and aktualizr-lite

 * The device-gateway will see this new certificate then check that it matches the certificate from step 2.
 Finally it adds the old certificate into a deny-list.

The certificate renewal logic uses the EST 7030 `simple re-enrollment`_ process to obtain a new certificate. The process is roughly:

 * Device generates a new private key and certificate signing request copying the Subject of its current certificate.

 * Device sends Certificate Signing Request (CSR) to EST server authenticating to it with its current certificate

 * EST Server verifies request, creates a new certificate, and returns it to the device

 * The new certificate is valid for `one year`_

.. _simple re-enrollment:
   https://www.rfc-editor.org/rfc/rfc7030.html#section-4.2.2

.. _one year:
   https://github.com/foundriesio/estserver/blob/1b32b40729c60e8dfa21155dd1d31135244e56c1/service.go#L210

Tracking Progress
-----------------

Fioconfig will emit update events during a certificate rotation so that operators can observe the progress of the rotation.
For example::

  $ fioctl devices updates <device>
  ID                    TIME                  VERSION  TARGET
  --                    ----                  -------  ------
  certs-1669676316      2022-11-28T23:03:51Z  290      intel-corei7-64-lmp-290

Update ID's prefixed with "cert-" are rotations.
Details can be viewed with::

  $ fioctl devices updates <device> certs-1669674502
  2022-11-28T22:29:49+00:00 : CertRotationStarted(intel-corei7-64-lmp-290) -> Succeed
  2022-11-28T22:29:50+00:00 : Generate new certificate(intel-corei7-64-lmp-290) -> Succeed
  2022-11-28T22:29:50+00:00 : Lock device configuration on server(intel-corei7-64-lmp-290) -> Succeed
  2022-11-28T22:29:50+00:00 : Update local configuration with new key(intel-corei7-64-lmp-290) -> Succeed
  2022-11-28T22:29:51+00:00 : Update device specific configuration on server with new key(intel-corei7-64-lmp-290) -> Succeed
  2022-11-28T22:29:51+00:00 : Finalize aktualizr configuration(intel-corei7-64-lmp-290) -> Succeed

In addition to update events, when a new key is in place a ``DEVICE_PUBKEY_CHANGE`` event will be sent to the factory's :ref:`ref-event-queues`.
This message plus the ``DEVICE_CONFIG_APPLIED`` should help you understand when rotations happen.

Configuring a Server
--------------------

Before you can perform certificate rotations, you must ensure you have taken control of your factory's :ref:`PKI <ref-device-gateway>`.
Specifically, you'll need access to your ``factory_ca.key`` in order to complete these steps.
There are options to choose from.

Foundries Managed
~~~~~~~~~~~~~~~~~

Running ``fioctl keys est authorize`` will allow FoundriesFactory to run an EST server for you at ``<repoid>.est.foundries.io``.
This command will sign a CSR created in the backend with your Factory's root key.
The resulting TLS certificate will be used by the FoundriesFactory EST server.

.. note::
   This option requires the FoundriesFactory backend to have a certificate authority to sign renewal requests.
   This "online-ca" is configured when running ``fioctl keys ca create``.

User Managed
~~~~~~~~~~~~

Users may also run their own EST server.
The EST server used by the Foundries.io backend is available at:

  https://github.com/foundriesio/estserver

The GitHub project includes the details for getting this server up and running.

Performing a Certificate Rotation
---------------------------------

Certificate rotations are triggered via configuration changes.
Fioctl includes a helper for doing this either per device or per device group with:

 * ``fioctl device config rotate-certs <device>``
 * ``fioctl config rotate-certs --group <group>``

In both cases fioctl defines a file and change handler such as::

  fio-rotate-certs - [/usr/share/fioconfig/handlers/renew-client-cert]
     | ESTSERVER=https://4a53f331-6f01-4694-8a97-af253d4d9b63.est.foundries.io:8443/.well-known/est
     | PKEYIDS=01,07
     | CERTIDS=03,09
     | ROTATIONID=certs-1669058841

Certificate rotation will be executed when ``fioconfig`` processes this new file.
If you are using a Factory managed EST server, the command works out of the box.
However, user managed EST servers will require running ``rotate-certs`` with the ``--server-name`` option to inform devices where the EST server is located.

Parameters
~~~~~~~~~~

The ``renew-client-cert`` handler requires a few parameters:

 * **ESTSERVER**: The base URL to your EST resources.
 * **ROTATIONID**: This unique ID will be used as the correlation ID when the device sends update events to the device-gateway.
 * **PKEYIDS** - Devices configured to use HSMs need to know a list of slot IDs to choose from when generating the next private key. 2 IDs are required so it can swap back and forth.
 * **CERTIDS**: Devices configured to use HSMs need to know a list of slot IDs to choose from when storing the new client certificate. 2 IDs are required so it can swap back and forth.
