.. _ref-device-gateway:

Managing Factory PKI
====================

LmP devices connect to OTA services via a :ref:`device gateway <ref-ota-architecture>` configured with mutual TLS.
Each Factory uses a default device gateway with certificates owned by Foundries.io™.
We allow—and **encourage**\—you to set up your own PKI infrastructure.
This is so that you are in control of the security of the device gateway.

Terminology
-----------

.. _Root-of-trust:

Root of Trust: ``factory_ca.key / factory_ca.pem`` 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The PKI root of trust for your Factory.
You own the private key (NIST P-256 by default).
The corresponding x509 certificate is shared with Foundries.io to define your root of trust.

All intermediate CA and mutual TLS certificates configured in your Factory must be signed by this keypair.
In particular, the certificates mentioned below.

.. _tls-crt:

Server TLS Certificate: ``tls-crt``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This certificate along with its private key is used by Device Gateway during mTLS handshake/session setup.
Specifically, they are used for Device Gateway identity verification by a device/client and a TLS session's symmetric key setup.
The private key is owned by Foundries.io and the certificate is signed by the root of trust.

.. _online-ca:

Certificate: ``online-ca``
~~~~~~~~~~~~~~~~~~~~~~~~~~

In order for ``lmp-device-register`` to work, Foundries.io needs the ability to sign client certificates for devices.
If enabled, the root of trust will sign an ``online-ca`` certificate that Foundries.io can use to sign client authentication certificates.

.. _local-ca:

Certificate: ``local-ca``
~~~~~~~~~~~~~~~~~~~~~~~~~

Optional pair(s) of a private key and intermediate CA certificate, signed by the root CA. 
Can be used by something like your manufacturing process to sign client certificates for devices—without needing access to Foundries.io.

It is also known and referred to as ``offline CA``, since you own its private key and keep it "offline".

  .. figure:: /_static/ca_certs.png
     :align: center
     :scale: 90 %
     :alt: PKI hierarchy

.. _ref-rm-pki:

Setting Up Your PKI
-------------------

:ref:`ref-fioctl` includes a sub-command to set up your PKI:

.. warning::
   The following command can only be used once.

.. code-block::

    fioctl keys ca create /absolute/path/to/certs/

A few important things to note about this command:

 * Use a PKCS#11 compatible HSM.
   This will ensure the safety of your Factory's root of trust private key.

 * The "PKI Directory" is important, and should be securely backed up.

 * As noted in the warning, it can only be set once.
   A reset requires contacting `Customer Support <https://foundriesio.atlassian.net/servicedesk/customer/portals>`,
   and will result in connected devices loosing connection.

After running the above command, you can validate the outcome and view the configured certificates by using the following command:

.. code-block::

    fioctl keys ca show --pretty

The Factory PKI is interwoven with the device manufacturing process and device registration.
You can find out more details on this topic in this guide :ref:`ref-factory-registration-ref`.

More details on Factory PKI can be found in this :ref:`guide <ref-device-gateway-pki-details>`.
