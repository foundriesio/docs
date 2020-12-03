.. _ug-configure-lmp:

LmP Configuration 
=================

.. _ug-configure-lmp_container-preloading:

Container Preloading
--------------------

.. note:: 

    Preloading container images will increase the size of the system image
    considerably, especially if the containers have not been optimally
    constructed. 

    Refer to the official Docker documentation for best practices
    on writing Dockerfiles:

    https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

Container images can be preloaded onto a :term:`system image` to avoid the need
to pull these images from hub.foundries.io on the initial boot of a device. **The
device must still be registered in order to run these containers**.

Enable Preloading of Containers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable preloading, set ``containers.preload`` to ``true`` to the
:term:`factory-config.yml` of the Factory.

.. code-block:: yaml

   containers:
     preload: true

The :ref:`Factory Definition <def-containers>` contains more detailed
information on the possible options in this schema.

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

Customize device hostnames at runtime, either by appending the **serial** number
from the Device Tree of the hardware, or the **mac address** to the hostname.

How to Enable
"""""""""""""

.. toggle-header::
   :header: **Show details**

   Ensure you are inside of the :term:`meta-subscriber-overrides.git`
   repository directory.

   #. Populate the recipe variables in:
   
      **conf/machine/include/lmp-factory-custom.inc**
   
      .. code-block::
   
         LMP_HOSTNAME_MODE = "mac"
         LMP_HOSTNAME_NETDEVICE = "eth0"

   #. Add ``lmp-auto-hostname`` to the list of recipes/packages in:
   
      **recipes-samples/images/lmp-factory-image.bb**
   
      .. code-block::
         :emphasize-lines: 9
   
         CORE_IMAGE_BASE_INSTALL += " \
             lmp-auto-hostname \
             kernel-modules \
             networkmanager-nmtui \
             git \
             vim \
             packagegroup-core-full-cmdline-utils \
             packagegroup-core-full-cmdline-extended \
             packagegroup-core-full-cmdline-multiuser \
         "

    .. toggle-header::
       :header: **Show git diff**
    
       .. code-block:: 
 
          diff --git a/conf/machine/include/lmp-factory-custom.inc b/conf/machine/include/lmp-factory-custom.inc
          index b6344ef..028b76a 100644
          --- a/conf/machine/include/lmp-factory-custom.inc
          +++ b/conf/machine/include/lmp-factory-custom.inc
          @@ -1 +1,4 @@
          -# LMP factory specific customizations (either replace or extend options as defined by meta-lmp)
          \ No newline at end of file
          +# LMP factory specific customizations (either replace or extend options as defined by meta-lmp)
          +
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

|

Variables
"""""""""

.. confval:: LMP_HOSTNAME_MODE=<option>
    :default: ``serial``

    .. option:: serial

       appends the serial number of the device.
 
       **Example Result:** ``raspberrypi4-64-100000008305bbc3``

    .. option:: mac

       appends the mac address of a chosen network interface.
 
       **Example Result:** ``raspberrypi4-64-dca6321669ea``

.. confval:: LMP_HOSTNAME_NETDEVICE=<interface>
    :default: ``eth0``

    *if* using ``mac`` mode, choses what network interface on devices to retrieve
    a mac address from.

    **Example Value:** ``eth0`` or ``wlan0``

.. _ug-configure-lmp_lmp-device-auto-register:

lmp-device-auto-register
~~~~~~~~~~~~~~~~~~~~~~~~

.. warning:: 
   Do not use this recipe in production. This recipe is only intended for
   usage in a development environment, such as the ``devel`` branch of the
   Factory, or another branch you have created for development purposes.

Creates a systemd oneshot service that will automatically register a device on
first boot once it has internet connectivity. This is done by providing an API
Token that has **devices:create** scope.

How to Enable
"""""""""""""

.. toggle-header::
   :header: **Show details**
 
   Ensure you are inside of the :term:`meta-subscriber-overrides.git`
   repository directory.

   #. Create the required directory structure for this recipe::

        mkdir -p recipes-support/lmp-device-auto-register/lmp-device-auto-register

   #. Add ``lmp-device-auto-register`` to the list of recipes/packages in:
   
      **recipes-samples/images/lmp-factory-image.bb**
   
      .. code-block::
         :emphasize-lines: 9
   
         CORE_IMAGE_BASE_INSTALL += " \
             lmp-device-auto-register \
             kernel-modules \
             networkmanager-nmtui \
             git \
             vim \
             packagegroup-core-full-cmdline-utils \
             packagegroup-core-full-cmdline-extended \
             packagegroup-core-full-cmdline-multiuser \
         "
 
   #. Create your **api-token** file. Replace ``<YOUR_API_TOKEN>`` with a
      **devices:create** scoped token:
   
      **recipes-support/lmp-device-auto-register/lmp-device-auto-register/api-token**
   
      .. code-block::
   
         <YOUR_API_TOKEN>
 
   #. Give the recipe access to the **api-token** file via
      by adding to:
   
      **recipes-support/lmp-device-auto-register/lmp-device-auto-register.bbappend**
   
      .. code-block::
   
         FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"
 
    .. toggle-header::
       :header: **Show git diff**
    
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

|
 
Variables
"""""""""

There are no variables for this recipe.

.. _meta-lmp: https://github.com/foundriesio/meta-lmp/tree/master
.. _meta-lmp-base: https://github.com/foundriesio/meta-lmp/tree/master/meta-lmp-base
