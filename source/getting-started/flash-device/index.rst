Flash your Device |:cloud_lightning:|
=====================================

.. note::
   To follow this section, you will need:
    - A supported board that can boot from an SD Card.
     
      **(Raspberry Pi 3 of any variant, or a Raspberry Pi 4 recommended)**

    - A `suitable Micro SD Card <https://elinux.org/RPi_SD_cards>`_ to flash
      your LmP target build to.
    - Wired or WiFi network with internet access.

      - Ethernet cable (if choosing Wired)
      - 3.3 volt USB to TTL Serial Cable (if choosing WiFi)

Download LmP system image
-------------------------

When you trigger a build, it produces build artifacts as an output which can be
downloaded from the **Targets** tab of your factory, as described in
:ref:`ref-watch-build`.

1. Navigate to the **Targets** section of your Factory.
   
2. Find your LmP platform build, denoted by the **trigger name**:
   ``platform-<tag>``. 

   E.G: ``lmp-factory-image-raspberrypi3-64.wic.gz``

3. Download it by clicking on its name in the list of artifacts

.. figure:: /_static/flash-device/artifacts.png
   :width: 769
   :align: center

