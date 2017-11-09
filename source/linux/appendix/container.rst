.. _lmp-appendix-container:

Appendix: Linux microPlatform Development Container
===================================================

You can install a Docker container based on Ubuntu 16.04 which
provides a Linux microPlatform build environment. This is the
recommended work environment for building Linux microPlatform images
on macOS and Windows. It can also be useful for reproducible builds.

#. `Install Docker`_.
#. Fetch the container from `Docker Hub`_::

      docker pull opensourcefoundries/lmp-sdk

#. Run the container as the ``builder`` user::

      docker run -it -u builder --name lmp-sdk opensourcefoundries/lmp-sdk

#. Set up Git inside the container::

      git config --global user.name "Your Full Name"
      git config --global user.email "your-email-address@example.com"

You can now follow instructions in :ref:`lmp-building-get-hardware` to
build the Linux microPlatform inside the running container.

.. _Install Docker:
   https://docs.docker.com/engine/installation/

.. _Docker Hub:
   https://hub.docker.com/r/opensourcefoundries/lmp-sdk/
