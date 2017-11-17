.. _lmp-appendix-container:

Appendix: Linux microPlatform Development Container
===================================================

You can install a Docker container based on Ubuntu 16.04 which
provides a Linux microPlatform build environment. This is the
recommended work environment for building Linux microPlatform images
on macOS and Windows. It can also be useful for reproducible builds.

#. `Install Docker`_.

#. Accessing Container Registry

   Open Source Foundries provides a continuously updated container
   registry to subscribers. Public releases to Docker Hub lag these
   subscriber releases.
   
#. Public releases can be fetched from `Docker Hub`_::

      docker pull opensourcefoundries/lmp-sdk

#. Subscriber releases can be fetched from hub.foundries.io::

      docker pull hub.foundries.io/lmp-sdk

   If this command fails, make sure to run ``docker login`` as described
   in :ref:`iot-gateway`.

   Subscribers may also find it useful to create a :file:`.netrc` which 
   is designed to store authentication credentials. To set this up, 
   please refer to :ref:`iot-gateway-subscriber-playbooks`.
   
#. Run the container as the ``builder`` user::

      docker run -it -u builder --name lmp-sdk opensourcefoundries/lmp-sdk

      docker run -it -u builder --name lmp-sdk hub.foundries.io/lmp-sdk

#. Set up Git inside the container::

      git config --global user.name "Your Full Name"
      git config --global user.email "your-email-address@example.com"

You can now follow instructions in :ref:`lmp-building-install` to
build the Linux microPlatform inside the running container.

.. _Install Docker:
   https://docs.docker.com/engine/installation/

.. _Docker Hub:
   https://hub.docker.com/r/opensourcefoundries/lmp-sdk/
