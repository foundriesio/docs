Going to Production
===================

Going to production requires several considerations. This document
can serve as both a guide and a checklist.

Cryptographic Keys
------------------
The first and most important thing to get right is taking ownership
of the Factory's cryptographic keys. It can't be stressed enough -
the keys created in these steps must be:

 * **Stored securely**
 * **Backed up securely**
 * **Duplicated**

   * in multiple places
   * on multiple mediums

At a minimum its suggested to have 3 copies of both a paper print
out and USB thumb drive copy of the credentials distributed in
3 different locations. These copies should be stored in a safe.

The keys that must be set up include:

 * TUF :ref:`offline <ref-offline-keys>` root and target keys
 * Device Gateway :ref:`PKI <ref-device-gateway>` keys
 * TODO Are Secure boot and Secure Element ready to link here?

Production Builds
-----------------
There are few things to think about for production builds and
manufacturing images.

Production images may want to restrict things such as:

 * Externally exposed network ports like SSH
 * Restrictions to remote logins

   * If remote logins are allowed (e.g. via WireGuard), should the
     sessions be restricted from the device's local area network?

 * How should remote authentication be managed? ``fio/fio`` should
   not be used as a production username/password.

Production images will likely want to have certain Docker Compose
Applications :ref:`preloaded <ref-preloaded-images>`.

Production builds will also need a way to auto-register devices
during :ref:`manufacturing <ref-factory-registration-ref>`.

Once a good production build has been created, the Factory needs to
populate the initial :ref:`production TUF targets
metadata<ref-production-targets>`.
