# Building from Source

This is a guide for building the base Linux microPlatform (LmP) from
source for Raspberry Pi 3 (64-bit). Additional information specific to
other targets is provided in `ref-linux-supported`.

This guide assumes the reader is familiar with basic concepts of
OpenEmbedded. It is not meant to be an introduction to the OpenEmbedded
/ Yocto Project. If you're just getting started, it's strongly
recommended to begin with the documentation provided in
`ref-linux-building-ref`.

!!! Note

    Locally built images are useful for local development, testing and for
    hardware enablement, but are not meant to be updated via OTA. For OTA
    support we recommend creating your own Factory and using our
    continuous integration system.

## Get Hardware

You will need a x86 computer to develop on; Linux is currently natively
supported. On macOS and Windows, see `ref-linux-dev-container` for
information on setting up a containerized Linux build environment.

You will also require at least 50GB of storage for a complete Linux
microPlatform build.

## Set Up Build Environment

On Debian-based Linux distributions, including Ubuntu, run:

    $ sudo apt-get install coreutils gawk wget git-core diffstat unzip \
        texinfo g++ gcc-multilib build-essential chrpath socat cpio \
        openjdk-11-jre python2.7 python3 python3-pip python3-pexpect xz-utils \
        debianutils iputils-ping libsdl1.2-dev xterm libssl-dev libelf-dev \
        android-tools-fsutils ca-certificates repo whiptail

!!! Note

    If you are running Ubuntu 18.04, make sure to enable the universe
    repository by adding following line to your `/etc/apt/sources.list`:

        deb http://archive.ubuntu.com/ubuntu/ bionic universe

    On other Linux distributions, please check the [Yocto Project Quick
    Start
    Guide](https://www.yoctoproject.org/docs/current/brief-yoctoprojectqs/brief-yoctoprojectqs.html)
    for additional guidance.

## Install the Linux microPlatform

### Download the meta layers

The Linux microPlatform sources can be placed in any directory on your
workstation, as long it provides enough disk space for the complete
build. This uses the [Google
Repo](https://source.android.com/setup/develop/repo) tool to fetch a
variety of Git repositories at known-good revisions, and keep them in
sync as time goes on.

1.  Make an installation directory for the Linux microPlatform, and
    change into its directory:

        mkdir lmp && cd lmp

    (You can also reuse an existing installation directory, or
    `/build/lmp` if building inside the lmp-sdk container, as described
    at `ref-linux-dev-container`)

2.  Install update using repo:

        repo init -u <https://github.com/foundriesio/lmp-manifest> -b repo refs/tags/FIXME
        repo sync

### Set up Work Environment

Next, set up your work environment for building the source.

The supported `MACHINE` target used by this guide is `raspberrypi3-64`.
(For information on other hardware platforms, see
`ref-linux-supported`.)

The default distribution (`DISTRO`) is automatically set to `lmp`, which
is provided by the meta-lmp-base layer (see `ref-linux-layers` for more
details).

Set up your work environment using the `setup-environment` script:

    MACHINE=raspberrypi3-64 source setup-environment [BUILDDIR]

If `MACHINE` is not provided, the script will list all possible machines
found in every enabled OpenEmbedded / Yocto Project layer, and force one
to be selected. `BUILDDIR` is optional; if it is not specified, the
script will default to `build-lmp`.

### Build the lmp-base-console Image

You can build the Linux microPlatform base-console image by running:

    bitbake lmp-base-console-image

!!! Note

    Depending on the amount of RAM and number of processors and cores in
    your system, the speed of your Internet connection, and other factors,
    the first build could take several hours. Subsequent builds run much
    faster since some artifacts are cached.

At the end of the build, your build artifacts will be found under
`deploy/images/raspberrypi3-64`. The artifact you will use to flash your
board is `lmp-base-console-image-raspberrypi3-64.wic.gz`.

### Install the lmp-base-console Image

If you're using a Raspberry Pi 3, you can use the same procedure
outlined in `gs-flash-image`. See `ref-linux-supported` for additional
information on other targets.

## Install the LmP for your FoundriesFactory

In case you are already working with a FoundriesFactory, you can instead
download the source code for that factory with the following steps.

1.  Make an installation directory for the LmP for that
    `<factory-name>`, and change into its directory:

        mkdir <factory-name> && cd <factory-name>

2.  Install the `<factory-name>` meta layers using repo:

        repo init -u https://source.foundries.io/factories/<factory-name>/lmp-manifest.git -b devel -m <factory-name>.xml
        repo sync

    The manifest `<factory-name>.xml` refers to all the LmP meta layers
    and also to the `<factory-name>` specific repositories as described
    `ref-factory-sources`.

3.  Build the image for `<factory-name>`:

        MACHINE=<machine-name> source setup-environment [BUILDDIR]
        bitbake lmp-factory-image

    The variable `MACHINE` should be set to a supported machine. see the
    current available option in `ref-linux-supported`.)
    
    `BUILDDIR` is optional; in case it is not provided, script default is
    `build-lmp`.
    
    `lmp-factory-image` is the suggested default image, and can be
    customized with the steps from `ref-adding-packages-image`.
    
    It is worth remembering that the `bitbake` step can take a while.
    
    At the end of the build, your build artifacts is found under
    `deploy/images/<machine-name>`. The artifact you use to flash your
    board is `lmp-base-console-image-<machine-name>.wic.gz`.

    !!! Warning
    
        The local build of your FoundriesFactory is great for developing and
        debugging and the results can be used on the host machine or deployed to
        a hardware board.
    
        However, the image created locally is not yet visible for the OTA
        system, and is only available for local use.
        
        When you push the changes to the FoundriesFactory git repositories and
        trigger a new build you can flash and register your device following the
        instructions of `gs-flash-device` and `gs-register`. This way you can
        take full advantage of OTA system.

## References

The following reference material on OpenEmbedded and Yocto Project is
recommended for those new to either project.

- [OpenEmbedded wiki](https://www.openembedded.org/wiki/Main_Page)
- [Yocto Project main page](https://www.yoctoproject.org/)
- [Yocto Project Quick Start Guide](https://www.yoctoproject.org/docs/current/brief-yoctoprojectqs/brief-yoctoprojectqs.html)
- [Yocto Project Reference Manual](https://www.yoctoproject.org/docs/current/ref-manual/ref-manual.html)
- [BitBake Manual](https://www.yoctoproject.org/docs/current/bitbake-user-manual/bitbake-user-manual.html)

