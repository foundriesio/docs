.. _ug-lmp-auto-hostname:

Auto Hostname
=============

This section shows how to enable ``lmp-auto-hostname``.
This utility customizes a device's hostname at runtime, by appending it with either the **serial** number from the device tree, or the **mac address**.

The recipe for lmp-auto-hostname_ is provided by meta-lmp_ and can be added by customizing ``meta-subscriber-overrides.git``.

Adding the Recipe
-----------------

Clone your ``meta-subscriber-overrides.git`` repo and enter its directory:

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
     +    lmp-auto-hostname \
          packagegroup-core-full-cmdline-extended \
          ${@bb.utils.contains('LMP_DISABLE_GPLV3', '1', '', '${CORE_IMAGE_BASE_INSTALL_GPLV3}', d)} \
     "

LmP Auto Hostname Variables
---------------------------

The ``lmp-auto-hostname`` recipe can be configured through variables.

.. confval:: LMP_HOSTNAME_MODE=<option>
    :default: ``serial``

    .. option:: serial

       Appends the serial number of the device:

       ``raspberrypi4-64-100000008305bbc3``

    .. option:: mac

       Appends the MAC address of a chosen network interface.

       ``raspberrypi4-64-dca6321669ea``

.. confval:: LMP_HOSTNAME_NETDEVICE=<interface>
    :default: ``eth0``

    If using ``mac`` mode, provide the device network interface to retrieve a MAC address from:

    ``eth0`` or ``wlan0``

Configuring the LmP Auto Hostname
---------------------------------

Select the Serial or MAC tab below, according to your needs.

.. tabs::

   .. group-tab:: Serial
      
      Serial is configured by default in the ``lmp-auto-hostname`` recipe, no need for extra changes.
      Add the ``recipes-samples/images/lmp-factory-image.bb`` file, commit, and push:

      .. prompt:: bash host:~$, auto

          host:~$ git commit -m "lmp-auto-hostname: Adding recipe" recipes-samples/images/lmp-factory-image.bb
          host:~$ git push

   .. group-tab:: MAC

      Edit ``conf/machine/include/lmp-factory-custom.inc``, adding the variables:
      
      .. prompt:: bash host:~$, auto
      
          host:~$ gedit recipes-samples/images/lmp-factory-image.bb
      
      ::
      
           LMP_HOSTNAME_MODE = "mac"
           LMP_HOSTNAME_NETDEVICE = "eth0"
      
      Add the changed files, commit, and push:

      .. prompt:: bash host:~$, auto

          host:~$ git add recipes-samples/images/lmp-factory-image.bb
          host:~$ git add conf/machine/include/lmp-factory-custom.inc
          host:~$ git commit -m "lmp-auto-hostname: Adding recipe"
          host:~$ git push

The latest Target named ``platform-devel`` should be the CI job you just created.

If your device is already registered, when all jobs finish, wait until the Over-the-Air update completes.
Otherwise download and flash the image.

Testing Auto Hostname
---------------------

Log in to the device via SSH and check the new hostname (right after ``fio@``).
You can also check ``/etc/hostname`` to confirm the new hostname.

.. tabs::

   .. group-tab:: Serial
      
      .. prompt:: bash fio@raspberrypi3-64-51ca7875:~$
      
          cat /etc/hostname 
      
      ::
      
           raspberrypi3-64-51ca7875
      
   .. group-tab:: MAC
      
      .. prompt:: bash fio@raspberrypi3-64-b827ebca7875:~$
      
          cat /etc/hostname 
      
      ::
      
          raspberrypi3-64-b827ebca7875

.. _meta-lmp: https://github.com/foundriesio/meta-lmp/tree/main
.. _lmp-auto-hostname: https://github.com/foundriesio/meta-lmp/tree/main/meta-lmp-base/recipes-support/lmp-auto-hostname
