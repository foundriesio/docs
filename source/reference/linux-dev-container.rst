.. highlight:: sh

.. _ref-linux-dev-container:

Linux microPlatform Development Container
=========================================

You can install a Docker container based on Ubuntu 16.04 which
provides a Linux microPlatform build environment. This is the
recommended work environment for building Linux microPlatform images
on macOS and Windows.

#. `Install Docker`_.

#. **Subscribers only:** log in to the Open Source Foundries
   subscriber container registry on the system which will run the
   development container::

       docker login hub.foundries.io --username=unused

   The username is currently ignored when logging in, but a value must
   be provided. When prompted for the password, enter your subscriber
   access token.

#. Run the container as the ``builder`` user.

   **Subscribers:** run update |version| of the container:

   .. parsed-literal::

      docker run -it -u builder --name lmp-sdk \\
             hub.foundries.io/lmp-sdk:|docker_subscriber_tag|

   **Public:** run update |public_version| of the container:

   .. parsed-literal::

      docker run -it -u builder --name lmp-sdk \\
             opensourcefoundries/lmp-sdk:|docker_public_tag|

#. Set up Git inside the container::

      git config --global user.name "Your Full Name"
      git config --global user.email "your-email-address@example.com"

You can now follow instructions in :ref:`ref-linux-building` to
build the Linux microPlatform inside the running container.

.. _Install Docker:
   https://docs.docker.com/engine/installation/

.. _Docker Hub:
   https://hub.docker.com/r/opensourcefoundries/lmp-sdk/
