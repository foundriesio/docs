.. _ref-preloaded-images:

Creating Preloaded Images
=========================

The main purpose of CI is to produce Targets. These Targets are
produced by two different types of CI builds: LmP "platform" builds and
"container" builds. By default, platform builds don't include the Docker
Compose Apps and container images defined in the Target. In a similar
fashion container builds don't produce an image that can be flashed to a
device.

As customers move closer to more formal phases of CI and/or production,
they normally want each Target to have a complete image that can run
without having to download container images.  This can be done by
configuring a Factory for "preloaded images".

There are two ways to create these images:

 * :ref:`fioctl targets image<fioctl_targets_image>`
 * configuring ci-scripts.git to preload each build

The easiest way to configure this is updating a Factory's
:ref:`factory-config.yml <def-containers>` in ci-scripts.git with::

 containers:
  preload: true
  assemble_system_image: true

  # Optional: The list of apps to preload can be set globally with:
  # params:
  #   APP_SHORTLIST: "money-making-app,debug-tools"

For simple workflows this may suffice. It will cause every Target built
in the Factory to include and enable **all** Compose Apps.

Common Advanced Scenario
------------------------
It's quite common to have more complex workflows. For example,
a Factory may have their containers.git set up like::

  # experimental and devel branches:
  fiotest          - A compose-app that some devices run for QA.
  money-making-app - The "product"
  debug-tools      - A compose-app with some tooling used for devel

  # master branch
  fiotest          - A compose-app that some devices run for QA.
  money-making-app - The "product"

  # production branch
  money-making-app - The "product"

In this scenario "devel" images should be preloaded with:

 * money-making-app
 * debug-tools

"master" images and "production" should only include the
"money-making-app".

Finally, the "experimental" branch doesn't need to include preloaded
images.

This can be configured in `factory-config.yml` with::

 lmp:
   tagging:
    # Use a "production" branch, that may have some special platform
    # features enabled/disabled. However, it still uses the containers
    # from master for its apps:
    refs/heads/production:
      - tag: production
        inherit: master
    ...

 containers:
  preload: true
  assemble_system_image: true

  params:
    # default to just preloading the money-making-app
    APP_SHORTLIST: "money-making-app"

  tagging:
    # Changes to containers master create both "master" and "production" tagged targets
    refs/heads/master:
      - tag: master
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

With this configuration in place the factory will produce Targets with
the correct apps preloaded and enabled by default.

Really Advanced Scenario
------------------------

User occasionally combine preloaded images with a certain kind of
:ref:`ref-advanced-tagging` that can be difficult to understand::

 lmp:
   tagging:
    refs/heads/sec-fix
      # produce a target with containers from master
      - tag: sec-fix
        inherit: master
      # produce a target with containers from devel
      - tag: sec-fix
        inherit: devel
    ...

In this scenario the devel and master container branches may not even
have the same set of apps/containers. It's generally recommended
to not produce a preloaded image. However, a ``ref_option`` could
be added to set ``ASSEMBLE_SYSTEM_IMAGE: "0"`` for that branch.

``APP_SHORTLIST`` will pick up its override value from the
"refs/heads/sec-fix" ``ref_option``. If devel and master had
different apps such as::

  devel: fiotest,moneymaking-app,debug-tools
  master: moneymaking-app

Preloading could be set by doing a union of these two sets of apps,
``APP_SHORTLIST: "money-making-app,debug-tools"``. In this case the
"master" Target will have money-making-app preloaded from the
container's master branch and the "devel" Target will have both
money-making-app and debug-tools preloaded from the container's
devel branch.
