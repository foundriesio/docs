.. highlight:: sh

.. _ref-linux-dev-container:

Linux microPlatform Development Container
=========================================

You can install a Docker container based on Ubuntu 18.04 which
provides a Linux microPlatform build environment. This is the
recommended work environment for building Linux microPlatform images
on macOS and Windows.

#. `Install Docker`_.

#. Run update |version| of the container as the ``builder`` user:

   .. parsed-literal::

      docker run -it -u builder --name lmp-sdk hub.foundries.io/lmp-sdk:|docker_tag|

#. Set up Git inside the container::

      git config --global user.name "Your Full Name"
      git config --global user.email "your-email-address@example.com"

You can now follow instructions in :ref:`ref-linux-building` to
build the Linux microPlatform inside the running container.

.. _Install Docker:
   https://docs.docker.com/install/
