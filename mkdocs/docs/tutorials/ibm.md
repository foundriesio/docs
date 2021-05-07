# IBM Watson IoT

In this tutorial you will be guided through the process of setting up
your device. In this case a Raspberry Pi 3 - to IBM Watson IoT. By using
the IBM IoT container available on the
[extra-containers](https://github.com/foundriesio/extra-containers)
repo, together with your FoundriesFactory, you will learn how to connect
your device to the cloud with just a few simple commands. Before you
know it, data - like CPU and RAM usage - will be flowing through the IBM
Watson IoT, allowing you to easily integrate your device data with any
IBM Service.

Once you install your app, you just need to load one config file over
fioctl and the device will start to send important system information to
IBM Watson IoT. In this tutorial we’re assuming that you already have an
[IBM Watson IoT
Account](https://cloud.ibm.com/catalog/services/internet-of-things-platform)
and your Raspberry Pi 3 is already connected to your FoundriesFactory.

## IBM Configuration

For the purposes of this tutorial we will begin by completing the
necessary steps to configure IBM IoT and next we will configure and
enable the IBM IoT container using FoundriesFactory.

## Create your Resource

First, we need to create resource.

Go to: "[IBM Dashboard](https://cloud.ibm.com/)" page.

At the top right of the window, click on "Create resource".

> <figure>
> <img src="/_static/tutorials/ibm/createresource.png" class="align-center" style="width:10in" alt="Create Resource" /><figcaption aria-hidden="true">Create Resource</figcaption>
> </figure>

Search for "internet of things" and select the "Internet of Things
Platform" box.

> <figure>
> <img src="/_static/tutorials/ibm/iot.png" class="align-center" style="width:8in" alt="Internet of Things Platform" /><figcaption aria-hidden="true">Internet of Things Platform</figcaption>
> </figure>

On the next window make sure that the Lite (free) plan is selected and
click on the Create button.

> <figure>
> <img src="/_static/tutorials/ibm/create.png" class="align-center" style="width:10in" alt="Project Name" /><figcaption aria-hidden="true">Project Name</figcaption>
> </figure>

You should now see the "Internet of Things Platform-te" page.

Click on "Launch"

> <figure>
> <img src="/_static/tutorials/ibm/launch.png" class="align-center" style="width:10in" alt="Internet of Things Platform-te" /><figcaption aria-hidden="true">Internet of Things Platform-te</figcaption>
> </figure>

## Create Device

Now we are ready to create our first device. We are using the Raspberry
Pi 3B for our demonstration but you may use any LmP device for the rest
of this tutorial.

On the Browse Devices window click on the "Create a device" button.

> <figure>
> <img src="/_static/tutorials/ibm/create_device.png" class="align-center" style="width:10in" alt="Create a device" /><figcaption aria-hidden="true">Create a device</figcaption>
> </figure>

In the "Add Device" dialog, enter your "Device Type". In my case, I will
use: RPi3B

Enter your "Device ID". In my case, I will use: 0001

Click on "Next".

> <figure>
> <img src="/_static/tutorials/ibm/devicename.png" class="align-center" style="width:10in" alt="Add Device" /><figcaption aria-hidden="true">Add Device</figcaption>
> </figure>

In the "Device Information", all fields are optional. In my case, I will
complete at least model and location:

> <figure>
> <img src="/_static/tutorials/ibm/details.png" class="align-center" style="width:10in" alt="Device Information" /><figcaption aria-hidden="true">Device Information</figcaption>
> </figure>

In the "Security", we will use "Auto-Generated authentication token".

Click on "Next"

> <figure>
> <img src="/_static/tutorials/ibm/security.png" class="align-center" style="width:10in" alt="Auto-Generated authentication token" /><figcaption aria-hidden="true">Auto-Generated authentication token</figcaption>
> </figure>

Finally in the "Summary", click on "Finish"

> <figure>
> <img src="/_static/tutorials/ibm/summary.png" class="align-center" style="width:10in" alt="Add device summary" /><figcaption aria-hidden="true">Add device summary</figcaption>
> </figure>

After finishing the device creation, you will see important information.

Save the "Organization ID", "Device Type", "Device ID" and the
"Authentication Token"

## FoundriesFactory

## Cloning your repository

To interact with your FoundriesFactory you'll first need to download the
necessary repositories, change the code and send it back to the server.

First, navigate to [Foundries.io App](https://app.foundries.io/), find
your Factory and the source code.

> <figure>
> <img src="/_static/tutorials/ibm/gitfoundries.png" class="align-center" style="width:20in" alt="Device activation page" /><figcaption aria-hidden="true">Device activation page</figcaption>
> </figure>

Open the container repository and clone it on your host machine:

    # Ubuntu Host Machine
    $ mkdir getstartedvideo
    $ cd getstartevideo
    $ git clone https://source.foundries.io/factories/getstartedvideo/containers.git/
    $ cd containers

In order to enable IBM IoT app we will need to clone some files from our
reference repository:

    # Ubuntu Host Machine
    $ git remote add fio https://github.com/foundriesio/extra-containers.git
    $ git remote update
    $ git checkout remotes/fio/master -- ibm-iotsdk

Edit the docker compose app file and update the Factory name:

    # Ubuntu Host Machine
    $ vim ibm-iotsdk/docker-compose.yml

ibm-iotsdk/docker-compose.yml:

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

Add the changes to your Factory and wait for it to finish compiling your
app:

    # Ubuntu Host Machine
    $ git add ibm-iotsdk/
    $ git commit "Adding new ibm-iotsdk app"
    $ git push

<figure>
<img src="/_static/tutorials/ibm/build.png" class="align-center" style="width:8in" alt="Building App" /><figcaption aria-hidden="true">Building App</figcaption>
</figure>

## Enabling the App on your Device

In the following steps we assume you have your Raspberry Pi 3 with
Foundries.io’s LmP running and correctly registered to your Factory.

With [fioctl](https://github.com/foundriesio/fioctl), we will enable the
application "ibm-iotsdk" on your device registered with the name
**raspberrypi3**. For more information about how to register and enable
application, check the page `ref-configuring-devices`:

    # Ubuntu Host Machine
    # Configure the device to run the "ibm-iotsdk" app
    $ fioctl devices config updates raspberrypi3 --apps ibm-iotsdk --tags master

On your Raspberry Pi, you should receive the update soon. You can watch
the logs by running the following commands:

    # Ubuntu Host Machine
    $ ssh fio@raspberrypi3-64.local
    # Raspberry Pi 3 Target Machine
    $ sudo journalctl -f -u aktualizr-lite

## Debugging the IBM IoT Container APP

In your Raspberry Pi 3 you can check the running container and copy the
container ID:

    # Raspberry Pi 3 Target Machine
    $ docker ps

<figure>
<img src="/_static/tutorials/ibm/dockerps.png" class="align-center" style="width:6in" alt="docker ps" /><figcaption aria-hidden="true">docker ps</figcaption>
</figure>

With the container ID check the container logs:

    # Raspberry Pi 3 Target Machine
    $ docker logs -f 20a1ede9c146

<figure>
<img src="/_static/tutorials/ibm/dockerlogs.png" class="align-center" style="width:6in" alt="docker log" /><figcaption aria-hidden="true">docker log</figcaption>
</figure>

As you can see, IBM IoT app is waiting for config files to connect and
start sending data to the cloud.

## Config files

We need to send a file configuration to the device. Create a file with
some variables needed on the application.

Create a file "ibm.config" and copy the "Organization ID", "Device
Type", "Device ID" and the "Authentication Token" to the variables:

    # Ubuntu Host Machine
    $ mkdir config
    $ cd config
    $ vim ibm.config

ibm.config:

    WIOTP_IDENTITY_ORGID='rmboq4'
    WIOTP_IDENTITY_TYPEID='RPi3B'
    WIOTP_IDENTITY_DEVICEID='0001'
    WIOTP_AUTH_TOKEN=XXXXXXXXXX

Use fioctl to send the files to the device safely:

    # Ubuntu Host Machine
    $ fioctl devices config set homeassistant32 ibm.config="$(cat ibm.config)""

After some time, the files will be copied to the folder
"/var/run/secrets" on your device:

    # Raspberry Pi 3 Target Machine
    $ root@raspberrypi3:/home/prjs/ibm/config# ls /var/run/secrets/
    ibm.config

## Connect and send data to IBM IoT

As soon as the container finds the "ibm.config" file, it will
automatically start sending data to the IBM Watson IoT Cloud.

> <figure>
> <img src="/_static/tutorials/ibm/conected.png" class="align-center" style="width:12in" alt="IBM Watson IoT" /><figcaption aria-hidden="true">IBM Watson IoT</figcaption>
> </figure>

## Receiving data on IBM IoT core

Once the previews steps are complete you will be able to receive data
inside your IBM Watson IoT.

At your IoT Dashboard, find "Boards" in the left menu.

> <figure>
> <img src="/_static/tutorials/ibm/board.png" class="align-center" style="width:8in" alt="Boards" /><figcaption aria-hidden="true">Boards</figcaption>
> </figure>

Click on "Usage Overview" card.

> <figure>
> <img src="/_static/tutorials/ibm/cards.png" class="align-center" style="width:8in" alt="Usage Overview" /><figcaption aria-hidden="true">Usage Overview</figcaption>
> </figure>

Click on "Add New Card".

> <figure>
> <img src="/_static/tutorials/ibm/newcard.png" class="align-center" style="width:12in" alt="Add New Card" /><figcaption aria-hidden="true">Add New Card</figcaption>
> </figure>

In the "Create Card" dialog, select "Line chart".

> <figure>
> <img src="/_static/tutorials/ibm/linechart.png" class="align-center" style="width:6in" alt="Create Card dialog" /><figcaption aria-hidden="true">Create Card dialog</figcaption>
> </figure>

Select your device.

> <figure>
> <img src="/_static/tutorials/ibm/selectdevice.png" class="align-center" style="width:8in" alt="Select your device" /><figcaption aria-hidden="true">Select your device</figcaption>
> </figure>

In the "Create Line chart Card" select:

    Event: psutil
    Property: cpu
    Name: cpu
    Type: Number
    Unit: (empety)
    Min: 0
    Max: 100

Click on "Next"

> <figure>
> <img src="/_static/tutorials/ibm/psutils.png" class="align-center" style="width:6in" alt="Create Line chart Card" /><figcaption aria-hidden="true">Create Line chart Card</figcaption>
> </figure>

Select the chart size you prefer.

> <figure>
> <img src="/_static/tutorials/ibm/chartsize.png" class="align-center" style="width:6in" alt="Chart Size" /><figcaption aria-hidden="true">Chart Size</figcaption>
> </figure>

Finally, complete the chart name and click on "Submit"

> <figure>
> <img src="/_static/tutorials/ibm/chartname.png" class="align-center" style="width:6in" alt="Chart Size" /><figcaption aria-hidden="true">Chart Size</figcaption>
> </figure>

Now you can see your device CPU usage live in the chart.

> <figure>
> <img src="/_static/tutorials/ibm/chart.png" class="align-center" style="width:12in" alt="CPU Chart" /><figcaption aria-hidden="true">CPU Chart</figcaption>
> </figure>
