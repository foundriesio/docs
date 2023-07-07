.. _ref-preloaded-images:

Creating Preloaded Images
=========================

The main purpose of the FoundriesFactory CI is to produce **Targets**. These **Targets** are
produced by two different types of CI builds: LmP ``platform`` and
``container`` builds. By default, ``platform`` builds don't include the Docker
Compose Apps and container images defined in the **Target**. In a similar
fashion ``container`` builds don't produce an image that can be flashed to a
device.

As customers move closer to more formal phases of CI and/or production,
they normally want each **Target** to have a complete image that can run
without having to download container images.  This can be done by
configuring a Factory for "preloaded images".

There are two ways to create these images:

 * :ref:`fioctl targets image<fioctl_targets_image>`
 * configuring ci-scripts.git to preload each build

The easiest way to configure this is by updating a Factory's
:ref:`factory-config.yml <def-containers>` in ``ci-scripts.git`` with::

  lmp:
  ...

      containers:
        preloaded_images:
         enabled: true
         app_type: <restorable|compose>
         shortlist: "money-making-app,debug-tools"
         oe_builtin: <true|false>

Where:

- ``enabled`` -  Whether to produce an archive containing docker images as part of a container build trigger.
- ``shortlist`` - Defines the list of apps to preload. All Target's apps are preloaded if it is not specified or its value is empty.
- ``app_type`` - *Optional*: Defines a type of Apps to preload.
  If an option is not defined or set to an empty value, the ``app_type``  preload will depend on the LmP version. If the LmP version is equal to or higher than **v85**, then `restorable` type is preloaded, otherwise `compose` type.
  See :ref:`ug-restorable-apps` for more details on Restorable Apps.
- ``oe_builtin`` - *Optional*: Preload Apps during an OE build CI run. Should be left disabled/undefined for most machines.

.. note::
   The ``oe_builtin`` is a special preloading case where Apps are preloaded during an OE build CI run, rather than preloaded by the `assemble` run of a LmP CI build. This is needed when the image produced by the LmP build is not a WIC image.

   In this case, rootfs as well as a system image produced by the run include preloaded Apps.

   Only `Restorable` type of Apps (default) are supported by the OE builtin preloader.

   This option does not work with some advanced tagging cases, e.g. multiple container builds using the same platform (see :ref:`ref-advanced-tagging` for more details).

For simple workflows, this may suffice. Because ``lmp`` configuration inherits from 
``containers``, it will cause every **Target** built in the Factory to include and 
enable **all** Docker Compose Apps.

The ``lmp`` can specify a different configuration or disable preloaded images::

  lmp:
    preloaded_images:
      enabled: false
  #   enabled: true
  #   shortlist: "money-making-app"
  ...

  containers:
    preloaded_images:
      enabled: true
      shortlist: "money-making-app,debug-tools"

And finally, it is possible to configure just ``lmp`` builds to preload containers.
In this case, because ``containers`` configuration **doesn't** inherits from 
``lmp``, ``container`` builds will **not** preload images::

  lmp:
    preloaded_images:
      enabled: true
      shortlist: "money-making-app,debug-tools"
  
  ...

  containers:
  ...

Common Advanced Scenario
------------------------

It’s quite common to have more complex workflows. For example, 
a Factory may have their ``containers.git`` set up with multiple branches and 
each branch could specify a different set of applications.

For example, let's assume you have 4 different branches with the following application:

.. code-block::

     # devel and experimental:
     money-making-app - The "product"
     debug-tools      - A compose app with some tooling used for development
     # main: 
     money-making-app - The "product"
     fiotest          - A compose-app that some devices run for QA.
     # production:
     money-making-app - The "product"

In this scenario, it is possible to configure each **Target** individually to preload 
different applications in its image.

This can be configured by additional variables on ``ref_options``.

.. prompt:: text

      ref_options:
        refs/heads/devel:
          params:
            APP_SHORTLIST: "<app1>,<app2>,<...>"
            ASSEMBLE_SYSTEM_IMAGE: "<1|0>  "

- ``APP_SHORTLIST`` - Overrides the list of application.
- ``ASSEMBLE_SYSTEM_IMAGE`` - To enable|disable preloading Apps.

Let's assume you want to produce the following types of Targets:

 * ``devel`` preloaded with the ``money-making-app`` and ``debug-tools``.
 * ``main`` and ``production`` preloaded with the ``money-making-app``.
 * ``experiemental`` will not preload anything .

This can be configured in `factory-config.yml` with:

.. prompt:: text

      lmp:
        tagging:
         # Use a "production" branch, that may have some special platform
         # features enabled/disabled. However, it still uses the containers
         # from main for its apps:
          refs/heads/production:
            - tag: production
              inherit: main
         ...
     
      containers:
        preloaded_images:
          enabled: true
          shortlist: "money-making-app"
     
        tagging:
          # Changes to containers main create both "main" and "production" tagged targets
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

With this configuration in place, the factory will produce **Targets** with
the correct apps preloaded and enabled by default.

Starting compose apps early
---------------------------

Preloading docker images doesn't mean the compose apps start automatically.
Usually compose apps are started by aktualizr-lite after device registration.
However, aktualizr-lite first checks for available updates. If there is a new
target available compose apps will only be started after the update is performed.

.. note::

   Note that this mainly applies to the first launch of compose apps. If
   ``docker-compose.yml`` contains **restart** clause, the container will be started
   by dockerd on subsequent boots.

In some scenarios it is required that compose apps start before device
registration and before aktualizr-lite on a freshly flashed device. This can
be done using one off systemd service and image with pre-loaded containers.

Example compose apps early start script can be found in meta-lmp:

  https://github.com/foundriesio/meta-lmp/tree/main/meta-lmp-base/recipes-support/compose-apps-early-start

The recipe produces a systemd one off service and shell script.

.. note::

   The systemd startup service only runs when the device is **not** registered
   to the Foundries Factory. Otherwise the script is not executed.

The following patch for meta-subscriber-overrides is required to add the
recipe to the lmp-factory-image

    .. code-block::

        --- a/recipes-samples/images/lmp-factory-image.bb
        +++ b/recipes-samples/images/lmp-factory-image.bb
        @@ -24,9 +24,10 @@ CORE_IMAGE_BASE_INSTALL += " \
             networkmanager-nmcli \
             git \
             vim \
        +    compose-apps-early-start \
             packagegroup-core-full-cmdline-utils \
             packagegroup-core-full-cmdline-extended \
             packagegroup-core-full-cmdline-multiuser \


The shell script checks for the list of compose apps to start in the
``/var/lmp/default-apps`` file. This file can't be provided by OSTree so it needs
to be created at runtime. If the file is not present all available compose
apps are started.

Compose apps listed in the default-apps file should be started as soon
as the docker service is started. In addition to that, when **restart** clause
is present in the compose app service, it will be started by dockerd on every
boot if it was at least once started by the script. Example:

.. code-block::

   services:
       fiotest:
           image: hub.foundries.io/demo/fiotest
           restart: always
