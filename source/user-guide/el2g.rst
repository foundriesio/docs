.. _ug-el2g:

Integrating NXP EdgeLock 2GO
============================

EdgeLock® 2GO is an add-on service from NXP®, integrated into FoundriesFactory® to simplify the securing of devices during manufacturing.
The service enables the automated installation and secure storage of required keys, certificates, and credentials when the end device first connects to the internet.

.. admonition:: Key Benefits

   - enablement of manufacturing in an untrusted facility
   - reducing complexity and time required to secure devices on the manufacturing line
   - simplified management of keys and certificates for devices and fleets in the field.

EdgeLock 2GO requires that the device hardware includes an NXP SE05x hardware security element, or uses an i.MX 8ULP or 9 series SoC.
We offer a free evaluation for the `i.MX 8M Plus EVK <https://www.nxp.com/design/development-boards/i-mx-evaluation-and-development-boards/evaluation-kit-for-the-i-mx-8m-plus-applications-processor:8MPLUSLPD4-EVK>`_ with a connected SE050 evaluation,
or on the `Arduino Portenta X8 <https://docs.arduino.cc/hardware/portenta-x8>`_.

Prerequisites
-------------

 * An :ref:`NXP SE05X secure element <ref-secure-elements>`
 * A Factory registered with EdgeLock 2GO. Please `contact our support team <https://foundriesio.atlassian.net/servicedesk/customer/portal/1/group/1/create/3>`_.
 * Access to your Factory :term:`PKI` :ref:`root of trust <Root-of-trust>`.

Enabling Auto-connect to Your Factory
-------------------------------------

Fioctl® can configure EdgeLock 2GO to give out credentials that automatically connect :term:`aktualizr-lite` to the device gateway, removing the need to run ``lmp-device-register``:

.. prompt:: bash host:~$, auto

   host:~$ fioctl el2g config-device-gateway --pki-dir <path to your PKI root of trust>

Now EdgeLock 2GO will have an intermediate CA that can create device client certificates acceptable to the Foundries.io™ device gateway.
Running ``fioctl el2g status`` will show something similar to::

  # Subdomain: yaytcakbhsmvi0cy.device-link.edgelock2go.com

  # Product IDs
  ID            NAME
  --            ----
  935389312472  SE050C2HQ1/Z01V3

  # Secure Objects
      TYPE         NAME                      OBJECT ID
      ----         ----                      ---------
      CERTIFICATE  fio-device-gateway-ca     83000043
      KEYPAIR      fio-device-gateway-ca-kp  83000042

  # Intermediate CAs
  Name: fio-device-gateway-ca
  Algorithm: NIST_P256
  -----BEGIN CERTIFICATE-----
  MIIBmjCCAUCgAwIBAgIUfFokkHTzV2GHUc+P2gKWfe5rWu4wCgYIKoZIzj0EAwIw
  ...

Optional: Enabling Devices to Connect With AWS IoT
----------------------------------------------------

Integrate with AWS IoT using the following steps to enlist devices.

Configure the integration by running:

.. prompt:: bash host:~$, auto

   host:~$ fioctl el2g config-aws-iot

Next run ``aws iot get-registration-code``.
This command uses your local AWS credentials and ``awscli`` to get a Certificate Authority (CA) registration code.
The registration code is a randomly generated number by AWS.
A new intermediate CA will be created in Edgelock 2Go and will be used to sign this code.
New secure objects will then be created and assigned to your device group(s).
The signed verification code and CA certificate are uploaded to AWS IoT.
AWS IoT can verify the registration code was signed properly and complete the process.

.. note::

  If this command is run **after** a device has been initially provisioned,
  you need to perform a manual step on the device to pick up the change:

  .. prompt:: bash device:~$, auto

     device:~$ sudo $(cat /etc/default/lmp-el2go-auto-register) lmp-el2go-auto-register

At this point you have two options: Manual device registration or Just-In-Time-Provisioning (JITP).

Manual Registration
~~~~~~~~~~~~~~~~~~~

Manual registration is the easier path, but not as scalable.
You add devices one-by-one via the AWS WebUI.
Here you will need you to provide the client certificate of the device.
This can be done by looking for the ``aws-iot-ca`` in the output of the device's ``fioctl el2g devices show <device-id>`` output.

JITP
~~~~

JITP automates the device registration process with AWS IoT.
Setting up JITP is specific to a user's AWS deployment, requiring an IAM policy template to define what a device may do.
`Integrating with AWS IoT using Just-in-Time Provisioning`_ shows one way to do this, and includes a template_ that *can* be used here.
With a policy in-hand, enable JITP using the CA created above with ``fioctl el2g config-aws`` by running something like:

.. code-block:: bash

   host:~$ aws iot update-ca-certificate --certificate-id <CERT ID FROM ABOVE> \
   --registration-config='{"templateBody": "{\"Parameters\": {\"AWS::IoT::Certificate::Id\": {\"Type\": \"String\"}, \"AWS::IoT::Certificate::CommonName\": {\"Type\": \"String\"}, \"AWS::IoT::Certificate::SerialNumber\": {\"Type\": \"String\"}}, \"Resources\": {\"thing\": {\"Type\": \"AWS::IoT::Thing\", \"Properties\": {\"ThingName\": {\"Ref\": \"AWS::IoT::Certificate::CommonName\"}, \"AttributePayload\": {\"SerialNumber\": {\"Ref\": \"AWS::IoT::Certificate::SerialNumber\"}}}}, \"certificate\": {\"Type\": \"AWS::IoT::Certificate\", \"Properties\": {\"CertificateId\": {\"Ref\": \"AWS::IoT::Certificate::Id\"}, \"Status\": \"ACTIVE\"}}, \"policy\": {\"Type\": \"AWS::IoT::Policy\", \"Properties\": {\"PolicyName\": \"<YOUR POLICY NAME>\"}}}}", "roleArn": "<YOUR ROLE ARN>"}'

.. _template:
   https://gist.github.com/doanac/b380d1c905f5110ebc5eceb283663ccf#file-setup-py-L68

.. _Integrating with AWS IoT using Just-in-Time Provisioning:
   https://foundries.io/insights/blog/aws-iot-jitp/

Creating an LmP Build With EdgeLock 2GO
---------------------------------------

The Factory's LmP build must have SE05X middleware enabled in order to use EdgeLock 2GO.
This is done by modifying ``meta-subscriber-overrides`` as outlined in the :ref:`se05X enablement <ref-security_se05x_enablement>` section.

The ``EL2GO_HOSTNAME`` variable must be set to your Factory's integration subdomain.
This can be retrieved by running::

  host:~$ fioctl el2g status | grep domain
  # Subdomain: XXXXXXXXXXXXX.device-link.edgelock2go.com

For example::

  # conf/machine/include/lmp-factory-custom.inc
  EL2GO_HOSTNAME = "XXXXXXXXXXXXX.device-link.edgelock2go.com"

You will now need to enable the device auto registration recipe_.
First, include the package in your factory image with::

  # recipes-samples/images/lmp-factory-image.bb
  CORE_IMAGE_BASE_INSTALL += " lmp-el2go-auto-register "

Next, the recipe needs access to your "repo id". The ``fioctl factories`` command will show your value. Put that in the file::

  # recipes-support/lmp-el2go-auto-register/lmp-el2go-auto-register/default.env
  REPOID=<YOUR ID FROM fioctl factories>

Now create a file ``recipes-support/lmp-el2go-auto-register/lmp-el2go-auto-register/root.crt`` with the value of your factory's root CA:

.. prompt:: bash host:~$, auto

  host:~$ fioctl keys ca show --just-root > recipes-support/lmp-el2go-auto-register/lmp-el2go-auto-register/root.crt


Override the main recipe with::

  # recipes-support/lmp-el2go-auto-register/lmp-el2go-auto-register.bbappend
  FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

.. _recipe:
   https://github.com/foundriesio/meta-lmp/tree/main/meta-lmp-base/recipes-support/lmp-el2go-auto-register

Once built with these configuration options a device will start the ``lmp-el2go-auto-register`` script at boot to:

 * Download configured key pairs
 * Configure/start aktualizr-lite

Enlisting Devices
-----------------
Devices must be added to an EdgeLock 2GO allow-list so that they will be authorized to obtain client credentials.
A device with an SE05X, product ID ``935389312472``, can be added with:

.. prompt:: bash host:~$, auto

   host:~$ fioctl el2g devices add 935389312472 <device id>

The status of the device will look similar to::

   host:~$ fioctl el2g devices list
   GROUP             ID                                          LAST CONNECTION
   -----             --                                          ---------------
   fio-935389312472  348555492004256518532939906410866457667712

.. note::

   Device IDs can be found on the device by running:

   .. prompt:: bash device:~$, auto

      device:~$ ssscli se05x uid | grep "Unique ID:" | cut -d: -f2

   This will produce a value like ``04005001eee3ba1ee96e60047e57da0f6880``.
   EdgeLock 2GO expects this in a hexadecimal format with an ``0x`` like: ``0x04005001eee3ba1ee96e60047e57da0f6880``.

Once enlisted, a device's ``lmp-el2go-auto-register`` service will get its new key pair(s) and start the aktualizr-lite daemon.
You should now see the device is provisioned with::

   host:~$ fioctl el2g devices show <device id>
   Hardware Type: SE050C2HQ1/Z01V3
   Hardware 12NC: 935389312472
   Secure Objects:
   NAME                      TYPE         STATUS
   ----                      ----         ------
   fio-device-gateway-ca-kp  KEYPAIR      PROVISIONING_COMPLETED
   fio-device-gateway-ca     CERTIFICATE  PROVISIONING_COMPLETED

If needed, you can troubleshoot this by running:

.. prompt:: bash device:~$, auto

   device:~$ journalctl -fu lmp-el2go-auto-register


Testing AWS IoT
---------------

If your devices are configured to use AWS IoT, you can test using our example container, which publishes an MQTT message to your instance::

  device:~$ docker run --rm -it \
      -e AWS_ENDPOINT=<YOUR AWS MQTT SERVER>.amazonaws.com \
      --device=/dev/tee0:/dev/tee0 \
      hub.foundries.io/lmp/awsiot-optee:postmerge

**NOTE:** If (JITP) is enabled, the first call will **fail** but AWS will register the device.
Subsequent calls will succeed.
The message is published to the topic ``se050/demo`` with a payload of
``{"time": <seconds since epoch>}``.

EdgeLock 2GO Concepts
---------------------

 * **Device Group** — EdgeLock 2GO manages devices by device groups.
   A device group is fixed to a specific product ID (e.g. an SE050 or SE051).
   The ``fioctl el2g`` commands create two device groups for a factory to make it easy to manage a homogenous security policy.
   One device group is for CI devices and the other is for production devices.
 * **Secure Object** — Secure objects are assigned to device groups to tell the EdgeLock 2GO what x509 key pairs should be assigned to devices.
   The most common use of a secure object combines a "Keypair" with a "Certificate".
   The certificate object is linked to an X509 Certificate Authority configured in the service.
   It can then sign certificate signing requests for a device key pair in order to generate client certificates.
 * **Subdomain** — Every EdgeLock 2GO account has a "device-link" subdomain that a device's ``nxp_iot_agent_demo`` binary connects to.
   This is the service where secure objects will be exchanged.

Installing Additional Secure Objects
------------------------------------

You can define Additional Secure Objects in EdgeLock 2GO through the API.
These objects are provisioned into the Secure Element when the device registers.
On top of this, keypairs and certificates are loaded into PKCS#11 so that they are accessible, e.g., OpenSSL.
The convention is that the keypair secure object has an even-numbered OID (e.g. ``0x10000010``),
and the corresponding certificate has an OID one higher (e.g. ``0x10000011``).
To enable automatic loading of the keypair and certificate,
set the ``GENERIC_KEYPAIRS`` variable in ``/etc/default/lmp-el2go-auto-register`` ::

  # recipes-support/lmp-el2go-auto-register/lmp-el2go-auto-register/default.env
  REPOID=<YOUR ID FROM fioctl factories>
  GENERIC_KEYPAIRS="0x10000010"

``GENERIC_KEYPAIRS`` defaults to 0X83000044 which is the OID used by AWS IoT.

Further Details
---------------

FoundriesFactory includes convenient APIs for working with EdgeLock 2GO, which Fioctl uses.
These are documented at https://api.foundries.io/ota/

You may also access the full EdgeLock 2GO API via a reverse proxy:

 ``https://api.foundries.io/ota/factories/<factory>/el2g-proxy/``

API documentation links:

 * `Developer Guide <https://cdn.foundries.io/el2go/AN12642_EdgeLock_2GO_Developer_Guide_for_Foundries.io_users.pdf>`_
 * `OpenAPI Swagger <https://cdn.foundries.io/el2go/el2go-managed-api-gateway-api-58.45.0.yaml>`_

The default FoundriesFactory EdgeLock 2GO implementation provides a free of charge evaluation for 30 days.
After enabling for commercial use, the standard package limits usage to 50,000 devices per subscription year, and 2x key pairs and 2x X.509 certificates per device.
This covers the FoundriesFactory key pair and certificate and one additional set for authentication to a third-party service such as AWS.
If you require additional devices, or more key pairs per device, please contact us.
