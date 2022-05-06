
How to use custom keys
----------------------

Create the keys
^^^^^^^^^^^^^^^

There are different ways to create and store the needed keys for the secure
boot. One important reference to understand how to generate the PKI tree is
`i.MX Secure Boot on HABv4 Supported Devices`_ application note from NXP.

In addition, the U-Boot project also includes a documentation on `Generating a
fast authentication PKI tree`_.

.. warning:: It is critical that the keys created in this process must be stored
  in a secure and safe place. Once the keys are fused to the board and it is
  closed, that board will only boot signed images. So the keys are required in
  future steps.

Generate the MfgTools scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is a set of scripts to help with creating the set of commands used to fuse
the key into the fuse banks of ``<machine>``, and to close the board which
configures the board to only boot signed images.

1. Clone the ``lmp-tools`` from GitHub

.. prompt:: bash host:~$

      git clone git://github.com/foundriesio/lmp-tools.git

2. Export the path to where keys are stored

.. prompt:: bash host:~$

    export KEY_FILE=/path-to-key-files/<efusefile>

3. Generate the script to fuse the board

.. prompt:: bash host:~$

      ./lmp-tools/security/<soc>/gen_fuse.sh -s $KEY_FILE -d ./fuse.uuu

4. Generate the script to close the board

.. prompt:: bash host:~$

      ./lmp-tools/security/<soc>/gen_close.sh -s $KEY_FILE -d ./close.uuu

5. Install the scripts to the ``meta-subscriber-overrides``:

.. prompt:: bash host:~$

      mkdir -p <factory>/meta-subscriber-overrides/recipes-support/mfgtool-files/mfgtool-files/<machine>
      cp fuse.uuu <factory>/meta-subscriber-overrides/recipes-support/mfgtool-files/mfgtool-files/<machine>
      cp close.uuu <factory>/meta-subscriber-overrides/recipes-support/mfgtool-files/mfgtool-files/<machine>
      cat <factory>/meta-subscriber-overrides/recipes-support/mfgtool-files/mfgtool-files_%.bbappend

The content of ``mfgtool-files_%.bbappend`` should be::

    FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

6. Inspect the changes and push it accordingly

.. prompt:: bash host:~$

      git status

The result of ``git status`` should look like::

      On branch devel
      Your branch is up to date with 'origin/devel'.

      Changes to be committed:
      (use "git restore --staged <file>..." to unstage)
          new file:   recipes-support/mfgtool-files/mfgtool-files/<machine>/close.uuu
          new file:   recipes-support/mfgtool-files/mfgtool-files/<machine>/fuse.uuu
          new file:   recipes-support/mfgtool-files/mfgtool-files_%.bbappend

The changes add the UUU scripts to the ``mfgtool-files`` artifacts of next
targets. Run the ``fuse.uuu`` and ``close.uuu`` to fuse the custom keys and
close the board, respectively.

.. warning:: The scripts ``fuse.uuu`` and ``close.uuu`` include commands which
  result is irreversible. The  scripts should be executed with caution and only
  after understanding its critical implications.

.. _i.MX Secure Boot on HABv4 Supported Devices: https://www.nxp.com/webapp/Download?colCode=AN4581&location=null
.. _Generating a fast authentication PKI tree: https://source.codeaurora.org/external/imx/uboot-imx/tree/doc/imx/habv4/introduction_habv4.txt?h=imx_v2020.04_5.4.70_2.3.0#n191
