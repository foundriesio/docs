.. highlight:: sh

.. _ref-linux-dev-container:

Linux microPlatform Development Container
=========================================

You can install a Docker container based on Ubuntu 16.04 which
provides a Linux microPlatform build environment. This is the
recommended work environment for building Linux microPlatform images
on macOS and Windows. It can also be useful for reproducible builds.

#. `Install Docker`_.

#. Pull the container image.

   **Subscribers** first need to log in to the Open Source Foundries
   subscriber container registry on the system which will run the
   development container, then fetching it::

       docker login hub.foundries.io --username=unused
       docker pull hub.foundries.io/lmp-sdk

   The username is currently ignored when logging in, but a value must
   be provided. When prompted for the password, enter your subscriber
   token. If ``docker pull`` fails, make sure ``docker login``
   succeeds and retry.

   **Public** releases can be fetched from `Docker Hub`_::

      docker pull opensourcefoundries/lmp-sdk

#. Run the container as the ``builder`` user.

   Subscribers::

      docker run -it -u builder --name lmp-sdk hub.foundries.io/lmp-sdk

   Public::

      docker run -it -u builder --name lmp-sdk opensourcefoundries/lmp-sdk

#. Set up Git inside the container::

      git config --global user.name "Your Full Name"
      git config --global user.email "your-email-address@example.com"

You can now follow instructions in :ref:`ref-linux-building` to
build the Linux microPlatform inside the running container.

.. _Install Docker:
   https://docs.docker.com/engine/installation/

.. _Docker Hub:
   https://hub.docker.com/r/opensourcefoundries/lmp-sdk/
