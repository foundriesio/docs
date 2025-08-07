.. tab-set::
    :sync-group: os

   .. tab-item:: Linux
       :sync: linux

       #. Verify target is present:

          .. code-block:: console

             $ lsusb | grep NXP
             Bus 001 Device 018: ID 1fc9:014e NXP Semiconductors OO Blank 93

          In this mode you will use the ``uuu`` tools to program the images to the eMMC.
          The ``USB ID`` may differ if a different SoC is used.

       #. To program the LmP to the EMMC, run:

          .. code-block:: console

             $ sudo mfgtool-files-<machine-name>/uuu mfgtool-files-<machine-name>/full_image.uuu
             uuu (Universal Update Utility) for nxp imx chips -- libuuu_1.4.243-0-ged48c51

             Success 1    Failure 0


             1:92     6/ 6 [Done                                  ] FB: done

      #. Turn off the power
      #. Put the board into run mode.

   .. tab-item:: Windows
       :sync: windows

       #. Start the ``Device Manager``
       #. Select ``View``
       #. Select ``Devices by container``
       #. Verify a device like the following:

          .. figure:: /_static/boards/windows_verify.png
             :width: 600
             :align: center

       #. To program the LmP to the EMMC, run:

          .. code-block:: powershell

              PS C:\Users\Someone> mfgtool-files-<machine-name>\uuu.exe mfgtool-files-<machine-name>\full_image.uuu
              uuu (Universal Update Utility) for nxp imx chips -- libuuu_1.4.243-0-ged48c51

              Success 1    Failure 0


              1:92     6/ 6 [Done                                  ] FB: done

       #. Turn off the power
       #. Put the board into run mode.
