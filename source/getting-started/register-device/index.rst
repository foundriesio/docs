.. _gs-register:

Registering Your Device
=======================

Your Linux® microPlatform (LmP) image includes the ``lmp-device-register`` tool that registers your device via the Foundries.io™ REST API.

1. Run this command from the device console to register it with your Factory:

 .. prompt:: bash device:~$, auto

      device:~$ sudo lmp-device-register -n <device-name>

.. note::

    **By default**, devices will run **all** applications that are defined in the :term:`containers.git` repository,
    thus available in the latest Target. This behavior can be changed by enabling only specific applications.
    Read :ref:`ug-fioctl-enable-apps` to learn how.

2. You will be prompted by ``lmp-device-register`` to `complete a challenge <https://www.oauth.com/oauth2-servers/device-flow/>`_ with our API:

   .. highlight:: none

   **Example Output**:

   .. prompt:: text

     Registering device, test, to factory gavin.
     Device UUID: df1295df-ba58-40a0-9239-542ded5ab934

     ----------------------------------------------------------------------------
     Visit the link below in your browser to authorize this new device. This link
     will expire in 15 minutes.
       Device Name: df1295ff-ba58-40a0-9239-542bed5ab964
       User code: SQRD-PLBN
       Browser URL: https://app.foundries.io/activate/

3. Your device is now registered and should be visible by navigating to the `web interface <https://app.foundries.io/factories/>`_ and selecting the **Devices** tab for your Factory. Or you can check by using :ref:`ref-fioctl`:

 .. prompt:: bash host:~$, auto

      host:~$ fioctl devices list
