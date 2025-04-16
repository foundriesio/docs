.. highlight:: sh

.. _ref-ota-architecture:

Architecture Overview
=====================

At a high level, the system consists of three entities:

 * LmP Devices
   
   - Execute ``lmp-device-register`` to associate the device with the gateway
     
   - Run ``aktualizr-lite`` and ``fioconfig`` daemons.

 * The device gateway

 * The Rest API
   - tooling like Fioctl and ``app.foundries.io`` use.

  .. figure:: /_static/reference-manual/ota/ota-arch.png
     :align: center
     :scale: 70 %
     :alt: OTA architecture diagram

Devices talk to the device gateway using `mutual TLS`_.
The device gateway provides a set of REST APIs to support:

* :ref:`aktualizr-lite <ref-aktualizr-lite>`
* :ref:`fioconfig <ref-fioconfig>`
* :ref:`device testing <ref-fiotest>`
* Docker authentication.

Aktualizr-lite and fioconfig run as separate daemons, periodically polling the device gateway with ``HTTP GET`` requests at configurable intervals.

Due to the fact devices are polling the server, REST API changes requested by Fioctl® tooling happen asynchronously.

How A Device Uses Security Hardware
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An LmP device uses Hardware Security Modules (HSM), Trusted Platform Module (TPM) devices, or Trusted Execution Environments (TEE) via the Public-Key Cryptography Standards #11 (PKCS#11) API.

They provide the guarantee that secrets will not be leaked and that communications will be secure.
Certain keys will be provisioned during device manufacturing.

  .. figure:: /_static/reference-manual/ota/lmp-device-arch.png
     :align: center
     :alt: LmP Device architecture diagram



How A Device Finds Updates
~~~~~~~~~~~~~~~~~~~~~~~~~~

Aktualizr-lite uses `TUF`_ to find and validate the available Targets that a device may install.
Aktualizr-lite will periodically check-in using this high level logic:

 * Asks if a ``new root.json`` exists.
   This allows a device to know about key rotations before going further.
   This call is almost always going to result in an HTTP 404 response.

 * Asks for the ``timestamp.json`` metadata.
   If this file has not changed, there is no need to ask for more metadata—nothing has changed.

 * Asks for the ``snapshot.json`` metadata.
   If this file has not changed, there is no need to ask for more metadata—the targets have not changed.

 * Ask for the ``targets.json`` metadata.
   At this point, the device can see if a new Target is available for installation.

.. _mutual TLS:
   https://codeburst.io/mutual-tls-authentication-mtls-de-mystified-11fa2a52e9cf

.. _TUF:
   https://theupdateframework.com/
