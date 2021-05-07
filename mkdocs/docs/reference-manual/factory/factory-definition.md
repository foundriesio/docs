# Factory Definition

Each Factory can be customized to control how CI handles it. This is
managed in the “Factory Definition” which is located in a factory’s
**ci-scripts.git** repository in the **factory-config.yml** file.

## notify

**`notify:` Section Example**

    notify:
      email:
        users: foo@foo.com,bar@bar.com
      failures_only: false

notify:  
email:  
users: `<email_1>,<email_2>,<...>`  
**Required:** Comma separated list of addresses to email after each CI
build.

failures\_only: `<true|false>`  
**Optional:** If set to `true` users will only be notified of CI
failures.

**Default:** `false`

## lmp

**`lmp:` Section Example**

    lmp:
      container_preload: true
      params:
        EXAMPLE_VARIABLE_1: hello_world
      machines:
        - imx8mmevk
      image_type: lmp-factory-image
      ref_options:
       refs/heads/devel:
         machines:
           - raspberrypi3-64
         params:
           IMAGE: lmp-mini
           EXAMPLE_VARIABLE_1: foo
      tagging:
        refs/heads/master:
          - tag: postmerge
        refs/heads/devel:
          - tag: devel
      mfg_tools:
        - machine: imx8mmevk
          image_type: mfgtool-files
          params:
            DISTRO: lmp-mfgtool
            EXTRA_ARTIFACTS: "mfgtool-files.tar.gz"

lmp:  
container\_preload: `<true|false>`  
**Optional:** Whether to preload docker images into the system-image as
part of a platform build via the archive built by `containers.preload`.

**Default:** `false`

**Inherits:** `containers.preload`

params:  
EXAMPLE\_VARIABLE\_1: `<value>`  
**Optional:** Define an arbitrary environment variable to be passed into
the LmP build. You can define as many as you want.

**Default:** This variable is user defined and does not exist unless
instantiated.

machines: `- <machine_1>` `- <machine_2>`  
**Required**: Specify the list of `Supported LmP Machines
<ref-linux-supported>` to build for by their `MACHINE` name. A Factory's
subscription is generally only good for a single machine.

**Default:** Set by user during `gs-signup`

image\_type:`<lmp_image_type>`  
**Optional:** Set the LmP image type to produce by recipe name. For
example, `lmp-mini-image`, `lmp-base-console-image` from
[meta-lmp](https://github.com/foundriesio/meta-lmp/tree/master/meta-lmp-base/recipes-samples/images).

**Default:** `lmp-factory-image` (from
**recipes-samples/images/lmp-factory-image.bb** in your
**meta-subscriber-overrides.git** repo)

ref\_options:  
refs/heads/`<branch>`:  
**Optional:** Override options when specific git references are updated

**Example:**

    # In the below example, when the branch named "devel" is built by our
    # CI system, it will have its option values for "machine" and
    # "params" overriden by what is specified after "refs/heads/devel:".
    # In the "devel" build, IMAGE will now equal "lmp-mini" rather than
    # "lmp-factory-image" as initially defined.

        lmp:
          params:
            IMAGE: lmp-factory-image
          machines:
            - imx8mmevk
          ref_options:
            refs/heads/devel:
              machines:
                - raspberrypi3-64
              params:
                IMAGE: lmp-mini

tagging:  
refs/heads/`<branch>`: `-tag: <tag>`  
**Optional:** Control how OTA\_LITE tags are handled. See
`ref-advanced-tagging` for more details.

mfg\_tools: `- machine: <machine>`  
**Optional:** Do an OE build to produce manufacturing tooling for a
given `MACHINE`. This is used to facilitate the manufacturing process
and to ensure secure boot on devices. Currently only NXP tools are
supported.\*\*

**Default:** None

image\_type: `<mfg_image_type>` **Optional:** Sets the name of the
recipe to use to build mfg\_tools.

**Default:** `mfgtool-files` (from
[meta-lmp-base/recipes-support/mfgtool-files/mfgtool-files\_0.1.bb](https://github.com/foundriesio/meta-lmp/blob/master/meta-lmp-base/recipes-support/mfgtool-files/mfgtool-files_0.1.bb))

## containers

**`containers:` Section Example**

    containers:
      preload: true
      assemble_system_image: false
      platforms:
        - arm
        - arm64
        - amd64
      tagging:
       refs/heads/master:
         - tag: postmerge
       refs/heads/devel-foundries:
         - tag: devel
       refs/heads/devel-foundries-base:
         - tag: devel-base
           inherit: devel

containers:  
preload: `<true|false>`  
**Optional:** Whether to produce an archive containing docker images as
part of a container build trigger. This archive can then be used to
preload docker containers into your system-image by setting
`lmp.preload` to `true`.

**Default:** `false`

**Inherits:** `lmp.preload`

assemble\_system\_image: `<true|false>`  
**Optional:** Whether to produce a system-image as part of container
build triggers. The system-image will be available as an artifact in the
`assemble-system-image` run step of builds produced with this option set
to `true`.

**Default:** `false`

platforms: `- arm` `- arm64` `- amd64`  
**Optional:** Specify a list of architectures to build containers for.
Containers are only built for the specified list.

**Default:** `amd64`

tagging:  
refs/heads/`<branch>`: `-tag: <tag>`  
**Optional:** Control how OTA\_LITE tags are handled. See
`ref-advanced-tagging` for more details.

**Default:** This variable does not exist unless instantiated.

provide a list of supported architectures for containers:

document DOCKER\_SECRETS

> &lt;br /&gt;
