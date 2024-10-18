.. _ref-device-gateway:

Managing Factory PKI
====================

LmP devices connect to OTA services via a :ref:`Device Gateway <ref-ota-architecture>` configured with :term:`mutual TLS <mTLS>`.
A set of digital certificates used to establish trust between Factory devices and the Device Gateway is a Factory Public Key Infrastructure (PKI).

When a new Factory is created, it is configured to use the default shared :term:`PKI` with certificates owned by Foundries.io™.
This provides a faster engagement with the FoundriesFactory™ Platform, allowing streamlined product development.

FoundriesFactory supports setting up your own Factory PKI via either :ref:`Fioctl® <ref-fioctl>` commands or the API integration.
We recommend setting up your own Factory PKI **before** going to production.
Benefits of owning your Factory PKI are two-fold:

- Controlling which devices can connect to your Factory Device Gateway to fetch configuration and software updates.
- Controlling which servers can deliver configuration and software updates to your Factory devices.

.. warning::
   The Factory :ref:`Root of Trust <Root-of-Trust>` **can only be set once**; subsequent attempts will fail.
   Other Factory PKI certificates can be updated at any time; provided that you own your Factory Root of Trust.

   `Contact customer support <https://support.foundries.io>`_ if you need your Factory PKI being reset.
   Once a reset was performed, all connected devices will lose their connection.
   These devices will not be able to connect to the Device Gateway until they are re-provisioned with a new Root of Trust.
   In practice this means that these devices need to be re-flashed (after the Factory PKI reset).

Terminology
-----------

.. _Root-of-trust:

Root of Trust: ``factory_ca.key / factory_ca.pem`` 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An X.509 certificate used as a Root Certificate Authority (RCA) for your Factory.
You own the private key (NIST P-256 by default), and share the corresponding certificate with Foundries.io.

All intermediate Certificate Authorities (CAs) and TLS certificates configured in your Factory must be signed by its Root of Trust.
The Root of Trust is preloaded to Factory devices so that they can use it to verify the FoundriesFactory web APIs TLS certificates.

.. warning::
    Never lose the private key of your Factory Root of Trust.
    By design, Foundries.io only stores a copy of the CA certificate bearing its public key.
    We are not able to recover your private key in case of its loss.

    We recommend storing your Factory Root of Trust in a cloud-based HSM solution of your choice.
    For example, we verified that the `AWS Cloud HSM <https://aws.amazon.com/cloudhsm/>`_ supports `importing EC private keys`_.
    That way you get increased safety of your highly important secret through their redundancy and backup policies.

    Additionally, we recommend printing the private key of your Root of Trust on paper and storing it in multiple fire and waterproof safes.

.. _importing EC private keys: https://docs.aws.amazon.com/cloudhsm/latest/userguide/key_mgmt_util-importPrivateKey.html

.. _tls-crt:

Server TLS Certificate: ``tls-crt``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An X.509 certificate used by :ref:`Device Gateway <ref-ota-architecture>` during a mutual TLS handshake and session setup.
Foundries.io owns the private key (NIST P-256 by default), and you sign the certificate by the Factory Root of Trust.

When your Factory devices connect to the Device Gateway, they verify the server identity by validating its TLS Certificate.
They use the preloaded Factory Root of Trust to perform that validation.
Once the mutual trust is established, Device Gateway uses its TLS Certificate to setup a session symmetric key.
That temporary symmetric key is used to encrypt all session traffic between the Device Gateway and the device.

Device Client Certificate
~~~~~~~~~~~~~~~~~~~~~~~~~

An X.509 certificate that is issued to your Factory device during the registration process.
The device owns the private key (NIST P-256 by default) and the certificate.

This certificate must be signed by either a :ref:`Local Device CA <local-ca>` or an :ref:`Online Device CA <online-ca>` (see below).
For example, when using the `lmp-device-register`_ to register your device, it generates the Device Client Certificate Signing Request (CSR).
The CSR is then signed by an appropriate Device CA at the registration server (either your own or Foundries.io), and stored on the device.

When connecting to the :ref:`Device Gateway <ref-ota-architecture>`, a device must present its Client Certificate during a TLS handshake.
The device identity is verified at the Device Gateway, and the device is either allowed or denied to connect based on its certificate validity.
Once mutual trust is established, device uses its Client Certificate to setup a session symmetric key.

.. _lmp-device-register: https://github.com/foundriesio/lmp-device-register/

.. _online-ca:

Online Device CA: ``online-ca``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An X.509 certificate used as a :term:`CA` for issuing certificates to devices registered via the FoundriesFactory API.
Foundries.io owns the private key (NIST P-256 by default), and you sign the certificate using the Factory Root of Trust.

When using the "shared" Factory PKI, this is the only CA used to issue Client Certificates to your Factory devices.
Once you take ownership of your Factory PKI, you may opt out of using the Online Device CA.

.. _local-ca:

Local Device CA: ``local-ca``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An X.509 certificate used as a :term:`CA`, issuing certificates to devices registered via your offline registration process.
You own the private key (NIST P-256 by default), and share the corresponding certificate with Foundries.io.
It must be signed by the Root of Trust, so that Foundries.io may verify if a user is entitled to upload a Device CA.

At creation, your Factory only has an Online Device CA and no Local Device CAs.
Your Factory may be configured to have one or more Local Device CAs only after you take ownership of your Factory PKI.
You may use the Local Device CA with our :ref:`ref-factory-registration-ref` to register your devices offline.

  .. figure:: /_static/ca_certs.png
     :align: center
     :scale: 90 %
     :alt: PKI hierarchy

.. _est-tls-crt:

EST Server TLS Certificate: ``est-tls-crt``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An X.509 certificate used by FoundriesFactory hosted :ref:`ref-cert-rotation` during a mutual TLS handshake and session setup.
Foundries.io owns the private key (NIST P-256 by default), and you sign the certificate using the Factory Root of Trust.

The FoundriesFactory process for rotating device certificates is based on the industry standard `RFC 7030`_ Enrollment over Secure Transport (EST).
Your Factory may be configured to use a FoundriesFactory hosted EST service, your own EST service, or no EST service.

.. _RFC 7030: https://datatracker.ietf.org/doc/html/rfc7030

.. _ref-rm-pki:

Managing Your Factory PKI
-------------------------

Setting Up Your PKI
~~~~~~~~~~~~~~~~~~~

:ref:`ref-fioctl` includes a command to set up your PKI:

.. warning::
   The following command can only be used once.

.. code-block::

    fioctl keys ca create /absolute/path/to/certs/

A few important things to note about this command:

 * Use a PKCS#11 compatible HSM.
   This will ensure the safety of your Factory's Root of Trust private key.

 * The "PKI Directory" is important, and should be securely backed up.

 * As noted in the warning, it can only be set once.
   A reset requires contacting `Customer Support <https://support.foundries.io>`_,
   and will result in connected devices loosing connection.

After running the above command, you can validate the outcome and view the configured certificates by using the following command:

.. code-block::

    fioctl keys ca show --pretty

Rotating Server TLS Certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes, you might need to rotate the TLS certificate used by the Device Gateway to serve your Factory devices.
For example, the corresponding TLS certificate might be close to its expiration date, or it might be compromised.
Foundries.io is not able to perform that task for you, as it requires access to your Factory Root of Trust.

:ref:`ref-fioctl` includes a command to rotate your Server TLS Certificate:

.. code-block::

    fioctl keys ca rotate-tls /absolute/path/to/certs/

Adding Device CA
~~~~~~~~~~~~~~~~

Sometimes, you might need to add more than one Device CA to your Factory.
Some use cases when this is needed include (but are not limited to) the following situations:

 * You have only initially set up an Online Device CA for your Factory,
   and want to also configure a Local Device CA (or vice versa).

 * You opened a new manufacturing site,
   and want a dedicated Local Device CA to issue Client Certificates to devices manufactured at this site.

 * One of your Device CAs was compromised,
   and you need to replace it by a new Device CA (either Online or Local).

:ref:`ref-fioctl` includes a command to add one more Device CA to your Factory:

.. code-block::

    fioctl keys ca add-device-ca /absolute/path/to/certs/ [--online-ca | --local-ca]

Revoking Device CA
~~~~~~~~~~~~~~~~~~

You may need to revoke or disable a Device CA for your Factory.
Some use cases when this is needed include the following situations:

 * One of your Device CAs was compromised,
   and you need to deny an ability to register new devices with client certificates issued by this CA.
   You may also want to completely deny access to the Device Gateway for already registered devices with such certificates.

 * You are closing a manufacturing site,
   and want to make sure that a Device CA issued for that manufacturing site can no longer be used to issue new client certificates.

:ref:`ref-fioctl` provides two separate commands: to disable and revoke an existing Device CA.

There is an important difference between disabling and revoking a Device CA:

- When you disable the Device CA,
  new devices with client certificates issued by that CA cannot be registered.
- When you revoke the Device CA, in addition to the above,
  already registered devices with client certificates issued by that CA cannot connect to your Factory.

Use the below command when you need to disable a Device CA:

.. code-block::

    fioctl keys ca disable-device-ca /absolute/path/to/certs/ [--ca-file <filename> | --ca-serial <serial>]

Use the following command when you need to revoke a Device CA:

.. code-block::

    fioctl keys ca revoke-device-ca /absolute/path/to/certs/ [--ca-file <filename> | --ca-serial <serial>]

After the Device CA is revoked, devices can no longer update their apps or config.
Therefore, the revocation process needs to be planned properly.
We recommend the following workflow:

1. Disable the Device CA.
   This action needs to be taken as soon as you notice that your Device CA was compromised.
   This makes sure that an attacker is not able to register new devices with client certificates issued by that CA.

2. Inspect your fleet of already registered devices, and delete those devices which you think are not legitimate.
   After this point, you can be sure that an attacker can no longer steal your new Intellectual Property (provided by OTA updates).
   FoundriesFactory advises you to also prepare a separate plan for how to deal with already compromised devices.

3. Rotate client certificates on your devices which have a client certificate issued by a Device CA you are revoking.
   You may use Foundries.io hosted :ref:`ref-cert-rotation` service, or use your own certificate rotation workflow.
   Make sure that new device client certificates are issued by one of the Device CAs enabled for your Factory.

4. Revoke the Device CA.
   At this point a reference to a given Device CA is completely removed from our servers, hence becomes untrusted.

Related Topics
--------------

The Factory PKI is interwoven with the device manufacturing process and device registration.
You can find out more details on this topic in this guide :ref:`ref-factory-registration-ref`.

More details on Factory PKI internals can be found in this :ref:`guide <ref-device-gateway-pki-details>`.
