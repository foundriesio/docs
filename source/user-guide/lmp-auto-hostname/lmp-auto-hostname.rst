.. _ug-lmp-auto-hostname:

Auto Hostname
=============

This section shows how to enable the ``lmp-auto-hostname`` recipe. This recipe customizes 
device hostnames at runtime, either by appending the **serial** number
from the device tree of the hardware, or the **mac address** to the hostname.

The recipe lmp-auto-hostname_ is provided by meta-lmp_ and can be added by 
customizing your ``meta-subscriber-overrides.git``.

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

       appends the serial number of the device.

       **Example Result:** ``raspberrypi4-64-100000008305bbc3``

    .. option:: mac

       appends the MAC address of a chosen network interface.

       **Example Result:** ``raspberrypi4-64-dca6321669ea``

.. confval:: LMP_HOSTNAME_NETDEVICE=<interface>
    :default: ``eth0``

    *if* using ``mac`` mode, provide the device network interface to retrieve
    a MAC address from.

    **Example Value:** ``eth0`` or ``wlan0``

Configuring the LmP Auto Hostname
---------------------------------

According to your needs, select the tab serial or MAC.

.. tabs::

   .. group-tab:: Serial
      
      Serial is configured by default in the ``lmp-auto-hostname`` recipe, 
      no need for extra changes.

      Add the ``recipes-samples/images/lmp-factory-image.bb`` file, commit and push:

      .. prompt:: bash host:~$, auto

          host:~$ git commit -m "lmp-auto-hostname: Adding recipe" recipes-samples/images/lmp-factory-image.bb
          host:~$ git push

   .. group-tab:: MAC

      Edit the ``conf/machine/include/lmp-factory-custom.inc`` file and add the variables:
      
      .. prompt:: bash host:~$, auto
      
          host:~$ gedit recipes-samples/images/lmp-factory-image.bb
      
      **conf/machine/include/lmp-factory-custom.inc**:
      
      .. prompt:: text
      
           LMP_HOSTNAME_MODE = "mac"
           LMP_HOSTNAME_NETDEVICE = "eth0"
      
      Add the changed files, commit and push:

      .. prompt:: bash host:~$, auto

          host:~$ git add recipes-samples/images/lmp-factory-image.bb
          host:~$ git add conf/machine/include/lmp-factory-custom.inc
          host:~$ git commit -m "lmp-auto-hostname: Adding recipe"
          host:~$ git push

The latest **Target** named ``platform-devel`` should be the CI job you just created.

When FoundriesFactory CI finishes all jobs, if your device is already registered, 
wait until the Over-the-Air update finishes, otherwise download and flash the image.

Testing Auto Hostname
---------------------

Log in to the device via SSH and check the new hostname right after ``fio@``.

Check also the file ``/etc/hostname`` to confirm the new hostname.

.. tabs::

   .. group-tab:: Serial
      
      .. prompt:: bash fio@raspberrypi3-64-51ca7875:~$
      
          cat /etc/hostname 
      
      **Example Output**:
      
      .. prompt:: text
      
           raspberrypi3-64-51ca7875
      
   .. group-tab:: MAC
      
      .. prompt:: bash fio@raspberrypi3-64-b827ebca7875:~$
      
          cat /etc/hostname 
      
      **Example Output**:
      
      .. prompt:: text
      
           raspberrypi3-64-b827ebca7875

.. _meta-lmp: https://github.com/foundriesio/meta-lmp/tree/master
.. _lmp-auto-hostname: https://github.com/foundriesio/meta-lmp/tree/master/meta-lmp-base/recipes-support/lmp-auto-hostname