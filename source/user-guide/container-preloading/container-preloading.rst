.. _ug-container-preloading:

Container Preloading
====================

This section guides you to configure your ``platform`` images to preload Docker Compose Apps.

By default, the ``platform`` build creates an image to be flashed to a device that
doesn't include Docker Compose Apps. After installing the image and registering
the device, ``aktualizr-lite`` downloads and runs the configured apps.

There are cases where having applications preloaded on the image can be helpful, such as:

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
         app_type: <restorable|compose>
         shortlist: "shellhttpd"
         oe_builtin: <true|false>

- ``enabled`` -  Whether to produce an archive containing docker images as part of a container build trigger.
- ``shortlist`` - Defines the list of apps to preload. All Target's apps are preloaded if it is not specified or its value is empty.
- ``app_type`` - Defines a type of Apps to preload.
  If an option is not defined or set to an empty value, the ``app_type``  preload will depend on the LmP version. If the LmP version is equal to or higher than **v85**, then `restorable` type is preloaded, otherwise `compose` type.
  See :ref:`ug-restorable-apps` for more details on Restorable Apps.
- ``oe_builtin`` - Defines a way to accomplish preloading Apps. If the option is not defined or set to `false` (by default),
  then Apps are preloaded by the `assemble` run of a LmP CI build. Otherwise, Apps are preloaded during an OE build CI run.
  In this case, rootfs as well as a system image produced by the run includes preloaded Apps.
  Only `Restorable` type of Apps (default) are supported by the OE builtin preloader.
  This option does not work with some of the advanced tagging cases,
  e.g. in the case of multiple container builds using the same platform (see :ref:`ref-advanced-tagging` for more details).


Add the ``factory-config.yml`` file, commit and push:

.. prompt:: bash host:~$, auto

    host:~$ git commit -m "Configure shellhttpd as preload app" factory-config.yml
    host:~$ git push

Getting a New Image with Preloaded Containers
----------------------------------------------

After these steps, when a ``platform`` or ``containers`` build finishes, it will
generate a ``.wic.gz`` file in :guilabel:`Runs`, ``assembly-system-image`` , ``tag`` folder, with the preloaded Docker Image.

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

When FoundriesFactory CI finishes all jobs, click in the **Target**, find :guilabel:`Runs` and download the image from ``assemble-system-image``:

.. figure:: /_static/userguide/container-preloading/container-preloading-image.png
   :width: 900
   :align: center

   FoundriesFactory New Containers Image

Flash the image and boot the device, next log in via SSH.

.. note::

    Some devices require additional artifacts to be flashed.
    In this case, download the files from the latest ``platform`` build and only use the ``image`` from ``assembly-system-image``. 
    For more information about how to flash your device, read :ref:`ref-boards`.

Testing preloaded Image
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


Testing Preloaded Restorable Apps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On your device, switch to root and list the files in the folder
``/var/sota/reset-apps``.

.. prompt:: bash device:~$

    sudo su
    ls /var/sota/reset-apps/apps

Preloaded Restorable Apps should be listed in the output, provided that the preloading was successful.

**Example Output**:

.. prompt:: text

     app-05 app-07 app-08

Another option to verify whether Restorable Apps are preloaded is to use `aklite-apps` utility.

.. prompt:: bash device:~$

    sudo su
    aklite-apps ls

**Example Output**:

.. prompt:: text

     app-05
     app-07
     app-08

A user can try to start preloaded Restorable Apps manually by using `aklite-apps` utility.

.. prompt:: bash device:~$

    sudo su
    aklite-apps run [--apps <a comma separated list of Apps>]


Starting Compose Apps Automatically
-----------------------------------

To start the preloaded application automatically (after the boot and before
the device registration when aktualizr-lite starts) you have to enable a systemd service
responsible for it.

meta-lmp_ already has a recipe that launches preloaded apps after the device boots.

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
