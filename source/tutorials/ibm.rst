.. _ref-ibm:

IBM Watson IoT
==============

In this tutorial you will be guided through the process of setting up your device. In this case a Raspberry Pi 3 - to IBM Watson IoT. By using the IBM IoT container available on the `extra-containers`_ repo, together with your FoundriesFactory, you will learn how to connect your device to the cloud with just a few simple commands. Before you know it, data - like CPU and RAM usage - will be flowing through the IBM Watson IoT, allowing you to easily integrate your device data with any IBM Service.

Once you install your app, you just need to load one config file over fioctl and the device will start to send important system information to IBM Watson IoT.
In this tutorial we’re assuming that you already have an `IBM Watson IoT Account`_ and your Raspberry Pi 3 is already connected to your FoundriesFactory.

IBM Configuration
--------------------

For the purposes of this tutorial we will begin by completing the necessary steps to configure IBM IoT and next we will configure and enable the IBM IoT container using FoundriesFactory.

Create your Resource
--------------------

First, we need to create resource.

Go to: "`IBM Dashboard`_" page.

At the top right of the window, click on "Create resource".

   .. figure:: /_static/tutorials/ibm/createresource.png
      :alt: Create resource
      :align: center
      :width: 10in

      Create Resource

Search for "internet of things" and select the "Internet of Things Platform" box.


   .. figure:: /_static/tutorials/ibm/iot.png
      :alt: Internet of Things Platform
      :align: center
      :width: 8in

      Internet of Things Platform

On the next window make sure  that the Lite (free) plan is selected and click on the Create button.


   .. figure:: /_static/tutorials/ibm/create.png
      :alt: Project Name
      :align: center
      :width: 10in

      Project Name

You should now see the "Internet of Things Platform-te" page.

Click on "Launch"


   .. figure:: /_static/tutorials/ibm/launch.png
      :alt: Internet of Things Platform-te
      :align: center
      :width: 10in

      Internet of Things Platform-te


Create Device
-------------

Now we are ready to create our first device. We are using the Raspberry Pi 3B for our demonstration but you may use any LmP device for the rest of this tutorial.

On the Browse Devices window click on the "Create a device" button.

   .. figure:: /_static/tutorials/ibm/create_device.png
      :alt: Create a device
      :align: center
      :width: 10in

      Create a device

In the "Add Device" dialog, enter your "Device  Type". In my case, I will use: RPi3B

Enter your "Device ID". In my case, I will use: 0001

Click on "Next".


   .. figure:: /_static/tutorials/ibm/devicename.png
      :alt: Add Device
      :align: center
      :width: 10in

      Add Device

In the "Device Information", all fields are optional. In my case, I will complete at least model and location:


   .. figure:: /_static/tutorials/ibm/details.png
      :alt: Device Information
      :align: center
      :width: 10in

      Device Information

In the "Security", we will use "Auto-Generated authentication token".

Click on "Next"

   .. figure:: /_static/tutorials/ibm/security.png
      :alt: Auto-Generated authentication token
      :align: center
      :width: 10in

      Auto-Generated authentication token

Finally in the "Summary", click on "Finish"

   .. figure:: /_static/tutorials/ibm/summary.png
      :alt: Add Device Summary
      :align: center
      :width: 10in

      Add device summary

After finishing the device creation, you will see important information.

Save the "Organization ID", "Device Type", "Device ID" and the "Authentication Token"

FoundriesFactory
----------------

Cloning your repository
-----------------------

To interact with your FoundriesFactory you'll first need to download the necessary repositories, change the code and send it back to the server.

First, navigate to `Foundries.io App`_, find your Factory and the source code.

   .. figure:: /_static/tutorials/ibm/gitfoundries.png
      :alt: Device activation page
      :align: center
      :width: 20in

      Device activation page

Open the container repository and clone it on your host machine::

 # Ubuntu Host Machine
 $ mkdir getstartedvideo
 $ cd getstartevideo
 $ git clone https://source.foundries.io/factories/getstartedvideo/containers.git/
 $ cd containers

In order to enable IBM IoT app we will need to clone some files from our reference repository::

 # Ubuntu Host Machine
 $ git remote add fio https://github.com/foundriesio/extra-containers.git
 $ git remote update
 $ git checkout remotes/fio/master -- ibm-iotsdk

Edit the docker compose app file and update the Factory name::

 # Ubuntu Host Machine
 $ vim ibm-iotsdk/docker-compose.yml

ibm-iotsdk/docker-compose.yml::

 # ibm-iotsdk/docker-compose.yml
 version: "3"
 services:
   ibm-iotsdk:
     image: hub.foundries.io/<YOUR_FACTORY_NAME>/ibm-iotsdk:latest
     tmpfs:
         - /run
         - /var/lock
         - /var/log
     volumes:
         - /var/run/secrets:/config
     tty: true
     network_mode: "host"
     privileged: true
     restart: always


Add the changes to your Factory and wait for it to finish compiling your app::

 # Ubuntu Host Machine
 $ git add ibm-iotsdk/
 $ git commit "Adding new ibm-iotsdk app"
 $ git push

.. figure:: /_static/tutorials/ibm/build.png
    :alt: Building App
    :align: center
    :width: 8in

    Building App

Enabling the App on your Device
-------------------------------

In the following steps we assume you have your Raspberry Pi 3 with Foundries.io’s LmP running and correctly registered to your Factory.

With `fioctl`_, we will enable the application "ibm-iotsdk" on your device registered with the name **raspberrypi3**. For more information about how to register and enable application, check the page :ref:`ref-configuring-devices`::

 # Ubuntu Host Machine
 # Configure the device to run the "ibm-iotsdk" app
 $ fioctl devices config updates raspberrypi3 --apps ibm-iotsdk

On your Raspberry Pi, you should receive the update soon. You can watch the logs by running the following commands::

 # Ubuntu Host Machine
 $ ssh fio@raspberrypi3-64.local
 # Raspberry Pi 3 Target Machine
 $ sudo journalctl -f -u aktualizr-lite


Debugging the IBM IoT Container APP
--------------------------------------

In your Raspberry Pi 3 you can check the running container and copy the container ID::

 # Raspberry Pi 3 Target Machine
 $ docker ps


.. figure:: /_static/tutorials/ibm/dockerps.png
    :alt: docker ps
    :align: center
    :width: 6in

    docker ps

With the container ID check the container logs::

 # Raspberry Pi 3 Target Machine
 $ docker logs -f 20a1ede9c146

.. figure:: /_static/tutorials/ibm/dockerlogs.png
      :alt: docker log
      :align: center
      :width: 6in

      docker log

As you can see, IBM IoT app is waiting for  config files to connect and start sending data to the cloud.

Config files
------------

We need to send a file configuration to the device. Create a file  with some variables needed on the application.

Create a file "ibm.config" and copy the "Organization ID", "Device Type", "Device ID" and the "Authentication Token" to the  variables::

 # Ubuntu Host Machine
 $ mkdir config
 $ cd config
 $ vim ibm.config

ibm.config::

 WIOTP_IDENTITY_ORGID='rmboq4'
 WIOTP_IDENTITY_TYPEID='RPi3B'
 WIOTP_IDENTITY_DEVICEID='0001'
 WIOTP_AUTH_TOKEN=XXXXXXXXXX

Use fioctl to send the files to the device safely::

 # Ubuntu Host Machine
 $ fioctl devices config set homeassistant32 ibm.config="$(cat ibm.config)""

After some time, the files will be copied to the folder "/var/run/secrets" on your device::

 # Raspberry Pi 3 Target Machine
 $ root@raspberrypi3:/home/prjs/ibm/config# ls /var/run/secrets/
 ibm.config


Connect and send data to IBM IoT
-----------------------------------

As soon as the container finds the "ibm.config" file, it will automatically start sending data to the IBM Watson IoT Cloud.

   .. figure:: /_static/tutorials/ibm/conected.png
      :alt: Connecting with IBM Watson IoT
      :align: center
      :width: 12in

      IBM Watson IoT

Receiving data on IBM IoT core
---------------------------------

Once the previews steps are complete you will be able to receive data inside your IBM Watson IoT.

At your IoT Dashboard, find "Boards" in the left menu.

   .. figure:: /_static/tutorials/ibm/board.png
      :alt: Boards
      :align: center
      :width: 8in

      Boards

Click on "Usage Overview" card.

   .. figure:: /_static/tutorials/ibm/cards.png
      :alt: Usage Overview
      :align: center
      :width: 8in

      Usage Overview

Click on "Add New Card".

   .. figure:: /_static/tutorials/ibm/newcard.png
      :alt: Add New Card
      :align: center
      :width: 12in

      Add New Card

In the "Create Card" dialog, select "Line chart".

   .. figure:: /_static/tutorials/ibm/linechart.png
      :alt: Create Card dialog
      :align: center
      :width: 6in

      Create Card dialog

Select your device.

   .. figure:: /_static/tutorials/ibm/selectdevice.png
      :alt: Select your device
      :align: center
      :width: 8in

      Select your device

In the "Create Line chart Card" select::

 Event: psutil
 Property: cpu
 Name: cpu
 Type: Number
 Unit: (empety)
 Min: 0
 Max: 100

Click on "Next"

   .. figure:: /_static/tutorials/ibm/psutils.png
      :alt: Create Line chart Card
      :align: center
      :width: 6in

      Create Line chart Card

Select the chart size you prefer.

   .. figure:: /_static/tutorials/ibm/chartsize.png
      :alt: Chart Size
      :align: center
      :width: 6in

      Chart Size

Finally, complete the chart name and click on "Submit"

   .. figure:: /_static/tutorials/ibm/chartname.png
      :alt: Chart Size
      :align: center
      :width: 6in

      Chart Size

Now you can see your device CPU usage live in the chart.

   .. figure:: /_static/tutorials/ibm/chart.png
      :alt: CPU Chart
      :align: center
      :width: 12in

      CPU Chart


.. _extra-containers:
   https://github.com/foundriesio/extra-containers

.. _IBM Watson IoT Account:
   https://cloud.ibm.com/catalog/services/internet-of-things-platform

.. _IBM Dashboard:
   https://cloud.ibm.com/

.. _Foundries.io App:
   https://app.foundries.io/

.. _fioctl:
   https://github.com/foundriesio/fioctl



