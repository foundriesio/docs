.. _ref-containers:

Containers
==========

A Factory's ``containers.git`` repo holds the source for Docker containers, as well as :doc:`compose-apps`.
When changes are made to this repo, new Targets will be built.
The CI logic for building a Target is based on simple naming rules:

 * Ignores top-level directories that ends with ``.disabled``.
 * A container image will be built for every top-level directory containing a file named ``Dockerfile``.
 * A :ref:`compose app <ref-compose-apps>` will be built for every top-level directory containing a file named ``docker-compose.yml``.

Both a container image and compose app will be built if both a Dockerfile and Docker-compose file are included.


Advanced Container Usage
------------------------

A ``docker-build.conf`` file enables advanced functionality.
This is sourced by the CI shell script and can set build time options:


 * **TEST_CMD**: Adding ``TEST_CMD="<some command>"`` directs the CI builder to run the command inside the container to verify that it is functioning correctly.

 * **SKIP_ARCHS**: A container will not be built for the specified architecture, e.g., ``SKIP_ARCHS=arm64``.

 * **EXTRA_TAGS_$ARCH**: This can work with ``SKIP_ARCHS``.
   If builds are skipped for arm64, an arm32 container could be *tagged* for it with ``EXTRA_TAGS_arm=arm64``.

 * **DOCKER_BUILD_CONTEXT**: Set an alternative directory for the Docker build context.

Examples
~~~~~~~~
::

  # Only build for amd64 and arm
  SKIP_ARCHS="arm64"

::

  # Use a 32-bit arm container for a 64-bit host:
  SKIP_ARCHS="arm64"
  EXTRA_TAGS_arm="arm64"

::

  # Use container.git as the build context
  BUILD_CONTEXT="../"

Passing Arguments to Build Context
----------------------------------

Containers may require Dockerfile `ARG`_ support for including build time variables.
If the file ``.docker_build_args`` exists in a container director, the contents are used as ``--build-arg`` options.
These are passed to the ``docker build`` command.

Static information can be done by defining a file like::

 # <container>/.docker_build_args
 KEY=Value
 KEY2="Value with spaces"

This produces a build command that includes ``--build-arg KEY=Value --build-arg KEY2="Value with spaces"``.

The need for dynamic arguments means some values must be generated at build time.
This can be accomplished is by taking advantage of ``docker-build.conf``;
as it is sourced by the build script, it can be used to generate content dynamically.

Example
~~~~~~~

A common case is including Git commit information in a container::

  <container>/docker-build.conf
  # $TAG is set by the build script as the Git short hash of the
  # containers.git commit being built.
  #
  # $x is the path to the container.
  cat <<EOF >$x/.docker_build_args
  GIT_SHA=$TAG
  GIT_MSG="$(git log --format=%s -1)"
  EOF

::

  <container>/Dockerfile
  ...
  # NOTE - These ARG's change *every* build. In order to maximize
  # Docker build caching, they should be as close to the end of the
  # file as possible so that the steps after these lines don't have
  # to get re-run *every* build.
  ARG GIT_SHA
  ARG GIT_MSG
  ENV GIT_SHA=$GIT_SHA
  ENV GIT_MSG=$GIT_MSG

.. _ARG:
   https://docs.docker.com/engine/reference/builder/#arg

Advanced Container Dependencies
-------------------------------

If you need custom code to be executed *before* the Docker build,
add ``pre-build.conf`` in the top-level directory of ``containers.git``.

Examples
~~~~~~~~

Here are examples of what can be done in ``pre-build.conf``:

.. code-block:: bash

 # Create a file with build environment for container "shellhttpd":
 env > shellhttpd/envvars

::

 # Allow containers in factory to use a common base image

 # First: Make our images build in a predictable order.
 # This ensures 0base is built first so other containers can inherit it:
 export IMAGES=$(find ./ -mindepth 2 -maxdepth 2 -name Dockerfile | cut -d / -f2 | sort)

 # Second: Modify each container to use the locally build arch-specific base image:
 _base_img="hub.foundries.io/${FACTORY}/0base:$LATEST-$ARCH"
 for x in $IMAGES ; do
     echo "Prebuild checking $x for FROM override"
     sed -i "s|hub.foundries.io/${FACTORY}/0base|${_base_img}|" $x/Dockerfile
 done

.. note::
    If there is shared files between containers, the recommendation is to put the common folder in the base image.
    The containers can inherit the files using :ref:`ug-multi-stage-container`.
