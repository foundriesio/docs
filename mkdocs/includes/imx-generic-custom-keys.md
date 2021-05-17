## How to use custom keys

### Create the keys

There are different ways to create and store the needed keys for the
secure boot. One important reference to understand how to generate the
PKI tree is [i.MX Secure Boot on HABv4 Supported Devices]() application
note from NXP.

In addition, the U-Boot project also includes a documentation on
[Generating a fast authentication PKI tree]().

!!! Warning

    It is critical that the keys created in this process must be stored in a
    secure and safe place. When the keys are fused to the board, that board
    will only boot signed images. So the keys are required in future steps.

### Generate the MfgTools scripts

There is a set of scripts to help with creating the set of commands used
to fuse the key into the fuse banks of `<machine>`, and to close the
board which configures the board to only boot signed images.

1.  Clone the `lmp-tools` from GitHub

        host:~$ git clone <git://github.com/foundriesio/lmp-tools.git>

1.  Export the path to where keys are stored

        host:~$ export KEY\_PATH=/path-to-key-files

1.  Generate the script to fuse the board

        host:~$ cd lmp-tools/ cd security/imx6ull ./gen\_fuse.sh -s $KEY\_PATH

1.  Generate the script to close the board

        host:~$ cd lmp-tools/ cd security/imx6ull ./gen\_close.sh -s $KEY\_PATH

1.  Install the scripts to the `meta-subscriber-overrides`:

        host:~$ mkdir -p <factory>/meta-subscriber-overrides/recipes-support/mfgtool-files/mfgtool-files/<machine>
        host:~$ cp fuse.uuu <factory>/meta-subscriber-overrides/recipes-support/mfgtool-files/mfgtool-files/<machine>
        host:~$ cp close.uuu <factory>/meta-subscriber-overrides/recipes-support/mfgtool-files/mfgtool-files/<machine>
        host:~$ cat <factory>/meta-subscriber-overrides/recipes-support/mfgtool-files/mfgtool-files_%.bbappend

    The content of `mfgtool-files_%.bbappend` should be:

        FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

        SRC_URI_append_<machine> = " \
            file://fuse.uuu \
            file://close.uuu \
        "

        do_deploy_prepend_<machine>() {
            install -d ${DEPLOYDIR}/${PN}
            install -m 0644 ${WORKDIR}/fuse.uuu ${DEPLOYDIR}/${PN}/fuse.uuu
            install -m 0644 ${WORKDIR}/close.uuu ${DEPLOYDIR}/${PN}/close.uuu
        }

    !!! Tip

        Replace the machine name in case the factory is using a custom machine
        name.

1.  Inspect the changes and push it accordingly

        host:~$ git status

    The result of `git status` should look like:

        On branch devel
        Your branch is up to date with 'origin/devel'.

        Changes to be committed:
        (use "git restore --staged <file>..." to unstage)
            new file:   recipes-support/mfgtool-files/mfgtool-files/<machine>/close.uuu
            new file:   recipes-support/mfgtool-files/mfgtool-files/<machine>/fuse.uuu
            new file:   recipes-support/mfgtool-files/mfgtool-files_%.bbappend

    The changes add the UUU scripts to the `mfgtool-files` artifacts of next
    targets. Run the `fuse.uuu` and `close.uuu` to fuse the custom keys and
    close the board, respectively.

    !!! Warning

        The scripts `fuse.uuu` and `close.uuu` include commands which result is
        irreversible. The scripts should be executed with caution and only after
        understanding its critical implications.
