.. _ug-container-preloading:

Container Preloading
====================

This guide covers configuring your ``platform`` images to preload Docker Compose Apps.

By default, the ``platform`` build creates an image to be flashed to a device—that does not include Docker Compose Apps.
Then, after installing the image and registering the device, ``aktualizr-lite`` downloads and runs the configured Apps.

Cases where having Apps preloaded on the image can be helpful include:

- Executing a Docker Compose App right after first boot, even without internet or registering the device.
- Reducing network data usage during the Docker Image download.

.. warning::

    Preloading container images will increase the size of the system image considerably,
    especially if the containers have not been optimally constructed.

    Refer to the official Docker documentation for
    `best practices on writing Dockerfiles <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/>`_.

There are two ways to create these images:

 * :ref:`fioctl targets image<fioctl_targets_image>`
 * configuring ``ci-scripts`` to preload each build

Here we focus on the second approach, so that every Target includes a flashable image with preloaded containers.

Configure the CI
----------------

Clone your ``ci-scripts`` repo and enter its directory:

.. prompt:: bash host:~$

    git clone https://source.foundries.io/factories/<factory>/ci-scripts.git
    cd ci-scripts

Add the following to ``factory-config.yml``,
making sure to set the appropriate values for ``app_type`` and ``oe_builtin`` (see below):

.. code-block:: YAML 

      containers:
        preloaded_images:
         enabled: true
         app_type: <restorable|compose>
         shortlist: "shellhttpd"
         oe_builtin: <true|false>

- ``enabled``- Whether to produce an archive containing Docker images as part of a container build trigger.
- ``shortlist``- Defines the list of apps to preload.
  All the  Target's apps are preloaded if not specified or empty.
  Here, it is set to preload the ``shellhttpd`` app.
- ``app_type`` - Defines the type of Apps to preload.
  If not defined, or set to an empty value, the ``app_type`` preload will depend on the LmP version.
  If the LmP version is **v85** or newer, then `restorable` type is preloaded, otherwise `compose` type is used.
  See :ref:`ug-restorable-apps`.
- ``oe_builtin`` - *Optional*: Preload Apps during an OE build CI run. Should be left disabled/undefined for most machines.

.. note::
   ``oe_builtin`` is a special preloading case where Apps are preloaded during an OE build, rather than by the `assemble` run of a LmP build.
   This is needed when the image produced is not a WIC image.

   In this case, rootfs and the system image will include preloaded Apps.

   Only `Restorable` type of Apps (default) are supported by the OE builtin preloader.

   This option does not work with some advanced tagging cases, e.g. multiple container builds using the same platform (see :ref:`ref-advanced-tagging` for more details).

Add the ``factory-config.yml`` file, commit and push:

.. prompt:: bash host:~$, auto

    host:~$ git commit -m "Configure shellhttpd as preload app" factory-config.yml
    host:~$ git push

Getting a New Image with Preloaded Containers
----------------------------------------------

After these steps, a ``platform`` or ``containers`` build will generate a ``.wic.gz`` file with the preloaded Docker Images under
:guilabel:`Runs`, ``assemble-system-image`` , ``<tag>``.

For example, pushing to ``main`` triggers the usual build and an additional run called ``assemble-system-image``.
Check the latest Target you just created:

.. figure:: /_static/user-guide/containers-and-docker/container-preloading-new-target.png
   :width: 900
   :align: center

   New Target

When the FoundriesFactory™ Platform CI finishes, click Target.
Find :guilabel:`Runs` and download the image from ``assemble-system-image``.
Flash the image and boot the device.

.. note::

    Some devices require additional artifacts to be flashed.
    In this case, download the files from the latest ``platform`` build and only use the ``image`` from ``assembly-system-image``. 
    For more information about how to flash your device, read :ref:`ref-boards`.

Checking the Preloaded Image
----------------------------

Restorable Type
~~~~~~~~~~~~~~~

Restorable apps are enabled by default on LmP v85+.

On your device, switch to root and list the files in the folder ``/var/sota/reset-apps``.

.. prompt:: bash device:~$

    sudo su
    ls /var/sota/reset-apps/apps

.. code-block:: text

     app-05 app-07 app-08

Preloaded Restorable Apps are listed in the output, provided that the preloading was successful.
In this case, the preloaded apps are ``app-05``, ``app-07`` and ``app-08``.

Another option to verify whether Restorable Apps are preloaded is to use the `aklite-apps` utility.

.. prompt:: bash device:~$

    sudo su
    aklite-apps ls

.. code-block:: text

     app-05
     app-07
     app-08

Try to start the preloaded Restorable Apps manually using `aklite-apps`:

.. prompt:: bash device:~$

    sudo su
    aklite-apps run [--apps <a comma separated list of Apps>]

.. note::
    ``app_type`` is set to ``restorable`` by default since LmP **v85**.
    If ``compose`` app type is set, then the preloaded apps are located under ``/var/sota/compose-apps/<app>``.
    Here is an example using ``shellhttpd`` preloaded app:

    .. prompt:: bash device:~$

        sudo su
        ls /var/sota/compose-apps/shellhttpd
        Dockerfile  docker-build.conf  docker-compose.yml  httpd.sh

Starting Compose Apps Automatically
-----------------------------------

To start the preloaded application automatically between the boot and the device registration when aktualizr-lite starts,
enable a systemd service responsible for it.

meta-lmp_ provides a recipe that launches preloaded apps after the device boots.

Clone your ``meta-subscriber-overrides.git`` repo and enter its directory:

.. prompt:: bash host:~$

    git clone https://source.foundries.io/factories/<factory>/meta-subscriber-overrides.git
    cd meta-subscriber-overrides

Edit the ``recipes-samples/images/lmp-factory-image.bb`` file and add the recipe to the ``CORE_IMAGE_BASE_INSTALL`` list:

.. code-block:: diff

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

The latest Target should be the CI job you just created.

.. figure:: /_static/user-guide/containers-and-docker/container-preloading-platform.png
   :width: 900
   :align: center

   New Platform Target

When the FoundriesFactory CI finishes, click on the Target.
Find :guilabel:`Runs` and download the image from the ``assemble-system-image`` run.
Flash the image and boot the device.

Testing Auto Start
------------------

On your device, list the ``compose-apps-early-start`` service:

.. prompt:: bash device:~$

    systemctl list-unit-files | grep enabled | grep compose-apps-early-start

.. code-block:: text

    compose-apps-early-start.service           enabled         enabled

Verify the ``compose-apps-early-start`` application status:

.. prompt:: bash device:~$, auto

    device:~$  systemctl status compose-apps-early-start

.. code-block:: text

     compose-apps-early-start.service - Ensure apps are configured and running as early>
          Loaded: loaded (/usr/lib/systemd/system/compose-apps-early-start.service; enabl>
          Active: active (exited) since Wed 2021-03-24 10:25:43 UTC; 5 months 17 days ago
         Process: 750 ExecStart=/usr/bin/compose-apps-early-start (code=exited, status=0/>
        Main PID: 750 (code=exited, status=0/SUCCESS)

After the ``compose-apps-early-start`` service has been successfully run, ``docker ps`` will show that the preloaded apps are running.

Common Advanced Scenario
------------------------

More complex workflows are common.
For example, a Factory may have ``containers.git`` set up with multiple branches where each specifies a different set of apps.

Assume you have four branches with the following application:

.. code-block:: shell

     # devel and experimental:
     money-making-app - The "product"
     debug-tools      - A compose app with some tooling used for development
     # main: 
     money-making-app - The "product"
     fiotest          - A compose-app that some devices run for QA.
     # production:
     money-making-app - The "product"

In this scenario, you can configure each Target individually to preload different applications in its image.

Configure this with additional variables for ``ref_options``.

.. code-block:: yaml

      ref_options:
        refs/heads/devel:
          params:
            APP_SHORTLIST: "<app1>,<app2>,<...>"
            ASSEMBLE_SYSTEM_IMAGE: "<1|0>  "

- ``APP_SHORTLIST`` - Overrides the list of application.
- ``ASSEMBLE_SYSTEM_IMAGE`` - To enable|disable preloading Apps.

Assume you want to produce the following types of Targets:

 * ``devel`` preloaded with the ``money-making-app`` and ``debug-tools``.
 * ``main`` and ``production`` preloaded with the ``money-making-app``.
 * ``experiemental`` will not preload anything .

Configure this in ``factory-config.yml`` with:

.. code-block:: yaml

      lmp:
        tagging:
         # Use a "production" branch, that may have some special platform
         # features enabled/disabled. However, it still uses the containers
         # from master for its apps:
          refs/heads/production:
            - tag: production
              inherit: main
         ...
     
      containers:
        preloaded_images:
          enabled: true
          shortlist: "money-making-app"
     
        tagging:
          # Changes to containers main create both "main" and "production" tagged Targets.
          refs/heads/main:
            - tag: main
            - tag: production
          refs/heads/devel:
            - tag: devel
     
        ref_options:
          refs/heads/devel:
            params:
              APP_SHORTLIST: "money-making-app,debug-tools"
          refs/heads/experimental:
            params:
              # Don't produce a preloaded system image
              ASSEMBLE_SYSTEM_IMAGE: "0"

With this configuration, the Factory will produce Targets with the correct apps preloaded and enabled by default.

.. _meta-lmp: https://github.com/foundriesio/meta-lmp/tree/main
