.. _ref-cert-rotation:

Device Certificate Rotation
===========================

Factory devices communicate with the :ref:`device gateway <ref-device-gateway>` via mutual TLS where both the device and server establish trust with each other.
A device receives an x509 client certificate during device registration that is valid for 20 years.
This validity period is common in IoT, but security bodies like NIST_ recommend changing such keys on a yearly basis.
Certificate rotation is the process you can use to do this.

The FoundriesFactory™ Platform's process for rotating device certificates is based on the industry standard `RFC 7030`_ Enrollment over Secure Transport (EST).

.. _NIST:
   https://www.nist.gov/
.. _RFC 7030:
   https://www.rfc-editor.org/rfc/rfc7030.html

How It Works
------------

The certificate rotation process is handled by :ref:`ref-fioconfig` on devices.
Fioconfig carefully executes a sequence of atomic operations that can withstand unexpected power failures and reboots.
When triggered a device will:

 #. Obtain a new keypair (private key and client certificate) from its configured EST server

 #. Inform the device gateway of this new key in order to:

    * Provide some 2FA guarantees—device must prove possession of both keys

    * Let the backend know that configuration operations should be rejected until the new key is in use

 #. Re-encrypts its configuration values

 #. Reconfigures aktualizr-lite and fioconfig to use the new keypair

 #. Restarts fioconfig and aktualizr-lite

 #. The device-gateway will see this new certificate then check that it matches the certificate from step 2.
 #. Finally it adds the old certificate into a deny-list.

The certificate renewal logic uses the EST 7030 `simple re-enrollment`_ process to obtain a new certificate. The process is roughly:

 * Device generates a new private key and certificate signing request copying the Subject of its current certificate.

 * Device sends Certificate Signing Request (CSR) to EST server authenticating to it with its current certificate

 * EST Server verifies request, creates a new certificate, and returns it to the device

 * The new certificate is valid for one year.

.. _simple re-enrollment:
   https://www.rfc-editor.org/rfc/rfc7030.html#section-4.2.2

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

In addition to update events, when a new key is in place a ``DEVICE_PUBKEY_CHANGE`` event will be sent to the Factory's :ref:`ref-event-queues`.
This message, plus ``DEVICE_CONFIG_APPLIED``, should help you understand when rotations happen.

Next Steps
----------

:ref:`Device Certificate Rotation <ref-cert-rotation-ug>` explains how to enable this in your Factory.
