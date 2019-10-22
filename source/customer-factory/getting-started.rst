.. _ref-getting-started:

Getting Started
===============

To get started using the FoundriesFactory please follow the steps below:

Create an account
~~~~~~~~~~~~~~~~~

  Visit https://app.foundries.io and you can create an account with our system or use your existing Github or Google account.

Verify your email address
~~~~~~~~~~~~~~~~~~~~~~~~~

  When you create an account, an automated email is sent to you to verify your email. Follow the link in the email to verify your account.

Set your name for your profile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  This is an optional step, but will help us identify your account quickly if you require support.

  Login to https://app.foundries.io

   In the upper right corner, select **Preferences & Settings**.

   .. figure:: /_static/settings-pulldown.png
      :alt: Settings pulldown menu
      :align: center
      :width: 3in

      Settings pulldown menu

   From the left menu, select **Profile**.

   Enter your name, and select **Save Profile**

Create your factory
~~~~~~~~~~~~~~~~~~~

  From the navigation bar, select **Factories**.

   .. figure:: /_static/factories.png
      :alt: Factories Page
      :align: center
      :width: 3in

   Select the **Create Factory** button.

   .. figure:: /_static/create-factory.png
      :alt: Create a factory
      :align: center
      :width: 3in

   Enter a name for the factory, contact email, and brief description.

   .. figure:: /_static/factory-details.png
      :alt: Factory Details
      :align: center
      :width: 3in

   Then select the **Create Factory** button.

   You have now created a factory, however to enable this factory, you must purchase a subscription.


Purchase a factory subscription
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  You will now see a factory has been created.

   .. figure:: /_static/factory-more-info.png
      :alt: Factory Information
      :align: center
      :width: 3in

   Select the **i** icon to view information about your factory.

   Select the **Billing** tab.

   Add a **Billing Account**

   .. figure:: /_static/factory-add-account.png
      :alt: Factory Account
      :align: center
      :width: 3in

   Enter your payment details, and select **Add Account**

   Select the **Subscriptions** tab

   .. figure:: /_static/factory-subscriptions.png
      :alt: Factory Subscriptions
      :align: center
      :width: 3in

   Select **Add Subscription**

   Choose the **Personal** or **Enterprise** subscription.

   .. figure:: /_static/factory-subscription.png
      :alt: Factory Subscription
      :align: center
      :width: 3in

   Refer to https://foundries.io/pricing/ for details about each subscription.

   Select **Add Subscription** to enable your factory.


Factory Generation
~~~~~~~~~~~~~~~~~~
  It will take a few minutes for your factory to be created. You will recieved an email when it is ready for use. Please follow the rest of this guide once you have an operational factory.


Generate an access token
~~~~~~~~~~~~~~~~~~~~~~~~

  In the upper right corner, select **Preferences & Settings**.

   .. figure:: /_static/settings-pulldown.png
      :alt: Settings pulldown menu
      :align: center
      :width: 3in

      Settings pulldown menu

   From the left menu, select **Access Tokens**.

   .. figure:: /_static/access-tokens-link.png
      :alt: Access tokens link
      :align: center
      :width: 3in

      Link to access tokens

   Select **Create New Token**.

   Give the token a name and select **Create**.

   .. figure:: /_static/create-token-dialog.png
      :alt: Create token dialog
      :align: center
      :width: 3in

      Create token dialog

   On your host, create a file named ``.netrc`` *(note the leading .)* in
   your home directory, readable only by your user, with the following contents::

     machine source.foundries.io
     login <your access token>

Viewing Builds
~~~~~~~~~~~~~~ 

  Click the **Builds** icon the upper navigation bar to view your factory builds.

   .. figure:: /_static/builds-link.png
      :alt: Builds icon
      :align: center
      :width: 3in

      Link for CI builds

   This view will display the public Linux microPlatform builds, along with
   any continuous integration jobs defined in your factory.

   .. note::

     The continuous integration jobs in your factory are private to you and your
     organization.

   Find your factory build, it will be ``<myfactory>/lmp``. Select it.

   .. figure:: /_static/ci-links.png
      :alt: ci.foundries.io
      :align: center
      :width: 2in

      CI Projects list

   Click on the default raspberrypi3-64 build and download the
   ``lmp-factory-image-raspberrypi3-64.img.gz`` artifact.


Install your factory build
~~~~~~~~~~~~~~~~~~~~~~~~~~

  Now follow the instructions in :ref:`tutorial-linux` to install your factory build on a microSD card.

  Insert the SD card into the Raspberry Pi 3, connect Ethernet and apply power.
