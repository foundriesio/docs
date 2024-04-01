Terminology
===========

.. Glossary::
   :sorted:

   FoundriesFactory
     :term:`Foundries.io`'s Cloud native DevSecOps platform.
     Used for building, testing, deploying and maintaining Linux-based devices.
     Includes the :term:`Linux microPlatform` distro, OTA update mechanisms, and management tools such as Fioctl.
     An instance of FoundriesFactory—customized to your needs and machine—is a :term:`Factory`.

   Foundries.io
     Provider of FoundriesFactory® DevSecOps platform and the :term:`Linux microPlatform`\™ OS.
     `Website <https://foundries.io>`_.

   Factory
     An instance of :term:`FoundriesFactory` tailored to your device and needs.
     Created to support a specific machine.
     A Factory produces :term:`Target`\s.
     
     * :ref:`Account Management, Factory <account-management>`
     * :ref:`Creating, Factory <gs-signup>`
     * :ref:`Git repositories, Factory <ref-factory-sources>`
   
   Fioctl
     Factory management tool to interact with the Foundries.io REST API.
     Source code available via the `Fioctl GitHub repo <https://github.com/foundriesio/fioctl>`_.

     * :ref:`Installing, Fioctl <gs-install-fioctl>`
     * :ref:`Example use, Fioctl <ug-fioctl>`

   Aktualizr-lite
     Default Update agent for FoundriesFactory.

     * :ref:`Reference Manual, Aktualizr-lite <ref-aktualizr-lite>`
   
   Linux microPlatform  
   LmP
     The FoundriesFactory embedded Linux distro included in your Factory.
     Included via the ``meta-lmp`` Layer.
     Source code available via the `meta-lmp GitHub repo <https://github.com/foundriesio/meta-lmp>`_.
     
     * :ref:`Reference Manual, LmP <ref-linux>`
     * :ref:`Updating, LmP <ref-linux-update>`
     * :ref:`Test plan, LmP <ref-lmp-testplan>`
     * :ref:`Customizing, LmP <tutorial-customizing-the-platform>`
     * :ref:`Porting, LmP <ref-pg>`

   Target
     A description of the software a device should run.
     This description is visible as metadata in :term:`targets.json`.
     Includes details such as OSTree Hash and Docker-Compose App URIs, but are arbitrary.

     * :ref:`Tutorial, Target <tutorial-creating-first-target>`

   Docker-Compose App
   Compose App
     Also referred to as app.
     A folder in :term:`containers.git`, containing a ``docker-compose.yml``.
     The name of this folder is the name of your Docker-Compose App.

     * :ref:`Tutorial, Compose Apps <tutorial-compose-app>`
     * :ref:`User Guide, Compose Apps <ref-compose-apps>`

   System Image
     The OS image produced by the Factory that is flashed to all devices.
     The build artifact is commonly named ``lmp-factory-image-<hardware-id>.wic.gz``

   ``factory-config.yml``
     A file in the :term:`ci-scripts.git` repository of the Factory which controls all configurable aspects of a Factory.
     Such as :ref:`ref-advanced-tagging`, :ref:`ug-container-preloading` and email alerts.

     * :ref:`Reference Manual, Factory Definition <ref-factory-definition>`

   ``targets.json``
     Part of `TUF Metadata <https://theupdateframework.com/metadata/>`_ that specifies what Targets are valid to install.
     You can view the summary with ``fioctl targets list``, or view in full with ``fioctl targets list --raw``

   ``MACHINE``
     The machine name, as configured in the Yocto Project meta-layer.
     Officially supported in FoundriesFactory if listed in :ref:`ref-linux-supported`.
   
   CA
   Certificate Authority
     Creates and signs certificates which certifies public keys.
     Frequently used by browsers.

     * :ref:`Root of Trust, Managing Factory PKI <root-of-trust>`

   CSR
   Certificate Signing Request
     Protocol to securely issue an X.509 certificate, if provided attributes.

     * :ref:`User Guide, Rotating Device Certificate <ref-cert-rotation-ug>`
     * :ref:`Security, Device Certificate Rotation <ref-cert-rotation>`
     * :ref:`User Guide, Device Gateway PKI <ref-device-gateway-pki-details>`
  
   Device Gateway
     Through which devices connect to OTA services.
     Configured with mutual TLS.
  
     * :ref:`Security, Device Gateway <ref-device-gateway>`
     * :ref:`Testing, Device Gateway Testing API <ref-fiotest>`
     * :ref:`Troubleshooting, Errors and Solutions <ref-ts-errors>`
     * :ref:`User Guide, Device Gateway PKI <ref-device-gateway-pki-details>`

   ECC
   Elliptic Curve Cryptography
     An approach in public-key cryptography based on elliptic curves over finite fields.
     This allows for smaller keys than otherwise, but with an equivalent security level.

     * :ref:`Security, Secure Element <ref-secure-element>`
     * :ref:`Security, StM32MP1 Secure boot <ref-secure-boot-stm32mp1>`
     * :ref:`Security, OP-TEE on the Versal Adaptive Computer Acceleration Platform <ref-tee-on-versal-acap>`

   ECIES
   Elliptic Curve Integrated Encryption Scheme
     Protocol to securely encrypt data using an EC public key that can only be decrypted by the private key owner.
     Used by FoundriesFactory to provision configuration changes to devices.

   Hardware Root of Trust
     The first step in a security process used to trust code; always trusted.
     Includes HSM/TPM and Secure Boot.

     * :ref:`Security, OP-TEE on the Versal Adaptive Computer Acceleration Platform <ref-tee-on-versal-acap>`

   HSM
   Hardware Security Module
     A physical device generally used for managing digital keys and encrypting and decrypting data.
     
     * :ref:`User Guide, LmP Device Auto Register <ug-lmp-device-auto-register>`
     * :ref:`OTA Reference Manual, OTA Architecture <ref-ota-architecture>`

   Key Agreement
     Symmetric key negotiation—definition of a shared secret—without having to transmit the key.

   Key Transport
     Symmetric key created by one party and transmitted to the other party as ciphertext.

   mTLS
     A mutual :term:`TLS` where both client and server must present an X.509 certificate to prove identity and authorize connection.
     This is how Factory devices talk to the device gateway for OTA.
     Compared to TLS, mTLS has the benefit of protecting intellectual property,
     but does not add more protection from device data manipulation.

     * :ref:`Device Gateway Reference Manual, Server TLS Certificate <tls-crt>`
     * :ref:`Security Reference Manual, FoundriesFactory Security Summary <ff-crypto-key-summary>`

   OAuth2
     The industry-standard protocol for authorization developed within the IETF OAuth Working Group.

   PKCS #11
   Public-Key Cryptography Standards # 11
     Defines an API for cryptographic tokens, implemented by OP-TEE.
     Supported for Factory PKI and storage of device keys.

     * :ref:`Secure Element TPM Reference Manual, PKCS #11 Support <ref-secure-element.tpm>`
     * :ref:`EdgeLock™ SE05x Reference Manual, Importing Secure Objects into PKCS #11 Tokens <ref-secure-element>`
     * :ref:`Linux Disk Encryption Reference Manual, PKCS #11 Tokens <howto-linux-disk-encryption>`
     * `TEE PKCS #11 Implementation (external) <https://github.com/OP-TEE/optee_os/tree/master/ta/pkcs11>`_
       
   PKI
   Public Key Infrastructure
     How digital certificates and keys relate to their owners and can be trusted.
     
     * :ref:`Device Gateway PKI User Guide, Device Gateway PKI <ref-device-gateway-pki-details>`
     * :ref:`Factory Account Roles User Guide, Factory PKI Management <ref-account-roles>`
     * :ref:`iMX Secure Boot Reference Manual, PKI tree <ref-secure-boot-imx-habv4>`
     * :ref:`Factory Registration Reference Manual, Device Gateway PKI <ref-factory-registration-ref>`

   Secure Boot
     Helps ensure only trusted software executes at boot.

     * :ref:`Security, Secure Boot <ref-secure-boot>`
     * :ref:`Security, UEFI Secure Boot <ref-secure-boot-uefi>`
     * :ref:`Security, Machines With Secure Boot <ref-secure-machines>` 

   Secure World
     Trusted Execution Environment (:term:`TEE`) on ARM.

   TEE
   OP-TEE
     Trusted Execution Environment.
     In general, a hardware based component where code can run.
     
     * :ref:`Porting Guide, including OP-TEE <ref-pg-spl-optee>`
     * :ref:`EdgeLock SE05x Reference Manual ,OP-TEE Use <ref-secure-element>`
     * :ref:`Factory Keys, OP-TEE Keys <ref-factory-keys>`
     
   TF-A
   Trusted Firmware-A
     Secure world software for Armv7-A and Armv8-A.

     * :ref:`Factory Keys, TF-A Keys <ref-factory-key-tfa>`

   TLS
   Transport Layer Security
     Cryptographic protocol for securing communication within a network.
     See-also: :term:`mTLS`

   TLS Handshake
     The procedure belonging to the :term:`TLS` protocol where the client and server agree on how to exchange information.

   TPM 2
   Trusted Platform Module 2.0 implementation
     A standard for a cryptoprocessor.
     Used to check platform integrity and to form a root of trust.

     * :ref:`Security, Trusted Platform Module <ref-secure-element.tpm>`

   TUF
   The Update Framework
     Open Source Framework and Specification used to help keep software update systems secure against different attack types.
     Uses its own keys.
     Also used for updating :term:`Fioctl`.
     See-also: :term:`Target`

     * :ref:`Account Management, Team Based Access and TUF Keys <team-based-access-tuf>`
     * :ref:`Custom CI User Guide, TUF Targets <ug-custom-ci-for-apps>`
     * :ref:`CI Targets Reference Manual, TUF Targets; TUF Metadata <ref-ci-targets>`
     * :ref:`Offline Updates, TUF Metadata; TUF Keys; TUF Repo; <ug-offline-update>`
     * :ref:`Reference Manual, Offline Factory TUF Keys <ref-offline-keys>`
     * :ref:`Crypto Key Summary, TUF Signing Keys <ff-crypto-key-summary>`
     * :ref:`Production Targets, TUF <ref-production-targets>`

   UEFI
   Unified Extensible Firmware Interface
     Standard which connects firmware for booting the hardware and operating system(s).
     Also defines :term:`Secure Boot`.

     * :ref:`Security, UEFI Secure Boot <ref-secure-boot-uefi>`
     * :ref:`Crypto Keys, UEFI Secure Boot Flow <ref-factory-keys>`
     * :ref:`Disk Encryption Support, UEFI Requirement; UEFI Support; UEFI Secure Boot <howto-linux-disk-encryption>`


   X.509
     An International Telecommunication Union (ITU) standard defining the format of public key certificates.
