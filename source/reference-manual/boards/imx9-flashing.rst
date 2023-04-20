.. tabs::

   .. group-tab:: Linux

      #. Verify target is present::

           $ lsusb | grep NXP
           Bus 001 Device 018: ID 1fc9:014e NXP Semiconductors OO Blank 93

         .. highlight:: none

         In this mode you will use the ``uuu`` tools to program the images to the eMMC. The USB
         ID may differ if a different SoC is used.

      #. Run the command below to program the LmP to the EMMC::

           $ sudo mfgtool-files-<machine-name>/uuu mfgtool-files-<machine-name>/full_image.uuu
             uuu (Universal Update Utility) for nxp imx chips -- libuuu_1.4.243-0-ged48c51

             Success 1    Failure 0


             1:92     6/ 6 [Done                                  ] FB: done

      #. Turn off the power.
      #. Put the board into run mode

   .. group-tab:: Windows

      #. Start the ``Device Manager``
      #. Select ``View``
      #. Select ``Devices by container``
      #. Verify a device like the following:

      .. figure:: /_static/boards/windows_verify.png
          :width: 600
          :align: center

      #. Run the command below to program the LmP to the EMMC::

           C:\Users\Someone> mfgtool-files-<machine-name>\uuu.exe mfgtool-files-<machine-name>\full_image.uuu
             uuu (Universal Update Utility) for nxp imx chips -- libuuu_1.4.243-0-ged48c51

             Success 1    Failure 0


             1:92     6/ 6 [Done                                  ] FB: done

      #. Turn off the power.
      #. Put the board into run mode
