.. _ref-device-gateway-pki-details:

Details Of Device Gateway PKI Settings
======================================

The :ref:`Factory PKI <ref-device-gateway>` reference manual describes core concepts of Device Gateway PKI and
how it can be configured by using the ``fioctl keys ca`` command.
The following describes low-level details that are happening behind the scenes during running that ``fioctl`` command.
Also, it provides an instruction to create, sign, and use an *offline* (aka *local*) device certificate.

Under The Hood
~~~~~~~~~~~~~~~~~~~~~~~~~~
The PKI for Device Gateway and Factory Devices is highly important in terms of secure communication between them.
Thus, it's important for users to understand what exactly the given command does underneath.

Before a user setups the PKI, their Devices and Device Gateway talk to each other by utilizing so-called "shared PKI",
this is a default PKI that the Foundries service sets up as part of new Factory provisioning.
The ``fioctl`` command communicates with ``https://api.foundries.io/ota/factories/$FACTORY/certs/``
endpoint to create and update Factory specific PKI keys and certificates. As long as Factory uses the "shared PKI"
the endpoint returns and empty response, meaning that no Factory PKI is set.
::

    curl -s -H "OSF-TOKEN: $TOKEN" https://api.foundries.io/ota/factories/${FACTORY}/certs/ | jq
    {
      "tls-crt": null,
      "ca-crt": null,
      "root-crt": null
    }

* ``root-crt`` is the PKI root CA certificate, also referred as :ref:`Root of Trust <Root-of-trust>`
* ``ca-crt`` is a certificate bundle containing one :ref:`online CA <online-ca>` certificate and optionally one or more :ref:`local CA <local-ca>` certificates, aka "offline-ca".
* ``tls-crt`` is a Device Gateway certificate, also referred as :ref:`a server TLS certificate <tls-crt>`


The first step that the ``fioctl`` command does is sending a post request to the PKI endpoint.
In the following example a response is redirected to a json file so its content can be used later.

::

    curl -s -X POST -H "Content-Type: application/json" -H "OSF-TOKEN: $TOKEN" "https://api.foundries.io/ota/factories/${FACTORY}/certs/" | jq . > factory_certs.json

The endpoint handler does the following:

1. Generates a private key and corresponding CSR (Certificate Signing Request) for Device Gateway (tls-crt);
2. Generates a private key and corresponding CSR for Online Device CA (online-ca);
3. Returns a json formatted response to a caller, the response includes the following:

   a. ``tls-csr`` - CSR for Device Gateway certificate
   b. ``ca-csr`` - CSR for Online Device CA certificate
   c. ``create_ca`` - a script that can be used for root CA creation, i.e. a private key and corresponding self-signed certificate.
   d. ``create_device_ca`` - a script that can be used for "local-ca"/"offline-ca" creation, i.e. a private key, corresponding certificate signed by the root CA.
   e. ``sign_tls_csr`` - a script that signs received ``tls-csr`` by the root CA
   f. ``sign_ca_csr`` - a script that signs received ``ca-csr`` ("online-ca") by the root CA

A user can extract any of the aforementioned fields by utilizing ``jq`` utility. For example:

::

    cat factory_certs.json | jq -r .create_ca

Once the ``fioctl`` command receives a response it makes use of the above mentioned scripts included in a response.
Specifically:

1. Invokes the ``create_ca`` script to generate Root CA key (``factory_ca.key``) and Root CA certificate (``factory_ca.pem``);
2. Signs the ``tls-csr`` by invoking the ``sign_tls_csr`` script, the resultant certificate is stored in ``tls-crt``;
3. Signs the ``ca-csr`` by invoking the ``sign_ca_csr`` script, the resultant certificate is stored in ``online-crt``;
4. Creates a local/offline Device CA by using ``create_device_ca``, the resultant private key and certificate are stored in ``local-ca.key`` and ``local-ca.pem`` correspondingly;

After that, the ``fioctl`` command uploads the generated artifacts to the backend by issuing a PATCH request to the endpoint.
Specifically, the following files are uploaded:

1. ``tls-crt`` - the result of ``tls-csr`` signing;
2. ``online-crt`` and ``local-ca.pem`` bundled together into the ``ca-crt`` field of the PATCH request;
3. ``factory_ca.pem`` - root CA certificate created by running ``create_ca`` transferred via ``root-crt`` fields of the PATCH request.

It should be pointed out that the factory root of trust can be set once.
Thus, the given command ``fioctl keys ca create`` performs work only at the first run, subsequent command calls will fail.
Device CA bundle (``ca-crt``) can be updated many times, specifically a user may add/remove local/offline CA certs to/from the bundle,
``fioctl keys ca update`` command is intended for it.

Device key and certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~
Once the PKI is setup, your Factory Device Gateway is ready to communicate via mTLS with Factory devices.
The devices must have a private key and a x509 certificate to setup mTLS session with Device Gateway
as well as the Root CA certificate to verify Device Gateway certificate during mTLS handshake.

As explained above the ``fioctl`` command generates two types of Device CA, online and local/offline CAs.
Both of these CAs can be used to sign Device CSR.

Online Device certificate
*************************
In the case of online CA, a private key is owned by the backend. Hence, only the backend can sign a Device CSR with the online CA.
The utility called ``lmp-device-register`` can be used for this purpose,
and this is the default device registration mechanism. The tool generates a device private key,
creates corresponding device CSR and makes a request to the backend to sign it with the online CA.
As a response, the backend returns a signed device certificate as well as a default configuration for the device (aka ``sota.toml``).
More details on ``lmp-device-register`` usage can be found in the :ref:`getting started guide <gs-register>`.

Local/Offline Device certificate
********************************

We advise users to use the Factory registration `reference implementation`_ as a mechanism for
offline device key and certificate generation as well as device registration.
The following is a guide on the manual creation of Local/Offline Device keys and certificates.
This can be useful for understanding low-level details of the overall process.


Create a directory for offline device key and certificate.
::

    mkdir -p devices/offline-device


Generate a private key
::

    openssl ecparam -genkey -name prime256v1 -out devices/offline-device/pkey.pem


Set offline Device certificate config
::

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

Make sure to replace <device-UUID> and ${FACTORY} with your values.

Set offline Device certificate extensions
::

   cat > devices/offline-device/device-cert.ext <<EOF
   keyUsage=critical,digitalSignature,keyAgreement
   extendedKeyUsage=critical,clientAuth
   EOF

Generate CSR

::

    openssl req -new -config devices/offline-device/device-cert.conf -key devices/offline-device/pkey.pem -out devices/offline-device/device-cert.csr

Sign CSR and produce offline Device certificate

::

    openssl x509 -req -in devices/offline-device/device-cert.csr -CAcreateserial -extfile devices/offline-device/device-cert.ext -CAkey local-ca.key -CA local-ca.pem -out devices/offline-device/client.pem


Check the generate offline Device key and certificate.
Before doing that you need to find out hostname of your Factory Device Gateway,
it can be extracted from the Device Gateway certificate (``tls-crt``)

::

   openssl x509 -noout -in tls-crt -ext subjectAltName

::

    curl --cacert factory_ca.pem --cert devices/offline-device/client.pem --key devices/offline-device/pkey.pem https://<device-gateway-ID>.ota-lite.foundries.io:8443/repo/targets.json | jq

It is worth noticing that the device is registered at the backend on the first request to Device Gateway in this case.

.. _reference implementation:
   https://github.com/foundriesio/factory-registration-ref