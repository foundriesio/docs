.. highlight:: sh

.. _ref-secure-element:

EdgeLock™ SE05x: Plug & Trust Secure Element
============================================

There is extensive documentation online about the EdgeLock™ SE05x Secure Element
so we won't duplicate it here; however for reference we recommend the following reads:

**Data Sheet**:
`SE05x Plug & Trust Secure Element`_

**Application Notes**:
`User Guidelines`_,
`SE05x APDU Specification`_,
`Ease ISA/IEC 62443 compliance with EdgeLock`_

**User Manuals**:
`NXP SE05x T=1 Over I2C Specification`_

The EdgeLock™ SE05x follows the Global Platform Card Specification. So on top of
the previously suggested product documentation we also advise to get some awareness
of the specification by reading the following documents:

**Global Platform Specifications**: `Card Specification 2.3.1`_, `Secure Channel Protocol 03`_

NXP SE05x Plug & Trust MW
--------------------------
NXP provides a software stack, the SE05x Plug&Trust Middleware, to support this
device in a number of environments.

There is also extensive documentation in the form of PDF and HTML browsable documents
within the freely downloadable `NXP SE05x Plug & Trust MW`_ software package.
We recommend users to download and succinctly read them to better understand what
the product has to offer.

A reduced open source version of this middleware is the Plug-and-Trust `mini
package`_ used in our OP-TEE integration. We forked the repository and
maintain it on our public github server. Since support for the SE05x
exists in OP-TEE upstream, OP-TEE references this project in order to run its
Azure CI pipeline and avoid build regressions.

.. note::
      The support for the SE05x in OP-TEE is generic and not platform dependent: it
      only requires an OP-TEE native I2C driver to enable SCP03 early during boot.


NXP SE05x Plug & Trust TEE Integration
--------------------------------------

At Foundries.io we believe in securing systems by extending the perimeter of the
**hardware root of trust** to as many operational phases as possible: secure monitoring,
secure authentication, storage protection, secure communication and key management.

Because a number of our customers have been targeting the NXP SE05x in their designs,
we chose to integrate the NXP middleware with our ROT (root of trust) by bringing
it under the umbrella of our Trusted Execution Environment: OP-TEE.

The SE05x middleware is a behemoth of a software stack: highly configurable, highly
flexible and therefore sometimes difficult to navigate. And derived from its flexibility
comes its complexity and size - well over half a million lines of code.

Fortunately, most of the functionality provided by the TEE overlaps with that
provided by the SE05x; in particular all cryptographic operations have a software
mirror implementation in OP-TEE: ECC, RSA, MAC, HASH, AES, 3DES and so forth.

This meant that we could validate our integration using the OP-TEE crypto regression
test suite from the `OP-TEE tests`_

The main advantage of using the SE05x in a product design which already runs a TEE
is that all private keys programmed in the device's non volatile memory will never
be leaked to the outside world.

The SE05x also provides a real random number generator which can be exported to
the REE (normal world) to improve its entropy requirements.

Because the TEE is its only client, the TEE SE05x stack only requires a single
global session and key store. Policies are configured so only the SCP03 enabled
session can access its objects for creation or deletion.

OP-TEE Integration
-------------------

The SE05x standard physical interface is I2C typically configured as a target running
in high speed mode (3.4Mbps). Since the SE05x could replace the OP-TEE default crypto
operations (software), we chose to implement a native I2C driver so the SE05x
could be accessed as early as possible.

OP-TEE's cryptographic providers are not runtime configurable meaning that the user
must choose at compile time where to execute its cryptographic functions: whether in
libmbedtls, libtomcrypt or now in the SE05x. But this is **not** an all or nothing configuration
and operations can be routed to one service or another; for instance on an iMX platform
the Hardware Unique Key could be retrieved from the CAAM, AES ECB and HASH operations implemented
in libtomcrypt, and RNG, ECC and RSA in the SE05x.

.. note::
      As a typical scenario, choosing to run AES ECB and HASH on the SE05x might
      be a bad idea due to its performance implications as those operations are heavily
      used to verify the trusted filesystem in OP-TEE and would dramatically slow down
      the opening of trusted applications.

Serial Communications to the SE05x
----------------------------------

The first step taken during the integration work was to develop and upstream a
native I2C driver (imx_i2c). But since this driver could not be used once the REE
started executing - as it would not protect against I2C bus collisions or power management
implementations controlled from the REE - we needed a second driver: a sort of i2c
trampoline service capable to routing I2C read and write operations from OP-TEE to
the REE driver (Linux in particular).

.. note::
       These drivers are configurable using the following build options::

	CFG_CORE_SE05X_I2C_BUS=   : the I2C bus where the SE05x sits
	CFG_CORE_SE05X_BAUDRATE=  : the SE05x baud-rate in mbps

Secure Communication Protocol 03
---------------------------------

The SE05x has native support for Global Platform Secure Communication Protocol 03 which
allows us to protect the integrity of end to end communications between the
processor and the SE05x. All data sent to the SE05x is software encrypted and all
data received is then decrypted in the TEE using a set of session specific keys. 
These keys are derived from predefined keys which are shipped with the devices.

.. note::
       The user can select whether to enable SCP03 during the secure world initialization
       or at a later time from the normal world by using the `scp03`_ command::

	CFG_CORE_SE05X_SCP03_EARLY=y : enables SCP03 before the Normal World has booted
	CFG_SCP03_PTA=y              : allows SCP03 to be enabled from the Normal World.

The predefined factory keys stored on the SE05X NVM (**static keys** from here
on) are public and should therefore be rotated to a secret set from
which session keys can be derived. 

To avoid having to store new static keys — reducing the surface attack and
simplifying the firmware upgrade process — the new set of keys will be derived in
OP-TEE from its core secret: the Hardware Unique Key (HUK)

.. warning::
     Once the static SCP03 keys have been derived from the HUK and programmed
     into the device's NVM the **HUK MUST NOT CHANGE**.
     
     It is equally critical that the HUK remains a **secret**.

There are two different ways of rotating the SCP03 key: with and without user
intervention from the Normal World.

To rotate the static SCP03 keys from the Trust Zone before the Normal World is
executing, the user should enable **CFG_CORE_SE05X_SCP03_PROVISION_ON_INIT=y**.

To rotate the static SCP03 keys from the Normal World, the user should enable
**CFG_CORE_SE05X_SCP03_PROVISION=y** and then use the `scp03`_ command.

SE05x Non Volatile Memory
-------------------------

The current implementation of the SE05x TEE driver only allows for permanent
storage of the ECC and RSA keys. These keys can be managed using the cryptoki
API implementing the pkcs#11 standard. External keys used by the SE05x to perform
other cryptographic operations are not stored in the SE05x NVM.

.. note::
      The SE05x NVM can be cleared by setting the following configuration option::

	CFG_CORE_SE05X_INIT_NVM=y

      Alternatively, the SE05x NVM can also be cleared by issuing the following
      command on the target: ::

        $ ssscli se05x reset
        
     The ssscli tool will be discussed in the next section.


Be aware that initializing the NVM would cause all keys and objects to be deleted
from permanent storage, but would not affect any handles that the PKCS#11 TA
might have stored in its database which would now point nowhere.
This configuration option however has no impact on the SCP03 set of static keys
which will remain unchanged.


Importing Secure Objects to PKCS#11 tokens
------------------------------------------

After manufacturing, the NXP SE05x will contain pre-provisioned keys and
certificates. These secure objects will be known to the user through their
product specific internal documentation and will be accessible from the TEE by
their 32 bit identifiers.

To import those objects into PKCS#11 tokens, we have extended the `TEE pkcs#11
implementation`_. This allows the user to call standard tools like pkcs11-tool
to import keys into the database; as we said earlier, private keys can't be
exposed outside the secure element and therefore these calls shall only import
the handles to access those keys. The SE05x OP-TEE driver is prepared to work
with either keys or key handles. Storing handles in the pkcs#11
database does not impose restrictions to the user.

.. note::
      The private key will be a handle to the actual key in the element NVM:
      private keys are **never** exposed outside the NXP SE05x. For example, to
      import the data-sheet documented 32 bit 0xF7000001 RSA 4096 bit key into
      the pkcs#11 database, issue the following command:

      .. code-block:: none
	 
          $ pkcs11-tool --module /usr/lib/libckteec.so.0.1 --keypairgen --key-type RSA:4096 --id 01 --token-label fio --pin 87654321 --label SE_7F000001 


We have also developed a tool, the `SE05x Object Import Application`_.
This tool interfaces with the TEE and gains access to the SE05x to import keys
*and* certificates, as well as listing and removing objects from the secure
element non-volatile memory.

The *certificates* are retrieved in DER format using the APDU interface
presented by the driver, and are then written to the pkcs#11 token.

The tool uses `libseteec`_ to send the APDUs to the secure element.
and `libckteec`_ to interface with the PKCS#11 implementation.

The `apdu`_ based interface in fact enables privileged user applications to
access the Secure Element. It does this by allowing the normal world to send
APDU frames that encode data and operations to the SE05x using OP-TEE's SCP03
enabled secure session.

Find some usage examples in the note below. Be aware that in OP-TEE's PKCS#11
implementation **each** PKCS#11 slot is indeed a token.

.. note::
      Import NXP SE051 Certficate with the id 0xf0000123 into OP-TEE
      pkcs#11'aktualizr' token storage:
      
      .. code-block:: none
		      
          $ fio-se05x-cli --token-label aktualizr --import-cert 0xf0000123 --id 45 --label fio

      Show NXP SE050 Certficate with the id 0xf0000123 on the console:
      
      .. code-block:: none
		      
          $ fio-se05x-cli --show-cert 0xf0000123 --se050
      
      Import NXP SE051 RSA:2048 bits key with the id 0xf0000123 into OP-TEE
      pkcs#11 'aktualizr' token storage:
      
      .. code-block:: none
		      
          $ fio-se05x-cli --token-label aktualizr --import-key 0xf0000123 --id 45 --key-type RSA:2048 --pin 87654321

      List all objects in the device's Non Volatile Memory:
      
      .. code-block:: none

          $ fio-se05x-cli --list-objects

      Delete OP-TEE created objects from the device's Non Volatile Memory (one specific object or all):

      .. code-block:: none

          $ fio-se05x-cli --delete-object 0x123456a1
          $ fio-se05x-cli --delete-object all


The following diagram succintly details the overall design:

   .. figure:: /_static/se050-import-keys.png
      :align: center
      :width: 6in


A python application that also uses the APDU interface is `ssscli`_, a tool developed by
NXP to provide direct access to its secure element. This tool might serve some
purpose during development but it is not required on a deployed product (we
advise users to deploy **fio-se05x-cli** and standard pkcs#11 tools instead).


.. code-block:: none

    fio@imx8mm-lpddr4-evk:~/$ ssscli
    Usage: ssscli [OPTIONS] COMMAND [ARGS]...

      Command line interface for SE05x

    Options:
      -v, --verbose  Enables verbose mode.
      --version      Show the version and exit.
      --help         Show this message and exit.

    Commands:
      a71ch       A71CH specific commands
      cloud       (Not Implemented) Cloud Specific utilities.
      connect     Open Session.
      decrypt     Decrypt Operation
      disconnect  Close session.
      encrypt     Encrypt Operation
      erase       Erase ECC/RSA/AES Keys or Certificate (contents)
      generate    Generate ECC/RSA Key pair
      get         Get ECC/RSA/AES Keys or certificates
      policy      Create/Dump Object Policy
      refpem      Create Reference PEM/DER files (For OpenSSL Engine).
      se05x       SE05X specific commands
      set         Set ECC/RSA/AES Keys or certificates
      sign        Sign Operation
      verify      verify Operation


.. _TEE pkcs#11 implementation:
   https://github.com/OP-TEE/optee_os/tree/master/ta/pkcs11

.. _SE05x Plug & Trust Secure Element:
   https://www.nxp.com/docs/en/data-sheet/SE050-DATASHEET.pdf

.. _User Guidelines:
   https://www.nxp.com/webapp/Download?colCode=AN12514

.. _SE05x APDU Specification:
   https://www.nxp.com/docs/en/application-note/AN12413.pdf

.. _Ease ISA/IEC 62443 compliance with EdgeLock:
   https://www.nxp.com.cn/docs/en/application-note/AN12660.pdf

.. _NXP SE05x T=1 Over I2C Specification:
   https://www.nxp.com/webapp/Download?colCode=UM11225&location=null

.. _Card Specification 2.3.1:
   https://globalplatform.org/specs-library/card-specification-v2-3-1/

.. _Secure Channel Protocol 03:
   https://globalplatform.org/wp-content/uploads/2014/07/GPC_2.3_D_SCP03_v1.1.2_PublicRelease.pdf

.. _NXP SE05x Plug & Trust MW:
   https://www.nxp.com/products/security-and-authentication/authentication/edgelock-se050-plug-trust-secure-element-family-enhanced-iot-security-with-maximum-flexibility:SE050?tab=Design_Tools_Tab

.. _scp03:
   https://u-boot.readthedocs.io/en/latest/usage/cmd/scp03.html

.. _OP-TEE tests:
    https://optee.readthedocs.io/en/latest/building/gits/optee_test.html

.. _mini package:
   https://github.com/NXP/plug-and-trust

.. _scp03 PTA:
   https://github.com/OP-TEE/optee_os/blob/master/core/pta/scp03.c

.. _libseteec:
   https://github.com/OP-TEE/optee_client/commit/f4f54e5a76641fda22a49f00294771f948cd4c92

.. _libckteec:
   https://github.com/OP-TEE/optee_client/tree/master/libckteec
   
.. _ssscli:
   https://github.com/foundriesio/plug-and-trust-ssscli

.. _SE05x Object Import Application:
   https://github.com/foundriesio/fio-se05x-cli

.. _apdu:
   https://github.com/OP-TEE/optee_client/blob/master/libseteec/src/pta_apdu.h
