.. _docker-credential-helper:

Docker Credential Helper
========================

``fioctl`` has a Docker credential helper, providing easy access to hub.foundries.io.
This enables the use of Docker commands from a personal computer, such as a laptop.

.. note::
   The :ref:`credentials<ref-api-access>` will need the “containers:read” scope to work with Docker.

To do this, run:

.. code:: bash

   sudo fioctl configure-docker

This creates a symlink named ``docker-credential-fio`` in the directory of the docker client binary, pointing to ``fioctl``.
Because the docker client is usually somewhere under ``/usr``, you will likely want to run it with root permission. The helper then updates your Docker config file.

Now, Docker commands will just work.

Example:

::

   docker pull hub.foundries.io/FACTORY/shellhttpd

You can also run ``fioctl configure-docker --help`` for more information and available flags.
