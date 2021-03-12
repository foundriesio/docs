.. _ref-device-gateway:

Managing Your Device Gateway
============================

LMP devices connect to OTA services via a
:ref:`device gateway <ref-ota-architecture>` configured with
mutual TLS. Each factory uses a default device gateway with
certificates owned by Foundries.io. We allow and **encourage**
you to set up your own PKI infrastructure so that you are in control
of the security of the device gateway.

Terminology
-----------

Root of trust - factory_ca.key / factory_ca.pem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The PKI root of trust for your factory. You own the
EC prime256v1 private key. The corresponding x509 certificate is shared
with Foundries.io to define your root of trust.

All mutual TLS certificates configured in your factory  must be signed
by this keypair.

Server TLS Certificate - tls-crt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The server TLS certificate keypair is used by the server to encrypt
TLS communication with devices. The private key is owned by
Foundries.io and the certificate is signed by the root of trust.

"online-ca"
~~~~~~~~~~~

In order for lmp-device-register to work, Foundries.io needs the
ability to sign client certificates for devices. If enabled, the
root of trust will sign a certificate that Foundries.io can use
to sign client authentication certificates.

"local-ca"
~~~~~~~~~~
Optional keypair(s) that can be used by something like your
manufacturing process sign client certificates for devices without
needing access to Foundries.io.

  .. figure:: /_static/ca_certs.png
     :align: center
     :scale: 90 %
     :alt: PKI hierarchy

Setting up your PKI
-------------------

:ref:`ref-fioctl` includes a sub-command to set this up:
``fioctl keys ca create``. There are a couple of important things to
note about this command:

 * It's highly recommend that you use a PKCS#11 compatible HSM. This
   will ensure the safety of your factory's root of trust private key.

 * The "PKI Directory" is important and should be securely backed
   up.

You can view the configured certificates with
``fioctl keys ca show --pretty``.
