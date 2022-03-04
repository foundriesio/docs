.. highlight:: sh

.. _ref-secure-element:

EdgeLock™ SE050: Plug & Trust Secure Element
============================================

There is extensive documentation online about the EdgeLock™ SE050 Secure Element
so we won't duplicate it here; however for reference we recommend the following reads:

**Data Sheet**:
`SE050 Plug & Trust Secure Element`_

**Application Notes**:
`User Guidelines`_,
`SE050 APDU Specification`_,
`Ease ISA/IEC 62443 compliance with EdgeLock`_

**User Manuals**:
`NXP SE05x T=1 Over I2C Specification`_

The EdgeLock™ SE050 follows the Global Platform Card Specification. So on top of
the previously suggested product documentation we also advise to get some awareness
of the specification by reading the following documents:

**Global Platform Specifications**: `Card Specification 2.3.1`_, `Secure Channel Protocol 03`_

NXP SE050 Plug & Trust MW
--------------------------
NXP provides a software stack to support this device in a number of environments:
the SE050 Plug&Trust Middleware. As of version 2.14 those would be.

* Linux: iMX6UL, iMX8Mq
* FreeRTOS/baremetal: K64F, iMX RT 1050, LPC55S
* Android: Hikey960
* Raspian Linux: Raspberry-Pi-3
* Windows

There is also extensive documentation in the form of PDF and HTML browsable documents
within the freely downloadable `NXP SE050 Plug & Trust MW`_ software package
We recommend users to download and succinctly read them to better understand what
the product has to offer.



NXP SE050 Plug & Trust TEE Integration
--------------------------------------

At Foundries.io we believe in securing systems by extending the perimeter of the
**hardware root of trust** to as many operational phases as possible: secure monitoring,
secure authentication, storage protection, secure communication and key management.

Because a number of our customers have been targeting the NXP SE050 in their designs,
we chose to integrate the NXP middleware with our ROT (root of trust) by bringing
it under the umbrella of our Trusted Execution Environment: OP-TEE.

The SE050 middleware is a behemoth of a software stack: highly configurable, highly
flexible and therefore sometimes difficult to navigate. And derived from its flexibility
comes its complexity and size - well over half a million lines of code.

Fortunately, most of the functionality provided by the TEE overlaps with that
provided by the SE050; in particular all cryptographic operations have a software
mirror implementation in OP-TEE: ECC, RSA, MAC, HASH, AES, 3DES and so forth.

This meant that we could validate our integration using the OP-TEE crypto regression
test suite from the `OP-TEE sanity tests`_

The main advantage of using the SE050 in a product design which already runs a TEE
is that all private keys programmed in the device's non volatile memory will never
be leaked to the outside world.

The SE050 also provides a real random number generator which can be exported to
the REE (normal world) to improve its entropy requirements.

Because the TEE is its only client, the TEE SE050 stack only requires a single
global session and key store. Policies are configured so only the SCP03 enabled
session can access its objects for creation or deletion.

OP-TEE Integration
-------------------

The SE050 standard physical interface is I2C typically configured as a slave running
in high speed mode (3.4Mbps). Since the SE050 could replace all the OP-TEE default crypto
operations (software), we chose to implement a native I2C driver so the SE050
could be accessed as early as possible.

OP-TEE's cryptographic providers are not runtime configurable meaning that the user
must choose at compile time where to execute its cryptographic functions: whether in
libmbedtls, in libtomcrypt or now in the SE050. But this is **not** an all or nothing configuration
and operations can be routed to one service or another; for instance on an iMX platform
the Hardware Unique Key could be retrieved from the CAAM, AES ECB and HASH operations implemented
in libtomcrypt, and RNG, ECC and RSA in the SE050.

.. note::
      As a typical scenario, choosing to run AES ECB and HASH on the SE050 might
      be a bad idea due to its performance implications as those operations are heavily
      used to verify the trusted filesystem in OP-TEE and would dramatically slow down
      the opening of trusted applications.

Serial Communications to the SE050
----------------------------------

The first step taken during the integration work was to develop and upstream a
native I2C driver (imx_i2c). But since this driver could not be used once the REE
started executing - as it would not protect against I2C bus collisions or power management
implementations controlled from the REE - we needed a second driver: a sort of i2c
trampoline service capable to routing I2C read and write operations from OP-TEE to
the REE driver (Linux in particular).

.. note::
       These drivers are configurable using the following build options::

	CFG_CORE_SE05X_I2C_BUS=: the I2C bus where the SE050 sits
	CFG_CORE_SE05X_BAUDRATE=: the SE050 baud-rate in mbps

Secure Communication Protocol 03
---------------------------------

The SE050 has native support for Global Platform Secure Communication Protocol 03 which
allows us to protect the integrity of end to end communications between the
processor and the SE050. All data sent to the SE050 is software encrypted and all
data received decrypted in the TEE using a set of predefined keys shipped with
the devices.

These keys can be securely rotated. Once rotated, they are stored in the TEE secure
file system.

.. note::
      We can choose whether to enable SCP03 right after boot with its default set of
      keys or at a later time once the RPMB-FS (or REE-FS) are available so the
      keys can be read from secure storage::

	CFG_CORE_SE05X_SCP03_EARLY=y : enables SCP03 with its default keys set
	CFG_CORE_SE05X_SCP03_PROVISION=y: allows SCP03 rotation set


Provisioning of new SCP03 keys is only available if *CFG_CORE_SE05X_SCP03_EARLY* is not set as we
would not be able to write back the new keys to secure storage.

To trigger SCP03 key rotation you need to execute the host side of the following
Pseudo Trusted Application from the REE: `scp03`_

.. warning::
     If the secure database storing the SCP03 keys gets corrupted, the processor will
     no longer be able to access the SE050 over an encrypted connection. Moreover there is
     no protocol defined to recover from that situation.

SE050 Non Volatile Memory
-------------------------

The current implementation of the SE050 TEE driver only allows for permanent
storage of the ECC and RSA keys. These keys can be managed using the cryptoki
API implementing the pkcs#11 standard. External keys used by the SE050 to perform
other cryptographic operations are not stored in the SE050 NVM.

.. note::
      The SE050 NVM can be cleared by setting the following configuration option::

	CFG_CORE_SE05X_INIT_NVM=y


Be aware that initializing the NVM would cause all keys and objects to be deleted
from permanent storage. This however has no impact on the SCP03 set of keys.

Importing Secure Objects to PKCS#11 tokens
------------------------------------------

After manufacturing, the NXP SE050 will contain pre-provisioned keys and certificates. These secure objects will be known to the user through internal documentation and will be accessible from the TEE by their 32 bit identifiers.

To import those objects into PKCS#11 tokens, we have extended our `TEE pkcs#11 implementation`_ and developed a secured `SE050 Object Import Application`_ to interface to the TEE and gain secure access to the SE050.

The following diagram succintly details the overall design:

   .. figure:: /_static/se050-import-keys.png
      :align: center
      :width: 6in

The *certificates* are retrieved in DER format using the import PTA and then written to the pkcs#11 token.

The *keys* however are retrieved via a pkcs#11 key generation request to the crypto driver through the OP-TEE core; the request will contain the key identifier which the driver will query from the SE050. If successfull, the keypair is returned to pkcs#11 and commited to secure storage.


.. note::
      The private key will just be a handle to the actual key stored in Non Volatile Memory: private keys are **never** exposed outside the NXP SE050.


.. _TEE pkcs#11 implementation:
   https://github.com/foundriesio/optee-sks

.. _SE050 Object Import Application:
    https://github.com/foundriesio/optee-se050-pkcs11-import

.. _SE050 Plug & Trust Secure Element:
   https://www.nxp.com/docs/en/data-sheet/SE050-DATASHEET.pdf

.. _User Guidelines:
   https://www.nxp.com/webapp/Download?colCode=AN12514

.. _SE050 APDU Specification:
   https://www.nxp.com/docs/en/application-note/AN12413.pdf

.. _Ease ISA/IEC 62443 compliance with EdgeLock:
   https://www.nxp.com.cn/docs/en/application-note/AN12660.pdf

.. _NXP SE05x T=1 Over I2C Specification:
   https://www.nxp.com/webapp/Download?colCode=UM11225&location=null

.. _Card Specification 2.3.1:
   https://globalplatform.org/specs-library/card-specification-v2-3-1/

.. _Secure Channel Protocol 03:
   https://globalplatform.org/wp-content/uploads/2014/07/GPC_2.3_D_SCP03_v1.1.2_PublicRelease.pdf

.. _NXP SE050 Plug & Trust MW:
   https://www.nxp.com/products/security-and-authentication/authentication/edgelock-se050-plug-trust-secure-element-family-enhanced-iot-security-with-maximum-flexibility:SE050?tab=Design_Tools_Tab

.. _scp03:
   https://github.com/foundriesio/optee-scp03

.. _OP-TEE sanity tests:
    https://optee.readthedocs.io/en/latest/building/gits/optee_test.html
