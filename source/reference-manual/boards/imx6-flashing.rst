.. tabs::

   .. group-tab:: Linux

      1. Verify target is present::

           $ lsusb | grep Freescale
           Bus 002 Device 052: ID 15a2:0080 Freescale Semiconductor, Inc.

         .. highlight:: none

         In this mode you will use the ``uuu`` tools to program the images to the eMMC.
   
      #. Run the command below to program the LmP to the EMMC::

           $ sudo mfgtool-files-<machine_name>/uuu -pp 1 mfgtool-files-<machine_name>/full_image.uuu
           uuu (Universal Update Utility) for nxp imx chips -- libuuu_1.4.43-0-ga9c099a
           
           Success 1    Failure 0
           
           
           1:31     3/ 3 [=================100%=================] SDPV: jump
           2:31     8/ 8 [Done                                  ] FB: done

      #. Turn off the power.
      #. Put the board into run mode

   .. group-tab:: Windows

      #. Start the ``Device Manager``
      #. Select ``View``
      #. Select ``Devices by container``
      #. Verify a device like the following:

      .. figure:: /_static/boards/imx6_windows.png
          :width: 600
          :align: center

      #. Run the command below to program the LmP to the EMMC::

           C:\Users\Someone> mfgtool-files-<machine_name>\uuu.exe -pp 1 mfgtool-files-<machine_name>\full_image.uuu
           uuu (Universal Update Utility) for nxp imx chips -- libuuu_1.4.43-0-ga9c099a
           
           Success 1    Failure 0
           
           
           1:31     3/ 3 [=================100%=================] SDPV: jump
           2:31     8/ 8 [Done                                  ] FB: done

      #. Turn off the power.
      #. Put the board into run mode
