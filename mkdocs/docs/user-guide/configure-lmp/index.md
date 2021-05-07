# LmP Configuration

## Container Preloading

Note

Preloading container images will increase the size of the system image
considerably, especially if the containers have not been optimally
constructed.

Refer to the official Docker documentation for best practices on writing
Dockerfiles:

<https://docs.docker.com/develop/develop-images/dockerfile_best-practices/>

Container images can be preloaded onto a `system image` to avoid the
need to pull these images from hub.foundries.io on the initial boot of a
device. **The device must still be registered in order to run these
containers**.

### Enable Preloading of Containers

To enable preloading, set `containers.preload` to `true` to the
`factory-config.yml` of the Factory.

    containers:
      preload: true

The `Factory Definition <def-containers>` contains more detailed
information on the possible options in this schema.

## Recipes

The following recipes are provided by
[meta-lmp](https://github.com/foundriesio/meta-lmp/tree/master) and are
available in the
[meta-lmp-base](https://github.com/foundriesio/meta-lmp/tree/master/meta-lmp-base)
layer which is included via `conf/bblayers.conf` in `lmp-manifest.git`
by default. These recipes provide advanced, configurable functionality
to the LmP.

### Enabling Recipes

This demonstration shows how to enable the lmp-auto-hostname recipe.
This same process can be followed for all of the other recipes described
on this page.

./demo/ug-configure-lmp-enable-recipe.cast

### lmp-auto-hostname

Customize device hostnames at runtime, either by appending the
**serial** number from the Device Tree of the hardware, or the **mac
address** to the hostname.

#### How to Enable

Ensure you are inside of the `meta-subscriber-overrides.git` repository
directory.

1.  Populate the recipe variables in:

    **conf/machine/include/lmp-factory-custom.inc**

        LMP_HOSTNAME_MODE = "mac"
        LMP_HOSTNAME_NETDEVICE = "eth0"

2.  Add `lmp-auto-hostname` to the list of recipes/packages in:

    **recipes-samples/images/lmp-factory-image.bb**

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

>     diff --git a/conf/machine/include/lmp-factory-custom.inc b/conf/machine/include/lmp-factory-custom.inc
>     index b6344ef..028b76a 100644
>     --- a/conf/machine/include/lmp-factory-custom.inc
>     +++ b/conf/machine/include/lmp-factory-custom.inc
>     @@ -1 +1,4 @@
>     -# LMP factory specific customizations (either replace or extend options as defined by meta-lmp)
>     \ No newline at end of file
>     +# LMP factory specific customizations (either replace or extend options as defined by meta-lmp)
>     +
>     +LMP_HOSTNAME_MODE = "mac"
>     +LMP_HOSTNAME_NETDEVICE = "eth0"
>     diff --git a/recipes-samples/images/lmp-factory-image.bb b/recipes-samples/images/lmp-factory-image.bb
>     index 0c46cef..6fb0980 100644
>     --- a/recipes-samples/images/lmp-factory-image.bb
>     +++ b/recipes-samples/images/lmp-factory-image.bb
>     @@ -14,6 +14,7 @@ require recipes-samples/images/lmp-feature-sbin-path-helper.inc
>      IMAGE_FEATURES += "ssh-server-openssh"
>
>      CORE_IMAGE_BASE_INSTALL += " \
>     +    lmp-auto-hostname \
>          kernel-modules \
>          networkmanager-nmtui \
>          git \
>     @@ -21,4 +22,4 @@ CORE_IMAGE_BASE_INSTALL += " \
>          packagegroup-core-full-cmdline-utils \
>          packagegroup-core-full-cmdline-extended \
>          packagegroup-core-full-cmdline-multiuser \
>     -"
>     \ No newline at end of file
>     +"

#### Variables

LMP\_HOSTNAME\_MODE=&lt;option&gt;

serial

appends the serial number of the device.

**Example Result:** `raspberrypi4-64-100000008305bbc3`

mac

appends the mac address of a chosen network interface.

**Example Result:** `raspberrypi4-64-dca6321669ea`

LMP\_HOSTNAME\_NETDEVICE=&lt;interface&gt;

*if* using `mac` mode, choses what network interface on devices to
retrieve a mac address from.

**Example Value:** `eth0` or `wlan0`

### lmp-device-auto-register

Warning

Do not use this recipe in production. This recipe is only intended for
usage in a development environment, such as the `devel` branch of the
Factory, or another branch you have created for development purposes.

Creates a systemd oneshot service that will automatically register a
device on first boot once it has internet connectivity. This is done by
providing an API Token that has **devices:create** scope.

#### How to Enable

Ensure you are inside of the `meta-subscriber-overrides.git` repository
directory.

1.  Create the required directory structure for this recipe:

        mkdir -p recipes-support/lmp-device-auto-register/lmp-device-auto-register

2.  Add `lmp-device-auto-register` to the list of recipes/packages in:

    **recipes-samples/images/lmp-factory-image.bb**

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

3.  Create your **api-token** file. Replace `<YOUR_API_TOKEN>` with a
    **devices:create** scoped token:

    **recipes-support/lmp-device-auto-register/lmp-device-auto-register/api-token**

        <YOUR_API_TOKEN>

4.  Give the recipe access to the **api-token** file via by adding to:

    **recipes-support/lmp-device-auto-register/lmp-device-auto-register.bbappend**

        FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

>     diff --git a/recipes-samples/images/lmp-factory-image.bb b/recipes-samples/images/lmp-factory-image.bb
>     index 0c46cef..491c71b 100644
>     --- a/recipes-samples/images/lmp-factory-image.bb
>     +++ b/recipes-samples/images/lmp-factory-image.bb
>     @@ -14,6 +14,7 @@ require recipes-samples/images/lmp-feature-sbin-path-helper.inc
>      IMAGE_FEATURES += "ssh-server-openssh"
>
>      CORE_IMAGE_BASE_INSTALL += " \
>     +    lmp-device-auto-register \
>          kernel-modules \
>          networkmanager-nmtui \
>          git \
>     @@ -21,4 +22,4 @@ CORE_IMAGE_BASE_INSTALL += " \
>          packagegroup-core-full-cmdline-utils \
>          packagegroup-core-full-cmdline-extended \
>          packagegroup-core-full-cmdline-multiuser \
>     -"
>     \ No newline at end of file
>     +"
>     diff --git a/recipes-support/lmp-device-auto-register/lmp-device-auto-register.bbappend b/recipes-support/lmp-device-auto-register/lmp-device-auto-      register.bbappend
>     new file mode 100644
>     index 0000000..72d991c
>     --- /dev/null
>     +++ b/recipes-support/lmp-device-auto-register/lmp-device-auto-register.bbappend
>     @@ -0,0 +1 @@
>     +FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"
>     diff --git a/recipes-support/lmp-device-auto-register/lmp-device-auto-register/api-token b/recipes-support/lmp-device-auto-register/lmp-device-auto-     register/api-token
>     new file mode 100644
>     index 0000000..2cf7f63
>     --- /dev/null
>     +++ b/recipes-support/lmp-device-auto-register/lmp-device-auto-register/api-token
>     @@ -0,0 +1 @@
>     +<YOUR_API_TOKEN>

#### Variables

There are no variables for this recipe.
