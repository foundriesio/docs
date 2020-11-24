.. _ug-configure-lmp:

LmP Configuration 
=================

.. _ug-configure-lmp_recipes:

Recipes
-------

The following recipes are provided by meta-lmp_ and are available in the
meta-lmp-base_ layer which is included via ``conf/bblayers.conf`` in
:term:`lmp-manifest.git` by default. These recipes provide advanced,
configurable functionality to the LmP.

Enabling Recipes
~~~~~~~~~~~~~~~~

This demonstration shows how to enable the lmp-auto-hostname recipe. This same
process can be followed for all of the other recipes described on this page.

.. asciinema:: ./demo/ug-configure-lmp-enable-recipe.cast
   :rows: 24
   :cols: 100
   :speed: 1

.. _ug-configure-lmp_lmp-auto-hostname:

lmp-auto-hostname
~~~~~~~~~~~~~~~~~

.. sidebar:: How to Enable

   #. Populate the recipe variables in:
   
      **meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc**
   
      .. code-block::
   
         IMAGE_INSTALL_append = " lmp-auto-hostname" 
         LMP_HOSTNAME_MODE = "mac"
         LMP_HOSTNAME_NETDEVICE = "eth0"

   #. Add ``lmp-auto-hostname`` to the list of recipes/packages in:
   
      **meta-subscriber-overrides/recipes-samples/images/lmp-factory-image.bb**
   
      .. code-block::
         :emphasize-lines: 9
   
         CORE_IMAGE_BASE_INSTALL += " \
             kernel-modules \
             networkmanager-nmtui \
             git \
             vim \
             packagegroup-core-full-cmdline-utils \
             packagegroup-core-full-cmdline-extended \
             packagegroup-core-full-cmdline-multiuser \
             lmp-auto-hostname \
         "
   
   .. toggle-header::
      :header: **Click to show git diff**
   
      .. code-block:: 

         diff --git a/conf/machine/include/lmp-factory-custom.inc b/conf/machine/include/lmp-factory-custom.inc
         index b6344ef..77e83c1 100644
         --- a/conf/machine/include/lmp-factory-custom.inc
         +++ b/conf/machine/include/lmp-factory-custom.inc
         @@ -1 +1,5 @@
         -# LMP factory specific customizations (either replace or extend options as defined by meta-lmp)
         \ No newline at end of file
         +# LMP factory specific customizations (either replace or extend options as defined by meta-lmp)
         +
         +IMAGE_INSTALL_append = " lmp-auto-hostname"
         +LMP_HOSTNAME_MODE = "mac"
         +LMP_HOSTNAME_NETDEVICE = "eth0"
         diff --git a/recipes-samples/images/lmp-factory-image.bb b/recipes-samples/images/lmp-factory-image.bb
         index 0c46cef..6fb0980 100644
         --- a/recipes-samples/images/lmp-factory-image.bb
         +++ b/recipes-samples/images/lmp-factory-image.bb
         @@ -14,6 +14,7 @@ require recipes-samples/images/lmp-feature-sbin-path-helper.inc
          IMAGE_FEATURES += "ssh-server-openssh"
         
          CORE_IMAGE_BASE_INSTALL += " \
         +    lmp-auto-hostname \
              kernel-modules \
              networkmanager-nmtui \
              git \
         @@ -21,4 +22,4 @@ CORE_IMAGE_BASE_INSTALL += " \
              packagegroup-core-full-cmdline-utils \
              packagegroup-core-full-cmdline-extended \
              packagegroup-core-full-cmdline-multiuser \
         -"
         \ No newline at end of file
         +"   

Customize device hostnames at runtime, either by appending the **serial** number
from the Device Tree of the hardware, or the **mac address** to the hostname.

Variables
"""""""""

LMP_HOSTNAME_MODE
  What mode the recipe should operate in.

  **Values**
    ``mac``
      appends the mac address of a chosen network interface.

      **Example Result:** ``raspberrypi4-64-dca6321669ea``

    ``serial`` 
      appends the serial number of the device.

      **Example Result:** ``raspberrypi4-64-100000008305bbc3``

LMP_HOSTNAME_NETDEVICE
  *if* using ``mac`` mode, choses what network interface on devices to retrieve
  a mac address from.

  **Default:** ``eth0``

  **Example Value:** ``eth0`` or ``wlan0``

.. _ug-configure-lmp_lmp-device-auto-register:

lmp-device-auto-register
~~~~~~~~~~~~~~~~~~~~~~~~

.. sidebar:: How to Enable

   .. warning:: 
      Do not use this recipe in production. This recipe is only intended for
      usage in a development environment, such as the ``devel`` branch of the
      Factory, or another branch you have created for development purposes.

   #. Add ``lmp-device-auto-register`` to the list of recipes/packages in:
   
      **meta-subscriber-overrides/recipes-samples/images/lmp-factory-image.bb**
   
      .. code-block::
         :emphasize-lines: 9
   
         CORE_IMAGE_BASE_INSTALL += " \
             kernel-modules \
             networkmanager-nmtui \
             git \
             vim \
             packagegroup-core-full-cmdline-utils \
             packagegroup-core-full-cmdline-extended \
             packagegroup-core-full-cmdline-multiuser \
             lmp-device-auto-register \
         "

   #. Create your **api-token** file. Replace ``<YOUR_API_TOKEN>`` example with
      a **devices:create** scoped token:
   
      **recipes-support/lmp-device-auto-register/lmp-device-auto-register/api-token**
   
      .. code-block::
   
         <YOUR_API_TOKEN>

   #. Give the recipe access to the **api-token** file via
      by adding to:
   
      **meta-subscriber-overrides/recipes-support/lmp-device-auto-register/lmp-device-auto-register.bbappend**
   
      .. code-block::
   
         FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

    .. toggle-header::
       :header: **Click to show git diff**
    
       .. code-block:: 
    
          diff --git a/recipes-samples/images/lmp-factory-image.bb b/recipes-samples/images/lmp-factory-image.bb
          index 0c46cef..491c71b 100644
          --- a/recipes-samples/images/lmp-factory-image.bb
          +++ b/recipes-samples/images/lmp-factory-image.bb
          @@ -14,6 +14,7 @@ require recipes-samples/images/lmp-feature-sbin-path-helper.inc
           IMAGE_FEATURES += "ssh-server-openssh"
          
           CORE_IMAGE_BASE_INSTALL += " \
          +    lmp-device-auto-register \
               kernel-modules \
               networkmanager-nmtui \
               git \
          @@ -21,4 +22,4 @@ CORE_IMAGE_BASE_INSTALL += " \
               packagegroup-core-full-cmdline-utils \
               packagegroup-core-full-cmdline-extended \
               packagegroup-core-full-cmdline-multiuser \
          -"
          \ No newline at end of file
          +"
          diff --git a/recipes-support/lmp-device-auto-register/lmp-device-auto-register.bbappend b/recipes-support/lmp-device-auto-register/lmp-device-auto-      register.bbappend
          new file mode 100644
          index 0000000..72d991c
          --- /dev/null
          +++ b/recipes-support/lmp-device-auto-register/lmp-device-auto-register.bbappend
          @@ -0,0 +1 @@
          +FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"
          diff --git a/recipes-support/lmp-device-auto-register/lmp-device-auto-register/api-token b/recipes-support/lmp-device-auto-register/lmp-device-auto-     register/api-token
          new file mode 100644
          index 0000000..2cf7f63
          --- /dev/null
          +++ b/recipes-support/lmp-device-auto-register/lmp-device-auto-register/api-token
          @@ -0,0 +1 @@
          +<YOUR_API_TOKEN>

Creates a systemd oneshot service that will automatically register a device on
first boot once it has internet connectivity. This is done by providing an API
Token that has **devices:create** scope.
 
Variables
"""""""""

LMP_HOSTNAME_MODE
  What mode the recipe should operate in.

  **Values**
    ``mac``
      appends the mac address of a chosen network interface.

      **Example Result:** ``raspberrypi4-64-dca6321669ea``

    ``serial`` 
      appends the serial number of the device.

      **Example Result:** ``raspberrypi4-64-100000008305bbc3``

LMP_HOSTNAME_NETDEVICE
  *if* using ``mac`` mode, choses what network interface on devices to retrieve
  a mac address from.

  **Default:** ``eth0``

  **Example Value:** ``eth0`` or ``wlan0``

.. _meta-lmp: https://github.com/ricardosalveti/meta-lmp/tree/master
.. _meta-lmp-base: https://github.com/ricardosalveti/meta-lmp/tree/master/meta-lmp-base
