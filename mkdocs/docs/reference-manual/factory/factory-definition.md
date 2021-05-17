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

`notify.email.users`
: Comma separated list of addresses to email after each CI build.
: Type: comma separated strings matching the pattern `.*@.*`
: Default: Email of the account used to create the Factory
: Example: `foo@foo.com,bar@bar.com` 
: Required: Yes

`notify.email.failures_only`
: If set to `true` users will only be notified of CI failures.
: Type: boolean (`true | false`)
: Default: `false`
: Example: `true`
: Required: No 

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

`lmp.container_preload` 
: Whether to preload docker images into the system-image as part of a platform build via the archive built by `containers.preload`.
: Type: boolean (`true | false`)
: Default: value of `containers.preload`
: Example: `true`
: Required: No

`lmp.container.params.<environment_variable>`
: Environment variable to be passed into the LmP build.
: Type: string
: Default: N/A
: Example: `foo`
: Required: No

`lmp.machines`
: Specify the list of `Supported LmP Machines <ref-linux-supported>` to build for by their `MACHINE` name. A Factory's subscription is generally only good for a single machine.
: Type: list of Yocto `MACHINE` names.
: Default: Machine selected on web interface during Factory creation
: Example: 
    ```
    lmp:
      machines:
        - imx8mmevk
        - qemuriscv64
    ```
: Required: Yes

`lmp.image_type` 
: Set the LmP image type to produce by recipe name. For example, `lmp-mini-image`, `lmp-base-console-image` from [meta-lmp](https://github.com/foundriesio/meta-lmp/tree/master/meta-lmp-base/recipes-samples/images).
: Type: string
: Default: `lmp-factory-image` (from **recipes-samples/images/lmp-factory-image.bb** in your **meta-subscriber-overrides.git** repo)
: Example: `lmp-mini-image`
: Required: Yes

`lmp.ref_options.refs/heads/<branch>`
: Override options when specific git references are updated
: Type: dictionary
: Default: N/A
: Example:
    ```
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
    ```
: Required: No

`lmp.tagging.refs/heads/<branch>`
: Control how OTA_LITE tags are handled. See `ref-advanced-tagging` for more details.
: Type: list of tags in `- tag: <tag>` format
: Default: N/A
: Example:
    ```
    lmp:
      tagging:
        refs/heads/master:
          - tag: postmerge
        refs/heads/devel:
          - tag: devel
    ```
: Required: No

`lmp.mfg_tools`
: Do an OE build to produce manufacturing tooling for a given `MACHINE`. This is used to facilitate the manufacturing process and to ensure secure boot on devices. Currently **only NXP** tools are supported.
: Type: list of dictionaries
: Default: N/A
: Example:
    ```
    mfg_tools:
      - machine: imx8mmevk
          image_type: mfgtool-files
          params:
            DISTRO: lmp-mfgtool
            EXTRA_ARTIFACTS: "mfgtool-files.tar.gz"
    ```
: Required: No

`lmp.mfg_tools.*.image_type`
: Recipe to use to build mfg_tools.
: Type: string
: Default: `mfgtool-files` (from [meta-lmp-base/recipes-support/mfgtool-files/mfgtool-files\_0.1.bb](https://github.com/foundriesio/meta-lmp/blob/master/meta-lmp-base/recipes-support/mfgtool-files/mfgtool-files_0.1.bb))
: Example: `mfgtool-files`
: Required: Yes

`lmp.mfg_tools.*.params.<environment_variable>`
: Environment variable to be passed into the mfg_tools build. 
: Type: string
: Default: Environment variables to pass to the build.
: Example: `foo`
: Required: No

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

`containers.preload`
: Whether to produce an archive containing docker images as part of a container build trigger. This archive can then be used to preload docker containers into your system-image by setting `lmp.preload` to `true`. 
: Type: boolean (`true | false`)
: Default: `false`
: Example: `true`
: Required: No

`containers.assemble_system_image`: `<true|false>`  
: Whether to produce a system-image as part of container build triggers. The system-image will be available as an artifact in the `assemble-system-image` run step of builds produced with this option set to `true`.
: Type: boolean (`true | false`)
: Default: `false`
: Example: `true`
: Required: No

`containers.platforms`:
: Specify a list of architectures to build containers for. Containers are only built for the specified list.
: Type: list of processor architectures
: Default: 
    ```
    - arm
    - arm64
    - amd64
    ```
: Example:
    ```
    containers:
      platforms:
        - riscv64
        - amd64
    ```
: Required: No

`containers.tagging.refs/heads/<branch>`
: Control how OTA\_LITE tags are handled. See `ref-advanced-tagging` for more details.
: Type: list of tags in `- tag: <tag>` format
: Default: N/A
: Example:
    ```
      tagging:
        refs/heads/master:
          - tag: postmerge
    ```
: Required: No

