.. _ref-cert-rotation-ug:

Device Certificate Rotation
===========================

The :ref:`Device Certificate Rotation <ref-cert-rotation>` reference manual describes core concepts and functions of certificate rotation.
This page explains how to configure your Factory for this functionality.

Choosing an EST Server
----------------------

Before you can perform certificate rotations, you must ensure you have taken control of your Factory's :ref:`PKI <ref-device-gateway>`.
Specifically, you'll need access to your ``factory_ca.key`` in order to complete these steps.
There are two ways to then run an EST server.

FoundriesFactory Managed
~~~~~~~~~~~~~~~~~~~~~~~~

Running ``fioctl keys est authorize`` will allow FoundriesFactory to run an EST server for you at ``<repoid>.est.foundries.io``.
This command will sign a CSR created in the backend with your Factory's root key.
The resulting TLS certificate will be used by the FoundriesFactory EST server.

.. note::
   This option requires the FoundriesFactory® backend to have a certificate authority to sign renewal requests.
   This "online-ca" is configured when running ``fioctl keys ca create``.

User Managed
~~~~~~~~~~~~

Users may also run their own EST server.
The EST server used by the Foundries.io™ backend is available at:

  https://github.com/foundriesio/estserver

The GitHub project includes the details for getting this server up and running.

Performing a Certificate Rotation
---------------------------------

Certificate rotations are triggered via configuration changes.
Fioctl™ includes a helper for doing this either per device or per device group with:

 * ``fioctl device config rotate-certs <device>``
 * ``fioctl config rotate-certs --group <group>``

In both cases Fioctl defines a file and change handler such as::

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
 * **PKEYIDS**: Devices configured to use HSMs need to know a list of slot IDs to choose from when generating the next private key. 2 IDs are required so it can swap back and forth.
 * **CERTIDS**: Devices configured to use HSMs need to know a list of slot IDs to choose from when storing the new client certificate. 2 IDs are required so it can swap back and forth.
