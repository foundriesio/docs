.. _ug-container-preloading:

Container Preloading
====================

This section guides you to configure your ``platform`` images to preload Docker Compose Apps.

By default, the ``platform`` build creates an image to be flashed to a device that
doesn't include Docker Compose Apps. After installing the image and registering 
the device, ``aktualizr-lite`` downloads and runs the configured apps.

There are cases where having applications pre-loaded on the image can be useful, such as:

- Executing a Docker Compose App right after the first boot, even without internet or registering the device.
- Reducing network data usage during the Docker Image download.

.. note::

    Preloading container images will increase the size of the system image
    considerably, especially if the containers have not been optimally
    constructed.

    Refer to the official Docker documentation for best practices
    on writing Dockerfiles:
    https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

Prerequisites
-------------

In this guide, it is assumed you already have a ``container`` build with the ``shellhttpd`` enabled:

.. figure:: /_static/userguide/container-preloading/container-preloading-target.png
   :width: 900
   :align: center

   FoundriesFactory Containers Targets

Click on the latest ``container`` build to see more details.

This tutorial uses ``shellhttpd`` as a reference. Check the Apps available in 
your latest Containers build:

.. figure:: /_static/userguide/container-preloading/container-preloading-apps.png
   :width: 900
   :align: center

   Containers Target Apps

Configure the CI
----------------

Cloning CI Scripts Repository

Clone your ``ci-scripts`` repo and enter its directory:

.. prompt:: bash host:~$

    git clone https://source.foundries.io/factories/<factory>/ci-scripts.git
    cd ci-scripts

Edit the ``factory-config.yml`` file and add the configuration below:

.. prompt:: bash host:~$, auto

    host:~$ gedit factory-config.yml

**factory-config.yml**:

.. prompt:: text

      containers:
        preloaded_images:
         enabled: true
         shortlist: "shellhttpd"

- ``enabled`` -  Whether to produce an archive containing docker images as part of a container build trigger.
- ``shortlist`` - Defines the list of apps to preload. If it is not specified or its value is empty, then all Target's apps are preloaded.

Add the ``factory-config.yml`` file, commit and push:

.. prompt:: bash host:~$, auto

    host:~$ git commit -m "Configure shellhttpd as pre-load app" factory-config.yml
    host:~$ git push

Getting a New Image with Pre-loaded Containers
----------------------------------------------

From now on, every time a ``platform`` or ``containers`` build finishes, it will 
generate a ``.wic.gz`` file with the pre-loaded Docker Image.

Find your ``containers`` folder and trigger a new build.

.. prompt:: bash host:~$, auto

    host:~$ cd containers/
    host:~$ git commit --allow-empty  -m "Trigger new build"
    host:~$ git push

The latest **Target** named ``containers-devel`` should be the CI job you just created.

.. figure:: /_static/userguide/container-preloading/container-preloading-new-target.png
   :width: 900
   :align: center

   FoundriesFactory New Target

When FoundriesFactory CI finishes all jobs, click in the **Target**, find :guilabel:`Runs` and download the image:

.. figure:: /_static/userguide/container-preloading/container-preloading-image.png
   :width: 900
   :align: center

   FoundriesFactory New Containers Image

Flash the image and boot the device, next log in via SSH.

.. note::

    Some devices require additional artifacts to be flashed. In this case, download 
    the files from the latest ``platform`` build. For more information about how to 
    flash your device, read :ref:`ref-boards`.

Testing pre-loaded Image
------------------------

On your device, switch to root and list the files in the folder 
``/var/sota/compose-apps/<app>``.

.. prompt:: bash device:~$

    sudo su
    ls /var/sota/compose-apps/shellhttpd

**Example Output**:

.. prompt:: text

     Dockerfile  docker-build.conf  docker-compose.yml  httpd.sh

You can also use Docker to list all images available on the device:

.. prompt:: bash device:~$

    docker images --digests           

**Example Output**:

.. prompt:: text

     REPOSITORY                              TAG       DIGEST                                                                    IMAGE ID       CREATED        SIZE
     hub.foundries.io/userguide/shellhttpd   <none>    sha256:956f4247799317bc03c382fbf939c6ada64cd6df95dc438883724740a46b0577   89afcf805196   22 hours ago   5.34MB

For test purposes, it is possible to run the Docker Compose App using the command:

.. prompt:: bash device:~$

    cd /var/sota/compose-apps/shellhttpd
    docker-compose up -d

**Example Output**:

.. prompt:: text

     Starting shellhttpd_httpd_1 ... done

Verify the applications running on the device with the ``docker ps`` command:

.. prompt:: bash device:~$, auto

    device:~$ docker ps

**Example Output**:

.. prompt:: text

     CONTAINER ID   IMAGE                                   COMMAND                  CREATED              STATUS          PORTS                                       NAMES
     ccfda617194e   hub.foundries.io/userguide/shellhttpd   "/usr/local/bin/http…"   About a minute ago   Up 35 seconds   0.0.0.0:8080->8080/tcp, :::8080->8080/tcp   shellhttpd_httpd_1

Run ``wget`` to test the container:

.. prompt:: bash device:~$, auto

    device:~$ wget -qO- 127.0.0.1:8080

**Example Output**:

.. prompt:: text

     Hello world

Starting Compose Apps Automatically
-----------------------------------

To start the pre-loaded application automatically (after the boot and before 
the device registration when aktualizr-lite starts) you have to enable a systemd service 
responsible for it.

meta-lmp_ already has a recipe that launches pre-loaded apps after the device boots.

Clone your ``meta-subscriber-overrides.git`` repo and enter its directory:

.. prompt:: bash host:~$

    git clone -b devel https://source.foundries.io/factories/<factory>/meta-subscriber-overrides.git
    cd meta-subscriber-overrides

Edit the ``recipes-samples/images/lmp-factory-image.bb`` file and add the recipe to the ``CORE_IMAGE_BASE_INSTALL`` list:

.. prompt:: bash host:~$, auto

    host:~$ gedit recipes-samples/images/lmp-factory-image.bb

**recipes-samples/images/lmp-factory-image.bb**:

.. prompt:: text

     diff --git a/recipes-samples/images/lmp-factory-image.bb b/recipes-samples/images/lmp-factory-image.bb
     --- a/recipes-samples/images/lmp-factory-image.bb
     +++ b/recipes-samples/images/lmp-factory-image.bb
     @@ -30,6 +30,7 @@ CORE_IMAGE_BASE_INSTALL += " \
          networkmanager-nmcli \
          git \
          vim \
     +    compose-apps-early-start \
          packagegroup-core-full-cmdline-extended \
          ${@bb.utils.contains('LMP_DISABLE_GPLV3', '1', '', '${CORE_IMAGE_BASE_INSTALL_GPLV3}', d)} \
     "

Add the ``recipes-samples/images/lmp-factory-image.bb`` file, commit and push:

.. prompt:: bash host:~$, auto

    host:~$ git commit -m "compose-apps-early-start: Adding recipe" recipes-samples/images/lmp-factory-image.bb
    host:~$ git push

The latest **Target** named ``platform-devel`` should be the CI job you just created.

.. figure:: /_static/userguide/container-preloading/container-preloading-platform.png
   :width: 900
   :align: center

   FoundriesFactory New Platform Target

When FoundriesFactory CI finishes all jobs, click in the **Target**, find :guilabel:`Runs` and download the image:

.. figure:: /_static/userguide/container-preloading/container-preloading-platform-image.png
   :width: 900
   :align: center

   FoundriesFactory Platform Image

Flash the image and boot the device, next log via SSH.

Testing Auto Start
------------------

Using a second terminal, test your application using ``curl`` from any external 
device connected to the same network (e.g. your host machine: the same computer 
you use to access your device with ssh).

.. prompt:: bash host:~$, auto

    host:~$ #Example curl 192.168.15.11:8080
    host:~$ curl <device IP>:8080

**Example Output**:

.. prompt:: text

     Hello world

On your device, use the following command to list the ``compose-apps-early-start`` 
service:

.. prompt:: bash device:~$

    systemctl list-unit-files | grep enabled | grep compose-apps-early-start

**Example Output**:

.. prompt:: text

    compose-apps-early-start.service           enabled         enabled

Verify the ``compose-apps-early-start`` application status:

.. prompt:: bash device:~$, auto

    device:~$  systemctl status compose-apps-early-start

**Example Output**:

.. prompt:: text

     compose-apps-early-start.service - Ensure apps are configured and running as early>
          Loaded: loaded (/usr/lib/systemd/system/compose-apps-early-start.service; enabl>
          Active: active (exited) since Wed 2021-03-24 10:25:43 UTC; 5 months 17 days ago
         Process: 750 ExecStart=/usr/bin/compose-apps-early-start (code=exited, status=0/>
        Main PID: 750 (code=exited, status=0/SUCCESS)

For more information, read :ref:`ref-preloaded-images`.

.. _meta-lmp: https://github.com/foundriesio/meta-lmp/tree/master