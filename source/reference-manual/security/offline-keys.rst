.. _ref-offline-keys:

Offline FoundriesFactory TUF Keys
=================================

FoundriesFactory uses TUF's multi-level key management strategy to secure software updates.  Part of this strategy utilizes roles to separate software update responsibilities.  By restricting each role's responsibilities or actions it's trusted to perform, the impact of a compromised role's key is minimized.

Even so, if a key were compromised, TUF provides a mechanism for reliably revoking keys: the root role. The root role exists to delegate trust to all other top-level roles used in the system.  TUF allows rotation of the root key in case it gets compromised.  Since key rotation is crucial to Factory security, it's important that the root key be highly secure as well.

To increase a root key's security further, it is encouraged that the Factory owner rotates it. Rotation will convert the root role's online-key, generated during the bootstrap of a Factory, to an offline key.

.. note:: By rotating the root key, the Factory owner also switches the Factory from a key produced and owned by Foundries.io to one where the Factory owner retains complete control of the root role and key.

Rotation
--------

Key rotation updates the keys that a FoundriesFactory fleet will trust.  It's recommended that every new Factory have its keys rotated for offline storage, but key rotation is also necessary in the event that keys have been compromised.  To do a rotation, the current root keys may be supplied to `fioctl`_ - a tool for managing a FoundriesFactory. When a Factory is created, Foundries.io sends a notification with the root keys of that Factory, like so::

    Your FoundriesFactory has been created and is ready for use.

    ...

    TUF key management requires that you keep a securely stored offline copy of
    your root credentials. In the event of an online key compromise, these offline
    keys will be used to securely rotate/replace the compromised key(s). You can
    download your keys *one time* from this URL:

       https://factory-keys.foundries.io/example/example.tgz

    Once downloaded, this file will be deleted from our system.


Provide fioctl with the path to the root key tar archive::

    fioctl keys rotate /absolute/path/to/example.tgz

.. note:: Key rotation requires the host have Docker installed and have access to the internet.
.. note:: Hardware security modules are not yet supported.

Fioctl will update the fleet's root of trust with newly RSA signed offline root keys.  In this way trust of a Factory's keys may be restored, ensuring secure updates keep flowing.

.. note:: Fioctl will update the offline keys at the path provided, ensure the necessary steps are taken to keep them stored securely.

.. _fioctl:
   https://github.com/foundriesio/fioctl
