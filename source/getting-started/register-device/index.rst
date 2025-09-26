.. _gs-register:

Registering Your Device
=======================

Your Linux® microPlatform (LmP) image includes the ``lmp-device-register`` tool that manages device registration for your device via the Foundries.io™ REST API.

1. To register a device with your Factory, run the following **from the device console**:

   .. code-block:: console

       device:~$ sudo lmp-device-register -n <device-name> -t main -f <factory>

   .. note::
      The parameters ``-t main -f <factory>`` are only needed for the first target.

2. You will be prompted by ``lmp-device-register`` to `complete a challenge <https://www.oauth.com/oauth2-servers/device-flow/>`_ with our API.
   Follow the instruction prompts:


   .. code-block:: none

     Registering device, test, to factory gavin.
     Device UUID: df1295df-ba58-40a0-9239-542ded5ab934

     ----------------------------------------------------------------------------
     Visit the link below in your browser to authorize this new device. This link
     will expire in 15 minutes.
       Device Name: df1295ff-ba58-40a0-9239-542bed5ab964
       User code: SQRD-PLBN
       Browser URL: https://app.foundries.io/activate/

3. Your device is now registered and should be visible by navigating to the `web interface <https://app.foundries.io/factories>`_ and selecting the :guilabel:`Devices` tab for your Factory:

   .. figure:: /_static/getting-started/register-device/tutorial-device-no-app.png
      :width: 900
      :align: center
      :alt: Devices view

      Device List


.. note::

    After registration, devices will run **all** applications that are available in the latest Target.
    This default behavior can be changed by enabling only specific applications.
    Read :ref:`ug-fioctl-enable-apps` to learn how.

.. seealso::
   :ref:`Team Based Factory Access <ref-team-based-access>` for permissions related to device management.
