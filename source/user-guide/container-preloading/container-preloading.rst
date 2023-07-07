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

There are two ways to create these images:

 * :ref:`fioctl targets image<fioctl_targets_image>`
 * configuring ``ci-scripts`` to preload each build

Here we focus on the second approach so every Target includes a flashable image with preloaded containers.

Configure the CI
----------------

Clone your ``ci-scripts`` repo and enter its directory:

.. prompt:: bash host:~$

    git clone https://source.foundries.io/factories/<factory>/ci-scripts.git
    cd ci-scripts

Edit the ``factory-config.yml`` file and add the configuration below:

**factory-config.yml**:

.. prompt:: text

      containers:
        preloaded_images:
         enabled: true
         app_type: <restorable|compose>
         shortlist: "shellhttpd"
         oe_builtin: <true|false>

- ``enabled`` -  Whether to produce an archive containing docker images as part of a container build trigger.
- ``shortlist`` - Defines the list of apps to preload. All Target's apps are preloaded if it is not specified or its value is empty. Here, it is set to preload the ``shellhttpd`` app.
- ``app_type`` - Defines a type of Apps to preload.
  If an option is not defined or set to an empty value, the ``app_type``  preload will depend on the LmP version. If the LmP version is equal to or higher than **v85**, then `restorable` type is preloaded, otherwise `compose` type.
  See :ref:`ug-restorable-apps` for more details on Restorable Apps.
- ``oe_builtin`` - *Optional*: Preload Apps during an OE build CI run. Should be left disabled/undefined for most machines.

.. note::
   The ``oe_builtin`` is a special preloading case where Apps are preloaded during an OE build CI run, rather than preloaded by the `assemble` run of a LmP CI build. This is needed when the image produced by the LmP build is not a WIC image.

   In this case, rootfs as well as a system image produced by the run include preloaded Apps.

   Only `Restorable` type of Apps (default) are supported by the OE builtin preloader.

   This option does not work with some advanced tagging cases, e.g. multiple container builds using the same platform (see :ref:`ref-advanced-tagging` for more details).

Add the ``factory-config.yml`` file, commit and push:

.. prompt:: bash host:~$, auto

    host:~$ git commit -m "Configure shellhttpd as preload app" factory-config.yml
    host:~$ git push

Getting a New Image with Preloaded Containers
----------------------------------------------

After these steps, when a ``platform`` or ``containers`` build finishes, it will
generate a ``.wic.gz`` file in :guilabel:`Runs`, ``assemble-system-image`` , ``<tag>`` folder, with the preloaded Docker Images.

For example, pushing to ``containers-devel`` after this change triggers the usual build and an additional run called ``assemble-system-image``. Check the latest **Target** named ``containers-devel`` you just created:

.. figure:: /_static/userguide/container-preloading/container-preloading-new-target.png
   :width: 900
   :align: center

   FoundriesFactory New Target

When FoundriesFactory CI finishes all jobs, click in the **Target**, find :guilabel:`Runs` and download the image from ``assemble-system-image``:

.. figure:: /_static/userguide/container-preloading/container-preloading-image.png
   :width: 900
   :align: center

   FoundriesFactory New Containers Image

Flash the image and boot the device.

.. note::

    Some devices require additional artifacts to be flashed.
    In this case, download the files from the latest ``platform`` build and only use the ``image`` from ``assembly-system-image``. 
    For more information about how to flash your device, read :ref:`ref-boards`.

Checking the Preloaded Image
----------------------------

app_type: compose
~~~~~~~~~~~~~~~~~

On your device, switch to root and list the files in the folder
``/var/sota/compose-apps/<app>``. In this case the preloaded app is ``shellhttpd``.

.. prompt:: bash device:~$

    sudo su
    ls /var/sota/compose-apps/shellhttpd

.. prompt:: text

    Dockerfile  docker-build.conf  docker-compose.yml  httpd.sh

app_type: restorable
~~~~~~~~~~~~~~~~~~~~

Restorable apps are enabled by default on LmP v85+.

On your device, switch to root and list the files in the folder
``/var/sota/reset-apps``.

.. prompt:: bash device:~$

    sudo su
    ls /var/sota/reset-apps/apps

.. prompt:: text

     app-05 app-07 app-08

Preloaded Restorable Apps should be listed in the output, provided that the preloading was successful. In this case, the preloaded apps are ``app-05``, ``app-07`` and ``app-08``.

Another option to verify whether Restorable Apps are preloaded is to use `aklite-apps` utility.

.. prompt:: bash device:~$

    sudo su
    aklite-apps ls

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

To start the preloaded application automatically after the boot and before
the device registration when aktualizr-lite starts, you have to enable a systemd service
responsible for it.

meta-lmp_ provides a recipe that launches preloaded apps after the device boots.

Clone your ``meta-subscriber-overrides.git`` repo and enter its directory:

.. prompt:: bash host:~$

    git clone -b devel https://source.foundries.io/factories/<factory>/meta-subscriber-overrides.git
    cd meta-subscriber-overrides

Edit the ``recipes-samples/images/lmp-factory-image.bb`` file and add the recipe to the ``CORE_IMAGE_BASE_INSTALL`` list:

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

When FoundriesFactory CI finishes all jobs, click in the **Target**, find :guilabel:`Runs` and download the image from the ``assemble-system-image`` run:

.. figure:: /_static/userguide/container-preloading/container-preloading-platform-image.png
   :width: 900
   :align: center

   FoundriesFactory Platform Image

Flash the image and boot the device.

Testing Auto Start
------------------

On your device, use the following command to list the ``compose-apps-early-start``
service:

.. prompt:: bash device:~$

    systemctl list-unit-files | grep enabled | grep compose-apps-early-start

.. prompt:: text

    compose-apps-early-start.service           enabled         enabled

Verify the ``compose-apps-early-start`` application status:

.. prompt:: bash device:~$, auto

    device:~$  systemctl status compose-apps-early-start

.. prompt:: text

     compose-apps-early-start.service - Ensure apps are configured and running as early>
          Loaded: loaded (/usr/lib/systemd/system/compose-apps-early-start.service; enabl>
          Active: active (exited) since Wed 2021-03-24 10:25:43 UTC; 5 months 17 days ago
         Process: 750 ExecStart=/usr/bin/compose-apps-early-start (code=exited, status=0/>
        Main PID: 750 (code=exited, status=0/SUCCESS)

After the ``compose-apps-early-start`` service has been successfully run, ``docker ps`` will show that the preloaded apps are running.


.. _meta-lmp: https://github.com/foundriesio/meta-lmp/tree/main
