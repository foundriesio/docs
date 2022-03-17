.. _ug-lmp-device-auto-register:

Auto Register
=============

This section shows how to enable the ``lmp-device-auto-register`` recipe. This
recipe creates a systemd oneshot service that will automatically register the
device on first boot once it has internet connectivity.
This is done by providing an API Token that has **devices:create** scope.

.. warning::
   Do not use the API Token in production. The use of an API Token is only intended for
   usage in a development environment. For more information, read
   :ref:`ref-factory-registration-ref`.
   As customers move closer to production, do not hesitate to contact Foundries.io
   to discuss the best practices to automatically register devices.

The recipe lmp-device-auto-register_ is provided by meta-lmp_ and can be added by
customizing your ``meta-subscriber-overrides.git``.

Prerequisites
-------------

To follow this section, it is important to have:

- Completed the :ref:`sec-learn` until the :ref:`gs-flash-device` section.

Creating Token
--------------

Go to `Tokens <https://app.foundries.io/settings/tokens/>`_ and create a new **Api Token** by clicking on
:guilabel:`+ New Token`.

Complete with a **Description** and the **Expiration date** and select :guilabel:`next`.

Select the :guilabel:`device:create` token and
select your **Factory**. You can later revoke this access and set up a new
token once you are familiar with the :ref:`ref-api-access`.

.. figure:: /_static/userguide/lmp-device-auto-register/lmp-device-auto-register-token.png
   :width: 500
   :align: center

   Token for device creation access

Enabling Recipe
---------------

Clone your ``meta-subscriber-overrides.git`` repo and enter its directory:

.. prompt:: bash host:~$

    git clone -b devel https://source.foundries.io/factories/<factory>/meta-subscriber-overrides.git
    cd meta-subscriber-overrides

Edit the ``recipes-samples/images/lmp-factory-image.bb`` file and add the recipe on the ``CORE_IMAGE_BASE_INSTALL`` list:

.. prompt:: bash host:~$, auto

    host:~$ gedit recipes-samples/images/lmp-factory-image.bb

**recipes-samples/images/lmp-factory-image.bb**:

.. prompt:: text

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

Create the required directory structure for this recipe:

.. prompt:: bash host:~$, auto

    host:~$ mkdir -p recipes-support/lmp-device-auto-register/lmp-device-auto-register

Create the ``api-token`` file and replace ``<YOUR_API_TOKEN>`` with the scoped token
created in the previous steps:

.. prompt:: bash host:~$, auto

    host:~$ gedit recipes-support/lmp-device-auto-register/lmp-device-auto-register/api-token

**recipes-support/lmp-device-auto-register/lmp-device-auto-register/api-token**:

.. prompt:: text

    <YOUR_API_TOKEN>


.. note::

   If the process of auto registration is following the fully detached mode, then API
   token filled here can be a bogus value. It only needs this because otherwise the
   ``lmp-device-register`` will try to do the OAuth flow still.

Create the file ``lmp-device-auto-register.bbappend`` in order to give the recipe
access to the ``api-token`` file.

.. prompt:: bash host:~$, auto

    host:~$ gedit recipes-support/lmp-device-auto-register/lmp-device-auto-register.bbappend

**recipes-support/lmp-device-auto-register/lmp-device-auto-register.bbappend**:

.. prompt:: text

    FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

Add the changed files, commit and push:

      .. prompt:: bash host:~$, auto

          host:~$ git add recipes-samples/images/lmp-factory-image.bb
          host:~$ git add recipes-support/lmp-device-auto-register/lmp-device-auto-register/api-token
          host:~$ git add recipes-support/lmp-device-auto-register/lmp-device-auto-register.bbappend
          host:~$ git commit -m "lmp-device-auto-register: Adding recipe"
          host:~$ git push

The latest **Target** named ``platform-devel`` should be the CI job you just created.

When FoundriesFactory CI finishes all jobs, download and flash the image.

.. note::

  To get a better understanding of what is going on, one can look at the repository
  lmp-device-auto-register_. In there is the Systemd Service file and the corresponding
  shell script that all can be customised just like the API token file is being overwritten.

Testing Auto Register
---------------------

After booting the new image, if connected to the internet, the device
will automatically register to your FoundriesFactory. It should be visible by navigating to the web
interface at https://app.foundries.io/factories/, clicking your **Factory** and
selecting the **Devices** tab.

.. figure:: /_static/userguide/lmp-device-auto-register/lmp-device-auto-register-device.png
   :width: 900
   :align: center

   FoundriesFactory Device Auto Registered

On your device, use the following command to list the ``lmp-device-auto-register``
service:

.. prompt:: bash device:~$

    systemctl list-unit-files | grep enabled | grep lmp-device-auto-register

**Example Output**:

.. prompt:: text

    lmp-device-auto-register.service           enabled         enabled

Verify the ``lmp-device-auto-register`` application status:

.. prompt:: bash device:~$, auto

    device:~$  systemctl status lmp-device-auto-register

**Example Output**:

.. prompt:: text

     lmp-device-auto-register.service - Script to auto-register device into Factory
          Loaded: loaded (/usr/lib/systemd/system/lmp-device-auto-register.service; enabled; vendor preset: enabled)
          Active: active (exited) since Sun 2021-09-12 17:34:06 UTC; 5min ago
         Process: 774 ExecStart=/usr/bin/lmp-device-auto-register (code=exited, status=0/SUCCESS)
        Main PID: 774 (code=exited, status=0/SUCCESS)

.. _meta-lmp: https://github.com/foundriesio/meta-lmp/tree/master
.. _lmp-device-auto-register: https://github.com/foundriesio/meta-lmp/tree/master/meta-lmp-base/recipes-support/lmp-device-auto-register
