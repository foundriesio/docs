.. _ref-security:

Security
========

Overview
--------

Security has multiple layers and dimensions.
It starts all the way from booting the device to running software on it and connecting to cloud services.
FoundriesFactory® provides a set of features to target every aspect of your Factory security.

Below sections focus on the following aspects:

  - how to securely connect your devices to Foundries.io™ cloud services.
  - how to securely boot your devices;
  - how to securely update firmware and software on your devices;
  - how to securely store secrets on your devices;


.. _ref-secure-cloud-services:

Secure Connection to Cloud Services
-----------------------------------

Your devices communicate with a set of FoundriesFactory cloud services,
the central of which is the :ref:`Device Gateway <ref-ota-architecture>`.
The `Device Gateway` enforces Factory devices to establish the `Mutual TLS (mTLS) <mTLS_>`_ connection to it.
During the `TLS Handshake <TLS_>`_ phase in `Mutual TLS`,
both the device and the cloud service present and verify their TLS certificates.

The Factory owner must take their :ref:`Factory PKI <ref-device-gateway>` offline before going to production.
We also recommend to take the :ref:`Device Registration Service <ref-factory-registration-ref>` under full control.
Finally, the :ref:`Device Networking <ref-device-network-access>` must be configured properly to connect to cloud services.

.. toctree::
   :maxdepth: 1

   device-gateway
   factory-registration-ref
   device-network-access
   cert-rotation

.. _mTLS:
  https://en.wikipedia.org/wiki/Mutual_authentication#mTLS

.. _TLS:
  https://www.rfc-editor.org/rfc/rfc8446


.. _ref-secure-boot:

Secure Boot (Hardware Root of Trust)
------------------------------------

FoundriesFactory `Secure Boot` is the mechanism to force a device to only execute boot software that is signed by a certain set of keys.
The verification process and corresponding security functions are performed by the SoC boot ROM.
These are the starting points for building a hardware root of trust.

The SoC hardware security manual should be consulted to identify the supported key types and the signing process.
Secure Boot specifics of select hardware platforms are described below.

.. toctree::
   :maxdepth: 1

   secure-boot-imx-habv4
   secure-boot-imx-ahab
   secure-boot-stm32mp1
   authentication-xilinx
   secure-boot-uefi

More information around Secure Boot aspects supported by LmP can be found in:

.. toctree::
   :maxdepth: 1

   secure-machines
   revoke-imx-keys
   tee-on-versal-acap

See how to implement the `Secure Boot Firmware Updates`_ below.

Secure Online Keys for Boot Stack
---------------------------------

FoundriesFactory uses online keys to sign the components from the boot stack during build time.
More information on how these keys are used and how to modify them can be found in the page below.

.. toctree::
   :maxdepth: 1

   factory-keys


.. _ref-ota-security:
.. _OTA:

Secure Over the Air Updates
---------------------------

FoundriesFactory `Over the Air Updates (OTA)` is the mechanism to deliver firmware and software updates to your Factory devices securely.
It leverages `The Update Framework (TUF) <TUF_>`_ underneath which uses a set of keys to sign every software piece.
These keys should be managed :ref:`offline <ref-offline-keys>` by the Factory owner before going to production.

.. toctree::
   :maxdepth: 1

   offline-keys

.. _TUF:
   https://theupdateframework.com/

.. _targets.json:
   https://theupdateframework.com/metadata/


.. _ref-boot-software-updates:

Secure Boot Firmware Updates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FoundriesFactory uses OTA_ to deliver secure boot firmware updates to your devices.
Secure Boot Firmware Update specifics of select hardware platforms are described below.

.. toctree::
   :maxdepth: 1

   boot-software-updates-imx
   boot-software-updates-imx8qm
   boot-software-updates-zynqmp
   boot-software-updates-stm32mp1


.. _ref-secure-elements:

Secure Element as Secrets Storage
---------------------------------

There are different techniques how to securely store secrets on your devices.
We recommend that you take advantage of the `Hardware Security Module (HSM)` to keep your device secrets sealed.

Hardware Secure Module (Secure Element) specifics of select hardware platforms are described below.

.. toctree::
   :maxdepth: 1

   secure-elements/secure-element.050
   secure-elements/se050-enablement
   secure-elements/secure-element.tpm
