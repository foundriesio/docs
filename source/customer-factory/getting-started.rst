Getting Started
===============

To get started using the Foundries Factory please follow the steps below:

#. Login to https://app.foundries.io and generate an access token.

   In the upper right corner, select "Preferences & Settings".

   .. figure:: /_static/settings-pulldown.png
      :alt: Settings pulldown menu
      :align: center
      :width: 3in

      Settings pulldown menu

   From the left menu, select "Access Tokens".

   .. figure:: /_static/access-tokens-link.png
      :alt: Access tokens link
      :align: center
      :width: 3in

      Link to access tokens

   Select "Create New Token".

   Give the token a name, and select "Create".

   .. figure:: /_static/create-token-dialog.png
      :alt: Create token dialog
      :align: center
      :width: 3in

      Create token dialog

   On your host, create a file named `.netrc` *(note the leading .)* in
   your home directory, readable only by your user, with the following contents::

     machine source.foundries.io
     login <your access token>

#. Click the "Builds" icon the upper navigation bar to view your factory builds.

   .. figure:: /_static/builds-link.png
      :alt: Builds icon
      :align: center
      :width: 3in

      Link for CI builds

   This view will display the public Linux microPlatform builds, along with
   any continuous integration jobs defined in your factory.
   *Your factory’s continuous integration jobs are private to you and your
   organization. They cannot be accessed without authentication through
   https://app.foundries.io.*

   Find your factory build, it will be "<myfactory>/lmp". Select it.

   Click on the default raspberrypi3-64 build

   Download the `lmp-factory-image-raspberrypi3-64.img.gz` artifact.

#. Now follow the instructions in :ref:`tutorial-linux` to install your
   factory build on a microSD card.

#. Insert the SD card into the Raspberry Pi 3, connect ethernet and apply power.
