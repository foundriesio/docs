.. _ug-lmp-device-auto-register:

Auto Register
=============

This section shows how to enable ``lmp-device-auto-register``.
This utility creates a systemd oneshot service that registers the device on first boot—once it has internet connectivity.
This is done by providing an API Token with **devices:create** scope.

.. warning::
   Do not use the API Token in production.
   They are intended only for usage in a development environment.
   For more information, read :ref:`ref-factory-registration-ref`.
   When close to production, do not hesitate to contact Foundries.io™ to discuss best practices for automatically registering devices.

The recipe for lmp-device-auto-register_ is provided by meta-lmp_ and can be added by customizing your ``meta-subscriber-overrides.git``.

Prerequisites
-------------

To follow this section, it is important to have:

- Completed the getting started guide up to :ref:`gs-flash-device`.

Creating Token
--------------

Go to `Tokens <https://app.foundries.io/settings/tokens>`_ and create a new **Api Token** by clicking on :guilabel:`+ New Token`.

Complete with a **Description** and the **Expiration date** and select :guilabel:`next`.

Select the :guilabel:`device:create` token and select your **Factory**.
You can later revoke this access and set up a new token once you are familiar with the :ref:`ref-api-access`.

.. figure:: /_static/userguide/lmp-device-auto-register/lmp-device-auto-register-token.png
   :width: 500
   :align: center

   Token for device creation access

Enabling Recipe
---------------

Clone your ``meta-subscriber-overrides.git`` and enter its directory:

.. prompt:: bash host:~$

    git clone https://source.foundries.io/factories/<factory>/meta-subscriber-overrides.git
    cd meta-subscriber-overrides

Edit ``recipes-samples/images/lmp-factory-image.bb``, adding the recipe to the ``CORE_IMAGE_BASE_INSTALL`` list:

.. code-block:: diff

     diff --git a/recipes-samples/images/lmp-factory-image.bb b/recipes-samples/images/lmp-factory-image.bb
     --- a/recipes-samples/images/lmp-factory-image.bb
     +++ b/recipes-samples/images/lmp-factory-image.bb
     @@ -30,6 +30,7 @@ CORE_IMAGE_BASE_INSTALL += " \
          networkmanager-nmcli \
          git \
          vim \
     +    lmp-device-auto-register \
          packagegroup-core-full-cmdline-extended \
          ${@bb.utils.contains('LMP_DISABLE_GPLV3', '1', '', '${CORE_IMAGE_BASE_INSTALL_GPLV3}', d)} \
     "

Configuring the LmP Auto Register
---------------------------------

Create the required directory structure for the recipe:

.. prompt:: bash host:~$, auto
   
   host:~$ mkdir -p recipes-support/lmp-device-auto-register/lmp-device-auto-register

Create the ``api-token`` file and replace ``<YOUR_API_TOKEN>`` with the scoped token created in the previous steps:

``recipes-support/lmp-device-auto-register/lmp-device-auto-register/api-token``:

::

    <YOUR_API_TOKEN>

Create ``lmp-device-auto-register.bbappend`` in order to give the recipe access to the ``api-token`` file.

``recipes-support/lmp-device-auto-register/lmp-device-auto-register.bbappend``:

::

    FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

Add the changed files, commit and push:

      .. prompt:: bash host:~$, auto

          host:~$ git add recipes-samples/images/lmp-factory-image.bb
          host:~$ git add recipes-support/lmp-device-auto-register/lmp-device-auto-register/api-token
          host:~$ git add recipes-support/lmp-device-auto-register/lmp-device-auto-register.bbappend
          host:~$ git commit -m "lmp-device-auto-register: Adding recipe"
          host:~$ git push

The latest Target should be the CI job you just created.

When the CI finishes, download and flash the image.

.. note::

  To get a better understanding of what is going on, one can look at the lmp-device-auto-register_ repo.
  The Systemd Service file and corresponding shell script can be customized, just like the API token file is being overwritten.

Additional Configuration
------------------------

Auto registration can use device tags and or a Hardware Security Module (HSM).
Additional configuration can be added by creating files in ``/etc/sota`` directory

Registering the device with a tag can be done by creating ``/etc/sota/tag`` file.
The file should contain only the tag.
Example ``tag`` file:

::

    postmerge

Registering the device using HSM can be done by creating ``/etc/sota/hsm`` file.
The file should contain the following contents:

::

    HSM_MODULE=</path/to/module>
    HSM_PI=<PIN value>
    HSM_SOPIN=<SO pin value>

Example ``hsm`` file for SE050 device

::

    HSM_MODULE="/usr/lib/libckteec.so.0"
    HSM_PI=87654321
    HSM_SOPIN=12345678

``lmp-device-auto-register`` recipe does not create these files.
They need to be created by the user either by amending the ``lmp-device-auto-register`` recipe,
or by creating a separate recipe.

Testing Auto Register
---------------------

After booting the new image—if connected to the internet—the device will automatically register to your Factory.
It should be visible by navigating to the `web interface <https://app.foundries.io/factories>`_ and selecting the **Devices** tab.

.. figure:: /_static/userguide/lmp-device-auto-register/lmp-device-auto-register-device.png
   :width: 900
   :align: center
   :alt: FoundriesFactory Device Auto Registered

On your device, use the following command to list the ``lmp-device-auto-register`` service:

.. prompt:: bash device:~$

    device:~$ systemctl list-unit-files | grep enabled | grep lmp-device-auto-register

::

    lmp-device-auto-register.service           enabled         enabled

Verify the ``lmp-device-auto-register`` application status:

.. prompt:: bash device:~$, auto

    device:~$  systemctl status lmp-device-auto-register

::

     lmp-device-auto-register.service - Script to auto-register device into Factory
     Loaded: loaded (/usr/lib/systemd/system/lmp-device-auto-register.service; enabled; vendor preset: enabled)
     Active: active (exited) since Sun 2021-09-12 17:34:06 UTC; 5min ago
     Process: 774 ExecStart=/usr/bin/lmp-device-auto-register (code=exited, status=0/SUCCESS)
     Main PID: 774 (code=exited, status=0/SUCCESS)

.. _meta-lmp: https://github.com/foundriesio/meta-lmp/tree/main
.. _lmp-device-auto-register: https://github.com/foundriesio/meta-lmp/tree/main/meta-lmp-base/recipes-support/lmp-device-auto-register
