.. highlight:: sh

.. _ref-linux-dev-container:

Development Container
=====================

You can install a Docker container based on Ubuntu 20.04 which
provides a Linux microPlatform build environment (this is the same
container image as used by our own CI). This is the recommended work
environment for building Linux microPlatform images on macOS and Windows.

#. `Install Docker`_.

#. Create local folders for ``sstate-cache``, ``downloads`` and ``build``,
   as a way to save the build environment outside the container:

   .. parsed-literal::

      mkdir -p ~/lmp/sstate-cache ~/lmp/downloads ~/lmp/build

#. Run update |version| of the container as the ``builder`` user:

   .. parsed-literal::

      docker run --rm -u builder --name lmp-sdk -v ~/lmp/build:/build/lmp -v ~/lmp/sstate-cache:/build/lmp/sstate-cache -v ~/lmp/downloads:/build/lmp/downloads -it hub.foundries.io/lmp-sdk:|docker_tag|

#. Set up Git inside the container (required by ``repo``)::

      git config --global user.name "Your Full Name"
      git config --global user.email "your-email-address@example.com"

You can now follow instructions in :ref:`ref-linux-building-install` to
build the Linux microPlatform inside the running container, using
``/build/lmp`` as your main work folder.

.. _Install Docker:
   https://docs.docker.com/get-docker/
