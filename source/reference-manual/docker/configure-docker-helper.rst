.. _docker-credential-helper:

Docker Credential Helper
========================

``fioctl`` has a Docker credential helper, providing easier access to hub.foundries.io.
This enables the use of Docker commands from a personal computer, such as a laptop.

.. note::
   The :ref:`credentials<ref-api-access>` will need the “containers:read” scope to work with Docker.

To do this, run:

.. code:: bash

   sudo fioctl configure-docker

This creates a symlink named ``docker-credential-fio`` in the directory of the docker client binary, pointing to ``fioctl``.

.. important::
    Because the Docker client is usually somewhere under ``/usr``, you will want to run ``fioctl configure-docker`` with root permission.

The helper then updates your Docker config file.
Now, Docker commands will just work.

Example:

::

   docker pull hub.foundries.io/FACTORY/shellhttpd

.. important::
   To run Docker commands without sudo, you will need to gain access to ``/var/run/docker.sock``.
   You can do this by `adding yourself to the Docker group <https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user>`_.

You can also run ``fioctl configure-docker --help`` for more information and available flags.

