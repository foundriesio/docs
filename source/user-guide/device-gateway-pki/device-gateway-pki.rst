.. _ref-device-gateway-pki-details:

Details Of Device Gateway PKI Settings
======================================

.. warning::
   The factory root of trust **can only be set once** —
   `contact customer support <https://support.foundries.io>` if you need to have the value reset.
   This means the command ``fioctl keys ca create`` works only for the first run.
   Subsequent attempts will fail.
   Additionally,if you do have a reset performed, it will result in connected devices losing connection.
   However, the Device CA bundle (``ca-crt``) can be updated many times;
   you may add or remove local/offline CA certs for the bundle with ``fioctl keys ca update``.

This guide covers Public Key Infrastructure (PKI) Settings.
In particular, the low-level details of what happens behind the scenes when running the ``fioctl keys ca`` commands.
It also provides instructions to create, sign, and use an *offline* (aka *local*) device certificate.

The :ref:`Factory PKI <ref-device-gateway>` reference manual describes core concepts of Device Gateway PKI and how it can be configured by using the ``fioctl keys ca``.

.. seealso::
   Documentation on using :ref:`Fioctl® <ug-fioctl>`

Under the Hood
~~~~~~~~~~~~~~

The PKI for Device Gateway and Factory Devices is vital for the secure communication between them.
It is important to understand exactly what the given command does.

Before a user sets up the PKI, their Devices and Device Gateway talk to each other by utilizing a so-called "shared PKI".
This is the default PKI that the FoundriesFactory™ service sets up as part of new Factory provisioning.
The ``fioctl`` command communicates with the end point ``https://api.foundries.io/ota/factories/$FACTORY/certs/`` to create and update Factory specific PKI keys and certificates.
As long as the Factory uses the "shared PKI", the endpoint returns an empty response, as no Factory PKI is set::

    curl -s -H "OSF-TOKEN: $TOKEN" https://api.foundries.io/ota/factories/${FACTORY}/certs/ | jq
    {
      "tls-crt": null,
      "ca-crt": null,
      "root-crt": null
    }

* ``root-crt`` is the PKI root CA certificate, also referred as :ref:`Root of Trust <Root-of-trust>`
* ``ca-crt`` is a certificate bundle containing one :ref:`online CA <online-ca>` certificate and optionally one or more :ref:`local CA <local-ca>` certificates, aka "offline-ca".
* ``tls-crt`` is a Device Gateway certificate, also referred as :ref:`a server TLS certificate <tls-crt>`


The first step that the ``fioctl`` command does is send a post request to the PKI endpoint.
In the following example, a response is redirected to a json file so its content can be used later.::

    curl -s -X POST -H "Content-Type: application/json" -H "OSF-TOKEN: $TOKEN" "https://api.foundries.io/ota/factories/${FACTORY}/certs/" | jq . > factory_certs.json

The endpoint handler does the following:

1. Generates a private key and corresponding Certificate Signing Request (CSR) for Device Gateway (tls-crt);
2. Generates a private key and corresponding CSR for Online Device CA (online-ca);
3. Returns a json formatted response to a caller, the response includes:

   a. ``tls-csr`` - CSR for Device Gateway certificate
   b. ``ca-csr`` - CSR for Online Device CA certificate
   c. ``create_ca`` - a script that can be used for root CA creation, i.e. a private key and corresponding self-signed certificate
   d. ``create_device_ca`` - a script that can be used for "local-ca"/"offline-ca" creation, i.e. a private key, corresponding certificate signed by the root CA
   e. ``sign_tls_csr`` - a script that signs received ``tls-csr`` by the root CA
   f. ``sign_ca_csr`` - a script that signs received ``ca-csr`` ("online-ca") by the root CA.

A user can extract any of the aforementioned fields by utilizing the ``jq`` utility: ::

    cat factory_certs.json | jq -r .create_ca

Once the ``fioctl`` command receives a response, it makes use of the above scripts included in a response.
Specifically, it:

1. Invokes the ``create_ca`` script to generate Root CA key (``factory_ca.key``) and Root CA certificate (``factory_ca.pem``);
2. Signs the ``tls-csr`` by invoking the ``sign_tls_csr`` script, the resultant certificate is stored in ``tls-crt``;
3. Signs the ``ca-csr`` by invoking the ``sign_ca_csr`` script, the resultant certificate is stored in ``online-crt``;
4. Creates a local/offline Device CA by using ``create_device_ca``, the resultant private key and certificate are stored in ``local-ca.key`` and ``local-ca.pem`` correspondingly;

Then the ``fioctl`` command uploads the generated artifacts to the backend by issuing a ``PATCH`` request to the endpoint.
The following files are uploaded:

1. ``tls-crt`` - the result of ``tls-csr`` signing;
2. ``online-crt`` and ``local-ca.pem`` bundled together into the ``ca-crt`` field of the PATCH request;
3. ``factory_ca.pem`` - root CA certificate created by running ``create_ca`` transferred via ``root-crt`` fields of the PATCH request.

Device Key and Certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~
Once the PKI is setup, your Factory Device Gateway is ready to communicate via mTLS with Factory devices.
The devices must have a private key and a x509 certificate to setup mTLS session with Device Gateway.
It also needs the Root CA certificate to verify Device Gateway certificate during mTLS handshake.

As explained above, the ``fioctl`` command generates two types of Device CA, online and local/offline CAs.
Both of these CAs can be used to sign Device CSR.

Online Device Certificate
*************************
In the case of online CA, a private key is owned by the backend. Hence, only the backend can sign a Device CSR with the online CA.
The utility called ``lmp-device-register`` can be used for this purpose, and is the default device registration mechanism.
The tool generates a device private key, creates a corresponding device CSR, and makes a request to the backend to sign it with the online CA.
As a response, the backend returns a signed device certificate as well as a default configuration for the device (aka ``sota.toml``).
More details on ``lmp-device-register`` usage can be found in the :ref:`getting started guide <gs-register>`.

Local/Offline Device Certificate
********************************

We advise using the Factory registration `reference implementation`_ as a mechanism for offline device key and certificate generation as well as device registration.
The following is a guide on the manual creation of Local/Offline Device keys and certificates.
This can be useful for understanding low-level details of the overall process.

Create a directory for offline device key and certificate::

    mkdir -p devices/offline-device

Generate a private key::

    openssl ecparam -genkey -name prime256v1 -out devices/offline-device/pkey.pem

Set offline Device certificate config::

   cat > devices/offline-device/device-cert.conf <<EOF
   [req]
   prompt = no
   days=3650
   distinguished_name = req_dn

   [req_dn]
   # Device ID
   commonName="`uuidgen`"
   organizationalUnitName="${FACTORY}"
   EOF

Make sure to replace ``<device-UUID>`` and ``${FACTORY}`` with your values.

Set offline Device certificate extensions::

   cat > devices/offline-device/device-cert.ext <<EOF
   keyUsage=critical,digitalSignature,keyAgreement
   extendedKeyUsage=critical,clientAuth
   EOF

Generate CSR::

    openssl req -new -config devices/offline-device/device-cert.conf -key devices/offline-device/pkey.pem -out devices/offline-device/device-cert.csr

Sign CSR and produce offline Device certificate::

    openssl x509 -req -in devices/offline-device/device-cert.csr -CAcreateserial -extfile devices/offline-device/device-cert.ext -CAkey local-ca.key -CA local-ca.pem -sha256 -out devices/offline-device/client.pem

Check the generate offline Device key and certificate.
Before doing that you need to find out hostname of your Factory Device Gateway,
it can be extracted from the Device Gateway certificate (``tls-crt``)::

   openssl x509 -noout -in tls-crt -ext subjectAltName

::

    curl --cacert factory_ca.pem --cert devices/offline-device/client.pem --key devices/offline-device/pkey.pem https://<device-gateway-ID>.ota-lite.foundries.io:8443/repo/1.root.json | jq

It is worth noticing that the device is registered at the backend on the first request to Device Gateway in this case.

.. _reference implementation:
   https://github.com/foundriesio/factory-registration-ref
