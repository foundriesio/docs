.. highlight:: sh

.. _ref-secure-element.tpm:

Trusted Platform Module
=======================

Trusted Platform Module (TPM) is a specialized microcontroller (or provided as firmware) designed
to provide hardware-based security capabilities. When available to a hardware platform it can
serve as secure storage for cryptographic keys, enable support for secure boot,
and provides a mechanism for measuring and verifying system integrity.

.. note::
   This page applies to TPM 2.0

With Linux® microPlatform (LmP), TPM devices can be used to assist with secure boot (based on the boot firmware
capabilities) and to manage and protect cryptographic keys used by the OTA client (``aktualizr-lite``)
and by the configuration manager (``fioconfig``).

TPM 2 Software Stack
--------------------

The `TPM2 software stack`_ is a complex set of software components that enable the integration and use
of the TPM2 device. The software stack is comprised of multiple layers and abstractions, each providing
different functionalities and interfaces to interact with the TPM2 chip.

The main software component used is `TPM 2 Software Stack (TSS)`_. This layer provides a software framework
for developing TPM2 applications. It also provides a set of APIs for application developers to interact
with the TPM2 chip, such as key management, encryption, and decryption. The TSS also manages the communication
with the TPM2 driver.

While it is possible to leverage TPM 2 via TSS directly (e.g. using ``tpm2-tss-engine`` with OpenSSL), in order
to have a single and common interface for the software stack used in LmP, the integration leverages the
`TPM 2 Public-Key Cryptography Standards (PKCS) #11`_ interface instead.

TPM 2 PKCS#11 Support
---------------------

The `PKCS#11 API`_ provides a standardized way for applications to interact with security tokens, such as smart
cards, NXP® SE05X and TPM 2 devices. The `TPM 2 Public-Key Cryptography Standards (PKCS) #11`_ implementation provides
a set of functions that enable applications to use the security capabilities of the TPM 2 device, such as key generation,
storage, and cryptographic operations, without requiring direct integration with the TPM2 software stack and APIs,
allowing it to be generic to PKCS#11.

The `TPM 2 PKCS#11 architecture`_ document explains the design internals. The default data store in LmP is set to
``/var/tmp2_pkcs11``, and by default the objects are stored under a persistent primary key in the owner hierarchy.
It is also possible to `use existing TPM2 objects`_ created with ``tpm2-tss-engine``, which requires linking via
the ``tpm2_ptool`` command line tool.

Also see :ref:`OTA Architecture Overview <ref-ota-architecture>` for the complete overview of software stack used by LmP,
including the integration with TPM 2 PKCS#11.

Validating TPM 2 PKCS#11
------------------------

The TPM2 PKCS#11 library is available at ``/usr/lib/pkcs11/libtpm2_pkcs11.so``.

.. code-block:: shell

    # Clear TPM and erase tpm2_pkcs11 database
    tpm2_clear -c p
    rm -f /var/tpm2_pkcs11/tpm2_pkcs11.sqlite3

    PTOOL='pkcs11-tool --module /usr/lib/pkcs11/libtpm2_pkcs11.so'

    # Initialize the pkcs11 token
    $PTOOL --init-token --label tpm2token --so-pin 12345678
    $PTOOL --init-pin --token-label tpm2token --so-pin 12345678 --pin 87654321

    # Generate 2 ECDSA keypairs
    $PTOOL --keypairgen --key-type EC:prime256v1 --token-label tpm2token --id 01 --label eckey --pin 87654321
    $PTOOL --keypairgen --key-type EC:prime256v1 --token-label tpm2token --id 02 --label eckey2 --pin 87654321

    # Perform sign & verify
    openssl dgst -binary -sha256 /usr/lib/pkcs11/libtpm2_pkcs11.so > file.sha
    $PTOOL --sign --id 01 --label eckey --token-label tpm2token --pin 87654321 --mechanism ECDSA --input-file file.sha --output-file file.sha.sig
    $PTOOL --verify --id 01 --label eckey --token-label tpm2token --pin 87654321 --mechanism ECDSA --input-file file.sha --signature-file file.sha.sig

    # ECDH1 derive
    $PTOOL --read-object --type pubkey --id 02 --token-label tpm2token --pin 87654321 -o /tmp/pub.der
    $PTOOL --derive -m ECDH1-DERIVE --id 01 --label eckey --token-label tpm2token --pin 87654321 --input-file /tmp/pub.der --output-file /tmp/bytes

For more information, please check `pkcs11 tool configuration guide`_ and the `OPTIGA TPM Application Note`_.

Registering LmP Devices With TPM 2 PKCS#11
------------------------------------------

The LmP registration tool ``lmp-device-register`` supports using PKCS#11 providers for handling the ECDSA
keypair and TLS certificate. This tool is also responsible for configuring ``/var/sota/sota.toml`` with the required
PKCS#11 module path and pins (needed by ``aktualizr-lite`` and ``fioconfig``).

To register with support for TPM 2 PKCS#11:

.. code-block:: shell

    lmp-device-register -n <device-name> -m /usr/lib/pkcs11/libtpm2_pkcs11.so -S <so-pin> -P <user-pin>

.. _TPM2 software stack:
   https://tpm2-software.github.io/

.. _TPM 2 Software Stack (TSS):
   https://github.com/tpm2-software/tpm2-tss

.. _TPM 2 Public-Key Cryptography Standards (PKCS) #11:
   https://github.com/tpm2-software/tpm2-pkcs11

.. _PKCS#11 API:
   http://docs.oasis-open.org/pkcs11/pkcs11-base/v2.40/os/pkcs11-base-v2.40-os.html

.. _TPM 2 PKCS#11 architecture:
   https://github.com/tpm2-software/tpm2-pkcs11/blob/master/docs/ARCHITECTURE.md

.. _use existing TPM2 objects:
   https://github.com/tpm2-software/tpm2-pkcs11/blob/master/docs/INTEROPERABILITY.md

.. _OPTIGA TPM Application Note:
   https://raw.githubusercontent.com/Infineon/pkcs11-optiga-tpm/main/documents/tpm-appnote-pkcs11.pdf
.. _pkcs11 tool configuration guide:
   https://github.com/tpm2-software/tpm2-pkcs11/blob/master/docs/PKCS11_TOOL.md
