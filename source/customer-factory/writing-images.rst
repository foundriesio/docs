Writing Images to Persistent Storage Devices
============================================

Your factory image does not have an installation mechanism. However, it is
very easy to install manually. This section is only useful for devices which
have hard drives, eMMC, and/or flash parts.

Transfer your image to the target device, using http, scp, or other protocol, and ensure the image has been decompressed. To decompress it on target run the following command::

 gunzip -d lmp-factory-image-raspberrypi3-64.wic.gz

Next you need to determine which block device you would like to write the
image to. Typically, a combination of grepping through ``dmesg`` and
``ls -alh /dev | grep mmc`` does the trick.

Once you have determined the block device you would like to image, run a
command similar to the following *(replace mmcblkpX with your block device)*::

 dd if=/path/to/lmp-factory-image-raspberrypi3-64.wic \
     of=/dev/mmcblkpX bs=4m bs=4M iflag=fullblock \
     oflag=direct status=progress
 sync

After you have written the image to the persistent block device, reboot, and
remove the original media.
