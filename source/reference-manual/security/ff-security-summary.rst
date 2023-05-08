Summary of Crypto Keys Used by FoundriesFactory
===============================================

This page provides a brief summary cryptographic keys used by FoundriesFactory®.
For detailed information on each key, please check the relevant page under :ref:`ref-security`.

Secure Connection to Cloud Services
-----------------------------------

These certificates are required to access the FoundriesFactory CI servers.

.. list-table:: Device Gateway Certificates Summary
   :header-rows: 1

   * - Keys
     - Type
     - Owner
   * - Root of Trust key (``factory_ca.key``)
     - NIST P-256
     - Owned and managed by the customer (offline key)
   * - TLS key
     - NIST P-256
     - Owned and managed by Foundries.io (used for mTLS handshake)
   * - Online CA private key (``online-ca.key``)
     - NIST P-256
     - If enabled (required by ``lmp-device-register`` for performing the device CSR), owned and managed by Foundries.io
   * - Local CA private key (``local-ca.key``)
     - NIST P-256
     - If enabled, owned and managed by the customer (used for performing the device CSR)

Secure Boot (Hardware Root of Trust)
------------------------------------

.. list-table:: Secure Boot Certificates Summary
   :header-rows: 1

   * - Keys
     - Type
     - Owner
   * - Hardware Root of Trust Key
     - Depends on the SoC
     - Owned and managed by the customer (offline key)

The Hardware Root of Trust depends on the SoC used.
Please refer to :ref:`ref-secure-boot` pages and
to the vendor reference manual for more information.

Secure Online Keys for Boot Stack
---------------------------------

The exact list of keys used for the boot stack depends on the hardware used.
Some platforms will not make use of all keys.
A list of available keys for an LmP build can be found below:

.. list-table:: LmP Build Certificates Summary
   :header-rows: 1

   * - Keys
     - Type
     - Owner
     - LmP Variable
   * - :ref:`SPL Verification Key <ref-factory-key-spldev>`
     - RSA 2048
     - Owned by the customer, available as an online key for FoundriesFactory CI
     - ``UBOOT_SPL_SIGN_KEYNAME``
   * - :ref:`U-Boot Proper Verification Key <ref-factory-key-ubootdev>`
     - RSA 2048
     - Owned by the customer, available as an online key for FoundriesFactory CI
     - ``UBOOT_SIGN_KEYNAME``
   * - :ref:`OP-TEE Verification Key <ref-factory-key-opteedev>`
     - RSA 2048
     - Owned by the customer, available as an online key for FoundriesFactory CI
     - ``OPTEE_TA_SIGN_KEY``
   * - :ref:`Kernel Modules Verification Key <ref-factory-key-linux-module>`
     - RSA 2048
     - Owned by the customer, available as an online key for FoundriesFactory CI
     - ``MODSIGN_PRIVKEY``
   * - :ref:`UEFI Verification Key  <ref-secure-boot-uefi>`
     - RSA 2048
     - Owned by the customer, available as an online key for FoundriesFactory CI
     - ``${UEFI_SIGN_KEYDIR}/DB.key``
   * - :ref:`TF-A Verification Key <ref-factory-key-tfa>`
     - ECDSA (prime256v1)
     - Owned by the customer, available as an online key for FoundriesFactory CI
     - ``TF_A_SIGN_KEY_PATH``

The detailed description for the LmP Build certificates,
including diagrams for the boot flow, is in :ref:`ref-factory-keys`.

Secure Over the Air Updates
---------------------------

.. list-table:: Secure OTA Certificates Summary
   :header-rows: 1

   * - Keys
     - Type
     - Owner
   * - Offline TUF Root Key
     - Ed25519 (default) or RSA 4096 **(*)**
     - Owned and managed by the customer (offline key)
   * - Online TUF Snapshot Key
     - Ed25519 (default) or RSA 4096 **(*)**
     - Owned and managed by FoundriesFactory CI
   * - Online TUF Timestamp Key
     - Ed25519 (default) or RSA 4096 **(*)**
     - Owned and managed by FoundriesFactory CI
   * - Online TUF Targets Signing Key
     - Ed25519 (default) or RSA 4096 **(*)**
     - Owned and managed by FoundriesFactory CI
   * - Offline TUF Targets Signing Key
     - Ed25519 (default) or RSA 4096 **(*)**
     - Owned and managed by the customer (offline key)
   * - OTA Client (``aktualizr-lite``/``fioconfig``) mTLS Key
     - NIST P-256
     - Owned by the device (unique per device), created during registration (CSR)

.. note::
   **(*)** Can be selected at Factory creation or changed later.

   Factories created before **v89** use ``RSA 4096`` by default but can switch to use ``Ed25519``.
