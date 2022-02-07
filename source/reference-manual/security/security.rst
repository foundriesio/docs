.. _ref-security:

Security
========

.. toctree::
   :maxdepth: 2

   secure-boot
   boot-software-updates
   ota-security
   secure-elements/index


Overview
========

Security has multiple layers and dimensions. Such as:

 * How the operator manages keys for signing things. This includes
   TUF key management for signing what can be installed. It also
   includes how firmware is signed so that bootloaders will trust it.

 * Device security - how devices store secure artifacts.

 * Connection security - how devices and cloud services trust each
   other.

TUF Security
------------

TUF is the mechanism by which the Foundries.io backend informs
devices what software they can run. The TUF targets.json includes
a software description that's pinned to secure hashes of all
components so that a device can know that it's running the correct
payload. TUF keys need to be managed by a customer offline_ in order
to generate `production targets`_.

.. _offline:
   https://docs.foundries.io/latest/reference-manual/security/offline-keys.html

.. _production targets:
   https://docs.foundries.io/latest/reference-manual/ota/production-targets.html

Secure Boot
-----------

TODO

Device Security
---------------

Devices employ multiple mechanisms to achieve security. First, they
can take advantage of a `Hardware Security Element(HSM)`_ to ensure
secrets are store securely.

These secrets are then generated/used by a secure `provisioning
process`_ that allows devices a safe way to self-register with
our cloud service.

.. _Hardware Security Element(HSM):
   https://docs.foundries.io/latest/reference-manual/security/secure-elements/index.html

.. _provisioning process:
   https://docs.foundries.io/latest/reference-manual/security/factory-registration-ref.html

Connection Security
-------------------

Connection security ties everything together. Devices and the `device
gateway`_ use mutual TLS to establish trust. We include a stream
lined way to establish PKI_ for each factory that works with the
secure provisioning process outlined above.

.. _device gateway:
   https://docs.foundries.io/latest/reference-manual/ota/ota-architecture.html

.. _PKI:
   https://docs.foundries.io/latest/reference-manual/security/device-gateway.html
