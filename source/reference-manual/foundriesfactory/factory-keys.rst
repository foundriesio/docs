.. _ref-factory-keys:

The LmP keys and certificates used during the build of a FoundriesFactory
=========================================================================

LmP build system can use some online keys for signing some boot components of
the software stack. It can handle the U-Boot, OP-TEE, Linux Kernel image and
modules. The device RoT key (the key used for secure boot, for example) is not
listed here as it is not an online key and is not used during the
FoundriesFactory build.

When a FoundriesFactory is created, by default two set of keys are created under
``lmp-manifest`` repository. The key set under ``conf/keys`` is a copy of the
default LmP public keys. The set under ``factory-keys`` is created during the
FoundriesFactory creation and is unique for that Factory.

.. warning::

        FoundriesFactories created prior to **v83** do not have the ``factory-keys``
        directory with the set of keys and certificates. In this case, the commands
        can be used to create the files.

The directory structure shown below:

   .. parsed-literal::
        lmp-manifest/
        ├── conf
        │   ├── keys
        │   │   ├── dev.crt
        │   │   ├── dev.key
        │   │   ├── opteedev.crt
        │   │   ├── opteedev.key
        │   │   ├── privkey_modsign.pem
        │   │   ├── ubootdev.crt
        │   │   ├── ubootdev.key
        │   │   ├── x509.genkey
        │   │   └── x509_modsign.crt
        │   └── local.conf
        ├── factory-keys
        │   ├── opteedev.crt
        │   ├── opteedev.key
        │   ├── privkey_modsign.pem
        │   ├── ubootdev.crt
        │   ├── ubootdev.key
        │   └── x509_modsign.crt



A pair is composed by a certificate (``*.crt``) and a key (``*.key``) file.

The **dev** pair is a generic RSA 2048 key pair and is not in use.

The **opteedev** pair is a RSA 2048 key pair used for OP-TEE. This is used by
configuring the variable ``OPTEE_TA_SIGN_KEY``.

The **ubootdev** pair is a RSA 2048 key pair used for U-Boot. This is used by
configuring the variable ``UBOOT_SPL_SIGN_KEYNAME``.

The file ``x509.genkey`` is a configuration file used for creating
``privkey_modsign.pem`` and ``x509_modsign.crt`` which is a RSA 2048 pair in PEM
format, and is used for signing Linux Kernel Modules. This is used by
configuring the variable ``MODSIGN_PRIVKEY``.

Replacing the initial keys from factory
---------------------------------------

Each FoundriesFactory is created with a unique key set, however it is highly
recommended to rotate the keys as needed. The suggestion is to rotate them each
6 to 24 months.

.. warning::
  One of the aspects that can contribute to a secure system is to often rotate
  the used keys. So, it is highly recommended to rotate the keys each 6 to 24
  months.

.. tip::
  The file name for each key pair can be changed.

  The variables from ``<factory>/meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc``
  can be redefined to change filenames or paths, as needed. Those variables are shown below:


  .. prompt::

     MODSIGN_KEY_DIR = "${TOPDIR}/conf/factory-keys"
     UBOOT_SIGN_KEYDIR ?= "${TOPDIR}/conf/factory-keys"
     OPTEE_TA_SIGN_KEY ?= "${TOPDIR}/conf/factory-keys/opteedev.key"

  Some other variables can be added to that file in order to further customize
  the file name or path for the used keys:

  .. prompt::

     #filename for the key/certificate for kernel modules
     MODSIGN_PRIVKEY ?= "${MODSIGN_KEY_DIR}/privkey_modsign.pem"
     MODSIGN_X509 ?= "${MODSIGN_KEY_DIR}/x509_modsign.crt"

     #filename for U-Boot key/certificate
     UBOOT_SIGN_KEYNAME ?= "ubootdev"

In the next sections, the command line on how to create the key pair for U-Boot,
OP-TEE and Linux Kernel Modules. Assuming the ``lmp-manifest`` repository is
cloned inside ``<factory>`` directory.

U-Boot keys
"""""""""""

.. prompt:: bash host:~$

    cd <factory>/lmp-manifest/factory-keys
    openssl genpkey -algorithm RSA -out ubootdev.key \
            -pkeyopt rsa_keygen_bits:2048 \
            -pkeyopt rsa_keygen_pubexp:65537
    openssl req -batch -new -x509 -key ubootdev.key -out ubootdev.crt

OP-TEE keys
"""""""""""

.. prompt:: bash host:~$

    cd <factory>/lmp-manifest/factory-keys
    openssl genpkey -algorithm RSA -out opteedev.key \
            -pkeyopt rsa_keygen_bits:2048 \
            -pkeyopt rsa_keygen_pubexp:65537
    openssl req -batch -new -x509 -key opteedev.key -out opteedev.crt

Linux Kernel Modules keys
"""""""""""""""""""""""""

In order to create the key used by Linux Kernel to sign the modules a
configuration file is needed. The `Linux Kernel documentation`_ states
the parameters needed for the configuration file.

For example, create a new text file with the following content or customize as
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
        Don't forget to push the new keys to get it included in the next CI
        build.

.. _Linux Kernel documentation: https://www.kernel.org/doc/html/v5.0/admin-guide/module-signing.html