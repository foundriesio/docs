.. _ref-factory-keys:

Crypto Keys Used by FoundriesFactory at Build Time
==================================================

By default, the LmP build system uses online keys to sign some boot components of
the software stack.

It can handle U-Boot, OP-TEE—which is a Trusted Execution Environment (TEE)—as
well as Linux® Kernel image and modules.

Secure Boot Flow
------------------

The secure boot flow starts from the boot ROM. After that step, the flow is
defined by the SoC vendor, as it depends on the architecture and the BSP they provide.

LmP implements three variations of boot flow, starting with Secondary Program Loader (SPL),
TF-A (BL2), or Unified Extensible Firmware Interface (UEFI).

The following diagrams show each boot flow with the related variable used
to configure the keys used by the Yocto Project.

.. note::

    The device RoT key (the key used for secure boot, for example) is shown in the diagrams.
    However it is not an online key and is not used during the Factory build.

i.MX Secure Boot Flow
"""""""""""""""""""""

The following diagram shows the Secure Boot flow for i.MX machines (TF-A is present only for arm64 devices):

.. graphviz::

   digraph {
        graph [
            label = "Secure Boot flow for i.MX machines"
        ];
        node [
            shape=box
        ];
        edge [
            arrowhead=none
        ];
        "Boot ROM"        -> "SPL"                               [label = "RoT key"];
        "SPL"             -> "uboot.itb"                         [label = "UBOOT_SPL_SIGN_KEYNAME"];
        "uboot.itb"       -> "bootscr"                           [label = "UBOOT_SPL_SIGN_KEYNAME"];
        "uboot.itb"       -> "TF-A (BL31, EL3 Runtime Firmware)" [label = "UBOOT_SPL_SIGN_KEYNAME"];
        "uboot.itb"       -> "OP-TEE"                            [label = "UBOOT_SPL_SIGN_KEYNAME"];
        "OP-TEE"          -> "OP-TEE TAs"                        [label = "OPTEE_TA_SIGN_KEY"];
        "uboot.itb"       -> "U-Boot proper"                     [label = "UBOOT_SPL_SIGN_KEYNAME"];
        "U-Boot proper"   -> "kernel fitImage"                   [label = "UBOOT_SIGN_KEYNAME"];
        "kernel fitImage" -> "DTB files"                         [label = "UBOOT_SIGN_KEYNAME"];
        "kernel fitImage" -> "initrd"                            [label = "UBOOT_SIGN_KEYNAME"];
        "kernel fitImage" -> "Linux kernel"                      [label = "UBOOT_SIGN_KEYNAME"];
        "Linux kernel"    -> "Linux kernel modules"              [label = "MODSIGN_PRIVKEY"];
   }

STM32MP15 Secure Boot Flow
""""""""""""""""""""""""""

The following diagram shows the Secure Boot flow for STM32MP15-based machines:

.. graphviz::

   digraph {
        graph [
            label = "Secure Boot flow for STM32MP15 based machines"
        ];
        node [
            shape=box
        ];
        edge [
            arrowhead=none
        ];
        "Boot ROM"           -> "TF-A (BL2)"            [label = "RoT key"];
        "TF-A (BL2)"         -> "fip.bin"               [label = "TF_A_SIGN_KEY_PATH"];
        "fip.bin"            -> "bootscr"               [label = "UBOOT_SIGN_KEYNAME"];
        "fip.bin"            -> "OP-TEE core (BL32)"    [label = "UBOOT_SIGN_KEYNAME"];
        "fip.bin"            -> "OP-TEE pager (BL32)"   [label = "UBOOT_SIGN_KEYNAME"];
        "fip.bin"            -> "OP-TEE pageable (BL32)" [label = "UBOOT_SIGN_KEYNAME"];
        "OP-TEE core (BL32)" -> "OP-TEE TAs"            [label = "OPTEE_TA_SIGN_KEY"];
        "fip.bin"            -> "u-boot-dtb"            [label = "UBOOT_SIGN_KEYNAME"];
        "fip.bin"            -> "U-Boot proper"         [label = "UBOOT_SIGN_KEYNAME"];
        "U-Boot proper"      -> "kernel fitImage"       [label = "UBOOT_SIGN_KEYNAME"];
        "kernel fitImage"    -> "DTB files"             [label = "UBOOT_SIGN_KEYNAME"];
        "kernel fitImage"    -> "initrd"                [label = "UBOOT_SIGN_KEYNAME"];
        "kernel fitImage"    -> "Linux kernel"          [label = "UBOOT_SIGN_KEYNAME"];
        "Linux kernel"       -> "Linux kernel modules"  [label = "MODSIGN_PRIVKEY"];
   }

UEFI Secure Boot Flow
"""""""""""""""""""""

The following diagram shows the Secure Boot flow (when booting with UEFI)
for ``intel-corei7-64`` based machines:

.. graphviz::

   digraph {
        graph [
            label = "Secure Boot flow for UEFI based machines"
        ];
        node [
            shape=box
        ];
        edge [
            arrowhead=none
        ];
        "Boot ROM"              -> "UEFI"                 [label = "RoT key"];
        "UEFI"                  -> "systemd-boot"         [label = "UEFI_SIGN_KEYDIR"];
        "systemd-boot"          -> "Linux kernel"         [label = "${UEFI_SIGN_KEYDIR}/DB.key"];
        "Linux kernel"          -> "Linux kernel modules" [label = "MODSIGN_PRIVKEY"];
   }

FoundriesFactory Keys
---------------------

When a Factory is created, by default, two sets of keys are created under
``lmp-manifest`` repository:

* ``conf/keys``: The key set is a copy of the default LmP public keys.
* ``factory-keys``: The key set is created during the Factory's creation
  and is unique for that Factory.

.. warning::

        FoundriesFactories created prior to **v83** do not have the ``factory-keys``
        directory with the set of keys and certificates. In this case, the commands
        can be used to create the files.

A pair comprises a certificate (``*.crt``) and a key (``*.key``) file.

The name of the key indicates by which component the **public** part of the key is used.

The **dev** pair is a generic ``RSA`` 2048 key pair and is not in use.

The **opteedev** pair is a ``RSA`` 2048 key pair by ``OP-TEE`` to validate trusted
applications run by ``OP-TEE``. This is used by configuring the variable ``OPTEE_TA_SIGN_KEY``.

The **ubootdev** pair is a ``RSA`` 2048 key pair by U-Boot proper to validate the
Linux Kernel. This is used by configuring the variable ``UBOOT_SIGN_KEYNAME``.

The **spldev** key pair is a ``RSA`` 2048 key pair used by U-Boot ``SPL`` to validate
``FIT`` image containing U-Boot and ``OP-TEE``.
This is used by configuring the variable ``UBOOT_SPL_SIGN_KEYNAME``.

The file ``x509.genkey`` is a configuration file used for creating
``privkey_modsign.pem`` and ``x509_modsign.crt`` and is used for signing Linux Kernel Modules.
This is used by configuring the variable ``MODSIGN_PRIVKEY``.

The **UEFI** certificates are detailed in :ref:`ref-secure-boot-uefi`.

The directory structure is shown below:

   .. parsed-literal::
        lmp-manifest/
        ├── conf
        │   ├── keys
        │   │   ├── dev.crt
        │   │   ├── dev.key
        │   │   ├── opteedev.crt
        │   │   ├── opteedev.key
        │   │   ├── privkey_modsign.pem
        │   │   ├── spldev.crt
        │   │   ├── spldev.key
        │   │   ├── tf-a
        │   │   ├── ubootdev.crt
        │   │   ├── ubootdev.key
        │   │   ├── uefi
        │   │   ├── x509.genkey
        │   │   └── x509_modsign.crt
        │   └── local.conf
        ├── factory-keys
        │   ├── opteedev.crt
        │   ├── opteedev.key
        │   ├── privkey_modsign.pem
        │   ├── spldev.crt
        │   ├── spldev.key
        │   ├── tf-a
        │   ├── ubootdev.crt
        │   ├── ubootdev.key
        │   ├── uefi
        │   └── x509_modsign.crt

How to Rotate the FoundriesFactory Keys
"""""""""""""""""""""""""""""""""""""""

Each Factory is created with a unique key set. However, it is highly
recommended to rotate the keys as needed. The suggestion is to rotate them every
6 to 24 months.

.. warning::
  One of the aspects that can contribute to a secure system is to rotate
  the used keys often. So, it is highly recommended to rotate the keys each 6 to 24
  months.

  Please note that, depending on the key, it may be required to trigger a :ref:`ref-boot-software-updates` to correctly change the Factory keys used. A mismatch in used keys could lead to devices failing to boot, which would then rollback to the previous stable version using the old keys.

In the following sections, the command line is shown on how to create the key pair for U-Boot,
OP-TEE and Linux Kernel Modules. This is assuming the ``lmp-manifest`` repository is
cloned inside ``<factory>`` directory.

U-Boot Keys
~~~~~~~~~~~

.. _ref-factory-key-ubootdev:

For ``ubootdev``:

.. prompt:: bash host:~$

    cd <factory>/lmp-manifest/factory-keys
    openssl genpkey -algorithm RSA -out ubootdev.key \
            -pkeyopt rsa_keygen_bits:2048 \
            -pkeyopt rsa_keygen_pubexp:65537
    openssl req -batch -new -x509 -key ubootdev.key -out ubootdev.crt

.. _ref-factory-key-spldev:

For ``spldev``:

.. prompt:: bash host:~$

    cd <factory>/lmp-manifest/factory-keys
    openssl genpkey -algorithm RSA -out spldev.key \
           -pkeyopt rsa_keygen_bits:2048 \
           -pkeyopt rsa_keygen_pubexp:65537
    openssl req -batch -new -x509 -key spldev.key -out spldev.crt

.. _ref-factory-key-opteedev:

OP-TEE Keys
~~~~~~~~~~~

.. prompt:: bash host:~$

    cd <factory>/lmp-manifest/factory-keys
    openssl genpkey -algorithm RSA -out opteedev.key \
            -pkeyopt rsa_keygen_bits:2048 \
            -pkeyopt rsa_keygen_pubexp:65537
    openssl req -batch -new -x509 -key opteedev.key -out opteedev.crt


.. _ref-factory-key-tfa:

TrustedFirmware-A Keys
~~~~~~~~~~~~~~~~~~~~~~

For TF-A keys:

.. prompt:: bash host:~$

    cd <factory>/lmp-manifest/factory-keys/tf-a
    openssl ecparam -name prime256v1 -genkey -noout -out privkey_ec_prime256v1.pem

.. tip::
        Remember to push the new keys to get them included in the next CI
        build.

.. _ref-factory-key-linux-module:

Linux Kernel Modules Keys
~~~~~~~~~~~~~~~~~~~~~~~~~

A configuration file is needed to create the key used by the Linux Kernel to sign
the modules. The `Linux Kernel documentation`_ states the parameters required
for the configuration file.

For example, create a new text file with the following content, or customize it as
needed:

.. prompt::

        [ req ]
        default_bits = 4096
        distinguished_name = req_distinguished_name
        prompt = no
        string_mask = utf8only
        x509_extensions = myexts

        [ req_distinguished_name ]
        #O = Unspecified company
        CN = Default insecure development key
        #emailAddress = unspecified.user@unspecified.company

        [ myexts ]
        basicConstraints=critical,CA:FALSE
        keyUsage=digitalSignature
        subjectKeyIdentifier=hash
        authorityKeyIdentifier=keyid

Or use the provided configuration file from
``<factory>/lmp-manifest/conf/keys/x509.genkey``
as shown in the following command:

.. prompt:: bash host:~$

    cd <factory>/lmp-manifest/factory-keys
    openssl req -new -nodes -utf8 -sha256 -days 36500 -batch -x509 \
            -config ../conf/keys/x509.genkey -outform PEM \
            -out x509_modsign.crt \
            -keyout privkey_modsign.pem

.. tip::
        Remember to push the new keys to get included in the next CI
        build.

.. tip::
  The file name for each key pair can be changed by changing variables from
  ``<factory>/meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc``
  as shown below:

  .. prompt::

     #filename for the key/certificate for kernel modules
     MODSIGN_PRIVKEY = "${MODSIGN_KEY_DIR}/privkey_modsign.pem"
     MODSIGN_X509 = "${MODSIGN_KEY_DIR}/x509_modsign.crt"

     # U-Boot signing key
     UBOOT_SIGN_KEYNAME = "ubootdev"

     # SPL / U-Boot proper signing key
     UBOOT_SPL_SIGN_KEYNAME = "spldev"

     # TF-A Trusted Boot
     TF_A_SIGN_KEY_PATH = "${TOPDIR}/conf/factory-keys/tf-a/privkey_ec_prime256v1.pem"

  This blog post shows how to identify which keys are being used during boot time: `How to read the boot logs to check the used keys`_.

.. _Linux Kernel documentation: https://www.kernel.org/doc/html/v5.0/admin-guide/module-signing.html
.. _How to read the boot logs to check the used keys: https://foundries.io/insights/blog/checking-log-secure/
