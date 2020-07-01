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
