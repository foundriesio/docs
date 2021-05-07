Linux

1.  Verify target is present:

        $ lsusb | grep Freescale
        Bus 002 Device 052: ID 15a2:0080 Freescale Semiconductor, Inc.

    In this mode you will use the `uuu` tools to program the images to
    the eMMC.

2.  Run the command below to program the LmP to the EMMC:

        $ sudo mfgtool-files-<machine_name>/uuu -pp 1 mfgtool-files-<machine_name>/full_image.uuu
        uuu (Universal Update Utility) for nxp imx chips -- libuuu_1.4.43-0-ga9c099a

        Success 1    Failure 0


        1:31     3/ 3 [=================100%=================] SDPV: jump
        2:31     8/ 8 [Done                                  ] FB: done

3.  Turn off the power.

4.  Put the board into run mode

Windows

1.  Start the `Device Manager`
2.  Select `View`
3.  Select `Devices by container`
4.  Verify a device like the following:

<figure>
<img src="/_static/boards/imx6_windows.png" class="align-center" width="600" />
</figure>

1.  Run the command below to program the LmP to the EMMC:

        C:\Users\Someone> mfgtool-files-<machine_name>\uuu.exe -pp 1 mfgtool-files-<machine_name>\full_image.uuu
        uuu (Universal Update Utility) for nxp imx chips -- libuuu_1.4.43-0-ga9c099a

        Success 1    Failure 0


        1:31     3/ 3 [=================100%=================] SDPV: jump
        2:31     8/ 8 [Done                                  ] FB: done

2.  Turn off the power.

3.  Put the board into run mode
