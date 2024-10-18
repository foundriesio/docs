.. _ref-device-gateway-pki-details:

Details Of Device Gateway PKI Settings
======================================

The :term:`PKI` for Device Gateway and Factory Devices is vital for the secure communication between them.
It is important to understand exactly what the Factory PKI related commands do.
The :ref:`Factory PKI <ref-device-gateway>` reference manual describes core concepts of your Factory PKI.
It also provides examples to configure your Factory PKI using the :ref:`Fioctl® <ref-fioctl>` commands.

This user guide focuses more on the Factory PKI internals.
That should allow you to integrate with the Factory PKI API directly if you need to.

Fioctl uses the `Golang native cryptographic libraries <https://pkg.go.dev/crypto>`_ to implement all PKI related commands.
However, the same cryptographic functions can be implemented using `OpenSSL <https://www.openssl.org/>`_, as demonstrated in this guide.

.. warning::
   The Factory :ref:`Root of Trust <Root-of-Trust>` **can only be set once**; subsequent attempts will fail.
   Other Factory PKI certificates can be updated at any time; having that you own your Factory Root of Trust.

   `Contact customer support <https://support.foundries.io>`_ if you need your Factory PKI being reset.
   Once you perform a reset, all connected devices will lose their connections.
   These devices will not be able to connect to the Device Gateway until they are re-provisioned with a new Root of Trust.
   In practice this usually means that these devices need to be re-flashed after the Factory PKI reset.


Taking Ownership of Factory PKI Using the API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before setting up your Factory PKI, your devices and Device Gateway talk to each other by utilizing a so-called "shared PKI".
This is the default PKI that the FoundriesFactory™ Platform, sets up as part of provisioning a new Factory.

You can always check your Factory PKI settings using the ``fioctl keys ca show`` command.
In the case of a shared PKI, the command tells you that your Factory PKI is not configured yet.

To take ownership of your Factory PKI, run the ``fioctl keys ca create`` command.
This command communicates with the FoundriesFactory API to create and update Factory specific PKI keys and certificates.

First, a command calls the API to initialize a Factory PKI, which performs the following actions:

- Verify if the Factory PKI was already initialized, and fail if a user attempts to initialize an already initialized PKI.
- Generates a server-side crypto-key for the :ref:`tls-crt` and returns a Certificate Signing Request (CSR) for it.
- Optionally generates a server-side crypto-key for the :ref:`online-ca` and returns a CSR for it.
- Optionally generates a server-side crypto-key for the :ref:`est-tls-crt` and returns a CSR for it.

Once the ``fioctl keys ca create`` command receives a response, it performs the following actions:

    - Generates the Factory Root CA on either your local file system or an HSM device.
    - Optionally generates a Local Device CA on your local file system, and signs it using the Factory Root :term:`CA`.
    - Signs all CSRs received from the above API call.
    - Finally, that command uploads all generated certificates to the API; private keys are not uploaded.

You can replay what the ``fioctl keys ca create`` command does using the following steps.

1. Call the API to Generate CSRs
''''''''''''''''''''''''''''''''

You may use `Curl <https://curl.se/>`_ to play with the Factory PKI APIs.
The following command calls the API to generate CSRs for the server TLS certificate and the Online Device CA::

    curl "https://api.foundries.io/ota/factories/${FACTORY}/certs/" \
        -s -X POST -H "Content-Type: application/json" -H "OSF-Token: $TOKEN" \
        -d '{"first-time-init": true, "tls-csr": true, "ca-csr": true, "est-tls-csr": false}'

The above API returns the following output in case of success::

    {
        "ca-csr": "(Optionally) A CSR for online Device CA of your Factory in PEM format."
        "tls-csr": "A CSR for device APIs server TLS certificate of your Factory in PEM format".
        "est-tls-csr": "(Optionally) A CSR for (Foundries.io hosted) EST server TLS certificate of your Factory in PEM format".
    }

You need to store all received CSRs on your local file system to be able to use OpenSSL to generate corresponding certificates.
For example, store a `tls-csr` into a `tls.csr` file (as used in examples below) and so on.

2. Generate a Private Key and Certificate for Factory Root CA
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

You may use OpenSSL to generate your Factory Root CA.

First, you need to create the following certificate configuration file on your file system::

    factory_ca.cnf:
        [req]
        prompt = no
        distinguished_name = dn
        x509_extensions = ext

        [dn]
        CN = Factory-CA
        OU = <your-factory-name>

        [ext]
        basicConstraints=CA:TRUE
        keyUsage = keyCertSign, cRLSign
        extendedKeyUsage = critical, clientAuth, serverAuth

.. important::
    It is important that the Organization Unit (OU) of your Factory Root CA Subject field is set to your Factory name.
    That information is used by the API to validate that you upload a Root CA for a correct Factory.

Next, use the following OpenSSL command to generate the private key for your Factory Root CA::

    openssl ecparam -genkey -name prime256v1 | openssl ec -out factory_ca.key

The above command stores the private key in a ``factory_ca.key`` file on your local file system.
If you want to store in on an HSM device, look at the `Fioctl Bash based PKI implementation`_ for an example.

.. _Fioctl Bash based PKI implementation: https://github.com/foundriesio/fioctl/blob/main/x509/bash.go

Once you have a configuration and private key files, use the following OpenSSL command to generate the Factory Root CA::

    openssl req -new -x509 -days 7300 -sha256 -config factory_ca.cnf -key factory_ca.key -out factory_ca.pem

The above command stores your Factory Root CA certificate in a ``factory_ca.pem`` file on your local file system.
In this example, the Factory Root CA is self-signed by its own private key.
Alternatively, you may sign it by a higher level CA at your disposal.

3. Optionally Generate Your Local Device CA
'''''''''''''''''''''''''''''''''''''''''''

Although Foundries.io™ securely stores your Factory Online Device CA; its private key is not owned by you.
We recommended generating one or more Local Device CA for your Factory before going to production.
Those Local Device CAs should be used to issue client TLS certificates for your production devices.
In a fully sealed setup you would disable or revoke the Online Device CA for your Factory.

Similarly to the Factory Root CA, you may use OpenSSL to generate your Local Device CA.

First, you need to create the following certificate configuration files on your file system::

    local_ca.cnf
        [req]
        prompt = no
        distinguished_name = dn

        [dn]
        CN = fio-<your-user-uid>
        OU = <your-factory-name>

    ca.ext:
        keyUsage=critical, keyCertSign
        basicConstraints=critical, CA:TRUE, pathlen:0

.. important::
    It is important that the Organization Unit of your Factory Device CA Subject field is set to your Factory name.
    That information is used by the API to validate that you upload a Root CA for a correct Factory.

    Additionally, the Common Name (CN) of your Factory Local Device CA Subject field needs to equal "fio-" plus your user ID.
    A user ID can be determined from the ``fioctl users`` command output or your Factory Users page.
    A user specified in this field becomes an owner of all devices auto-registered using client certificates issued by this CA.

Next, use the following OpenSSL command to generate the private key for your Factory Root CA::

    openssl ecparam -genkey -name prime256v1 | openssl ec -out local_ca.key

Then, generate a CSR for your Local Device CA using the following OpenSSL command::

    openssl req -new -config local_ca.cnf -key local_ca.key -out local_ca.csr

Finally, use OpenSSL to generate your Factory Local Device CA, and sign it by your Factory Root CA::

    openssl x509 -req -days 3650 -sha256 -CAcreateserial -in local_ca.csr \
        -extfile ca.ext -CAkey factory_ca.key -CA factory_ca.pem -out local_ca.pem

These commands will store your Factory Local Device CA private key and certificate in ``local_ca.key`` and ``local_ca.pem`` files.

4. Sign CSRs Received from the API
''''''''''''''''''''''''''''''''''

You may use OpenSSL to sign API provided CSRs for your Factory, similarly to how the Factory Local Device CA is signed.

First, you need to create the following certificate configuration files on your file system::

    server.ext
        keyUsage=critical, digitalSignature
        extendedKeyUsage=critical, serverAuth

    ca.ext:
        keyUsage=critical, keyCertSign
        basicConstraints=critical, CA:TRUE, pathlen:0

Next, use OpenSSL to determine the DNS names from the server TLS CSR, and append it to the server configuration file::

    echo "subjectAltName=$(openssl req -text -noout -verify -in tls.csr | grep DNS:)" >> server.ext

Finally, use OpenSSL to generate the server TLS certificate, and sign it by your Factory Root CA::

    openssl x509 -req -days 3650 -sha256 -CAcreateserial -in tls.csr \
        -extfile server.ext -CAkey factory_ca.key -CA factory_ca.pem -out tls.pem

Similarly, you may generate and sign a server TLS certificate for Foundries.io hosted EST server if you need it.

If you also want to have a Factory Online Device CA, generate and sign using the following OpenSSL command::

    openssl x509 -req -days 3650 -sha256 -CAcreateserial -in online_ca.csr \
        -extfile ca.ext -CAkey factory_ca.key -CA factory_ca.pem -out online_ca.pem

5. Upload Generated Certificates to the API
'''''''''''''''''''''''''''''''''''''''''''

Once you have generated all the necessary certificates, you may upload them to the Factory PKI API.

You might have generated more than one Device CA (for example both Local and Online Device CAs, or several Local Device CAs).
In this case, you need to contatenate them into a single file before the upload, e.g. using this command::

    cat online_ca.pem local_ca.pem >> device_ca_list.pem

Your Factory PKI certificates may be uploaded to the API using this Curl command::

    ROOT_CA_CRT=$(cat factory_ca.pem | awk -v ORS='\\n' '1') \
    DEVICE_CA_CRT=$(cat device_ca_list.pem | awk -v ORS='\\n' '1') \
    TLS_CRT=$(cat tls.pem | awk -v ORS='\\n' '1') \
    curl "https://api.foundries.io/ota/factories/${FACTORY}/certs/" \
        -s -X PATCH -H "Content-Type: application/json" -H "OSF-Token: $TOKEN" \
        -d '{"root-crt": "'"${ROOT_CA_CRT}"'", "tls-crt": "'"${TLS_CRT}"'", "ca-crt": "'"${DEVICE_CA_CRT}"'"}'

After this command your Factory PKI is ready to use.

Registering Factory Devices Using the API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Devices are usually registered with your Factory by running the
`lmp-device-register® <https://github.com/foundriesio/lmp-device-register/>`_ tool.
See the :ref:`getting started guide <gs-register>` for more details on using the tool.

This same task may be accomplished by generating the device client certificate using OpenSSL, and uploading it to the API.
The device may be registered via the FoundriesFactory API or the your own registration service
(e.g. a `factory-registration-ref® <https://github.com/foundriesio/factory-registration-ref>`_).

Below steps perform device registration using OpenSSL the same way as the ``lmp-device-register``
and ``factory-registration-reg`` tools would do.

First, you need to create the following certificate configuration files on your file system::

    client.cnf
        [req]
        prompt = no
        distinguished_name = dn

        [dn]
        CN = <your-device-uuid>
        OU = <your-factory-name>

    client.ext:
        keyUsage=critical, digitalSignature
        basicConstraints=critical, clientAuth

Next, use the following OpenSSL command to generate the private key for your device client certificate::

    openssl ecparam -genkey -name prime256v1 | openssl ec -out client.key

Then, generate a CSR for your device client certificate using the following OpenSSL command::

    openssl req -new -config client.cnf -key client.key -out client.csr

Finally, use OpenSSL to generate your device client certificate, and sign it by your Factory Local Device CA::

    openssl x509 -req -days 3650 -sha256 -CAcreateserial -in client.csr \
        -extfile ca.ext -CAkey local_ca.key -CA local_ca.pem -out client.pem

At this point, the device should be ready to connect to your Factory Device Gateway to fetch updates.
Optionally, you might register your device with the API using this Curl command::

    DEVICE_CRT=$(cat client.pem | awk -v ORS='\\n' '1') \
    curl "https://api.foundries.io/ota/devices/" \
        -s -X PUT -H "Content-Type: application/json" -H "OSF-Token: $TOKEN" \
        -d '{"client.pem": "'"${DEVICE_CRT}"'", "name": "<optional-device-name>"}'

You may run the following commands to verify that your device can connect to your Factory Device Gateway::

    # Run this command first to see the device gateway host name (which looks like <device-gateway-ID>.ota-lite.foundries.io):
    openssl x509 -noout -in tls.pem -ext subjectAltName

    # Then, substitute the <device-gateway-ID> in the below command with your findings.
    curl --cacert factory_ca.pem --cert client.pem --key client.key https://<device-gateway-ID>.ota-lite.foundries.io:8443/repo/1.root.json | jq

If you did not register your device with the API, it will be auto-registered on the first call to the Device Gateway.
