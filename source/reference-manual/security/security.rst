.. _ref-security:

Security
========

.. toctree::
   :maxdepth: 1

   secure-boot
   boot-software-updates
   ota-security
   secure-elements/index


Overview
--------

Security has multiple layers and dimensions. Such as:

 * How the operator manages keys for signing. This includes
   TUF key management for signing what can be installed. It also
   includes how boot firmware is signed so that the hardware boot ROM
   will trust it.

 * Device security - how devices store secure artifacts.

 * Connection security - how devices and cloud services trust each
   other.

TUF Security
------------

TUF_ is the mechanism by which the Foundries.io backend informs
devices what software they can run. The TUF targets.json_ includes
a software description that's pinned to secure hashes of all
components so that a device can know that it is running the correct
payload. TUF keys need to be managed by a customer :ref:`offline <ref-offline-keys>`
in order to generate :ref:`production targets <ref-production-targets>`.

.. _TUF:
   https://theupdateframework.com/

.. _targets.json:
   https://theupdateframework.com/metadata/

Secure Boot (Hardware Root of Trust)
------------------------------------

:ref:`Secure Boot <ref-secure-boot>` is the mechanism used to force a device to
only execute boot software that is signed by a certain set of keys. The
verification process and respective security functions are performed by the SoC
boot ROM, and these are the starting points for building a hardware root of
trust.

The SoC hardware security manual should be consulted for identifying the
supported key types and the signing process required for establishing the
hardware root of trust.

Device Security
---------------

Devices employ multiple mechanisms to achieve security. First, they
can take advantage of a :ref:`Hardware Security Element(HSM) <ref-secure-elements>`
to ensure secrets are store securely.

These secrets are then generated/used by a secure :ref:`provisioning
process <ref-factory-registration-ref>` that allows devices a safe way
to self-register with our cloud service.

Connection Security
-------------------

Connection security ties everything together. Devices and the
:ref:`device gateway <ref-ota-architecture>` use mutual TLS to establish
trust. We include a streamlined way to establish :ref:`PKI <ref-device-gateway>`
for each factory that works with the secure provisioning process
outlined above.
