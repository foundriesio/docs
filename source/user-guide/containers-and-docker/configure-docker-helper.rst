.. _docker-credential-helper:

Docker Credential Helper
========================

Fioctl® has a Docker credential helper, providing easier access to ``hub.foundries.io``.
This enables the use of Docker commands from a personal computer, such as a laptop.

.. note::
   The :ref:`credentials<ref-api-access>` will need the “containers:read” scope to work with Docker.

.. important::
   On macOS, you may encounter authentication issues.
   This is due to Git on OSX using the Keychain Access Utility.
   Git attempts to use this for authentication before ``git-credential-fio``.

   The solution is to remove Keychain Access entries from your git config file.
   Locate the git config by running::

    git config -l --show-origin | grep credential
  
   Edit the gitconfig file with ``credential.helper=osxkeychain``, commenting out the line.

   Fioctl should now be able to authenticate.

To do this, run:

.. code:: bash

   sudo fioctl configure-docker

This creates a symlink named ``docker-credential-fio`` in the directory of the docker client binary, pointing to ``fioctl``.

.. important::
    Because the Docker client is usually somewhere under ``/usr``, you will want to run ``fioctl configure-docker`` with root permission.

The helper then updates *your* Docker config file, which is located under ``$HOME/.docker``.

.. note::
    The helper configures for the current `user` and not the entire `system`.
    If you are logged in as root, then it would be in the root home directory, which you should generally avoid doing.

Now, Docker commands will just work.

Example:

::

   docker pull hub.foundries.io/FACTORY/shellhttpd

.. important::
   To run Docker commands without sudo, you will need to gain access to ``/var/run/docker.sock``.
   You can do this by `adding yourself to the Docker group <https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user>`_.

You can also run ``fioctl configure-docker --help`` for more information and available flags.

