.. highlight:: sh

.. _ref-linux-wic-installer:

WIC Image Installer
===================

 .. note::

  Only EFI compatible systems are currently supported by the image
  installer (e.g. intel-corei7-64).

To generate a WIC based image installer, switch the default ``WKS_FILE_sota``
definition for your target machine to ``image-efi-installer.wks``::

  $ cat meta-subscriber-overrides/conf/machine/include/lmp-factory-custom.inc
  WKS_FILE_intel-corei7-64_sota = "image-efi-installer.wks.in"

As WIC is only capable of consuming one single WKS file (even if multiple are
defined via WKS_FILES), this will force the build system to only generate
installer images by default.

Remove the custom ``WKS_FILE_sota`` override to restore back to the default
behavior and generate normal bootable WIC images
