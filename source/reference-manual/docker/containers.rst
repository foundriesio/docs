.. _ref-containers:

Containers
==========

Every factory has a containers.git repository. This repository holds the
source for Docker containers to be built as well as :doc:`compose-apps`.
As changes are made to this repository new Targets will be built. The CI
logic for building a Target is based on simple naming rules:

 * Ignore any top-level directory that ends with ``.disabled``.
 * A container image will be built for every top-level directory containing
   a file named ``Dockerfile``.
 * A compose app will be built for every top-level directory containing
   a file named ``docker-compose.yml``.
 * Both a container image and compose app will be built if a top-level
   directory includes both types of files.


Advanced Container Usage
------------------------

A container directory may contain a ``docker-build.conf`` file that enables
some advanced functionality. This file "sourced" by the CI shell script and
can set a few special variables to influence what's done at build time:


 * **CI testing** - Adding ``TEST_CMD="<some command>"`` directs the CI
   builder to run the command inside the container it just built as a means
   of verifying its functioning correctly.

 * **SKIP_ARCHS** - By default containers are builds for arm, arm64, and amd64.
   If a container won't build for a certain architecture, it can be skipped.
   For example ``SKIP_ARCHS=arm64``.

 * **MANIFEST_PLATFORMS** - If ``SKIP_ARCHS`` is used, then
   ``MANIFEST_PLATFORMS`` will need to be updated to reflect what platforms
   this multi-arch container is being published for. Following the example
   above its possible to do: ``MANIFEST_PLATFORMS=linux/amd64,linux/arm``

 * **EXTRA_TAGS_$ARCH** - This can work with ``SKIP_ARCHS``. If builds are
   skipped for arm64, the arm container could be tagged for it with:
   ``EXTRA_TAGS_arm=arm64``.

 * **DOCKER_BUILD_CONTEXT** - Use an alternative directory for the docker
   build context.

Examples
~~~~~~~~
::

  # Only build for amd64 and arm
  SKIP_ARCHS="arm64"
  MANIFEST_PLATFORMS="linux/arm,linux/amd64"

::

  # Use a 32-bit arm container for a 64-bit host:
  SKIP_ARCHS="arm64"
  EXTRA_TAGS_arm="arm64"

::

  # Use container.git as the build context
  BUILD_CONTEXT="../"

Passing Arguments to Build Context
----------------------------------

Containers may require Dockerfile `ARG`_ support for including
build time variables. If the file ``.docker_build_args`` exists in a
container directory, the build script will turn the  contents
into ``--build-arg`` options passed to the ``docker build`` command.

Static information can be done by simply defining a file like::

 # <container>/.docker_build_args
 KEY=Value
 KEY2="Value with spaces"

That would produce a build command that included
``--build-arg KEY=Value --build-arg KEY2="Value with spaces"``.

The need for dynamic arguments usually means the values must
be generated at build time. The way this can be accomplished is by
taking advantage of ``docker-build.conf``. This file is "sourced"
by the build script, so it can be used to generate content dynamically.

Example
~~~~~~~
A common case is including Git commit information into the container::

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

In rare occasions a Factory may need some custom code to run *before* the
docker build logic is called on each container. This can be done with a file
in the top-level directory of containers.git, ``pre-build.conf``.

Examples
~~~~~~~~

Here are some examples of things that can be done inside
``pre-build.conf``:

.. code-block:: bash

 # Create a file with build environment for container "shellhttpd":
 env > shellhttpd/envvars

::

 # Allow containers in factory to use a common base image

 # First: Make our images build in a predictable order.
 # This ensures 0base is built first so other containers can inherit it:
 export IMAGES=$(find ./ -mindepth 2 -maxdepth 2 -name Dockerfile | cut -d / -f2 | sort)

 # Second: Modify each container to use the locally build arch-specific base image:
 _base_img="hub.foundries.io/${FACTORY}/0base:$(git log -1 --format=%h)-$ARCH"
 for x in $IMAGES ; do
     echo "Prebuild checking $x for FROM override"
     sed -i "s|hub.foundries.io/${FACTORY}/0base|${_base_img}|" $x/Dockerfile
 done

