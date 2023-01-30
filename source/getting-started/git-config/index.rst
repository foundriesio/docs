.. _gs-git-config:

Configuring Git
===============

Pushing to your repositories with :ref:`FoundriesFactory® <ref-factory-definition>` is a matter of configuring Git to use :ref:`Fioctl™ <ref-fioctl>` as a credential helper.
Afterwards, Git will know when you are connecting to ``source.foundries.io`` and will use :ref:`ref-fioctl` for authentication when utilizing ``git`` commands.

Setting Up Git
##############

Run the following command to add the relevant entries to the Git configuration:

.. prompt:: bash host:~$, auto

   host:~$ sudo fioctl configure-git

.. important::
   This needs to be run as ``sudo`` instead of directly as the ``root`` user.
   This is because it needs to have privileges to create a symlink in the same directory as where ``git`` is located.

.. warning::
   * If for some reason the command fails with an error, the following manual steps can be taken to get the exact same result::
     
      git config --global credential.https://source.foundries.io.username fio-oauth2
      git config --global credential.https://source.foundries.io.helper fio
      ln -s /usr/bin/fioctl /usr/bin/git-credential-fio

   * Existing users may need to remove the following lines from ``.gitconfig`` to use ``fioctl configure-git`` utility::

      [http "https://source.foundries.io"]
      extraheader = Authorization: basic <TOKEN>

   * If editting scopes on existing tokens, the user should refresh the local ``fioctl`` credentials with::

      fioclt login --refresh-access-token

Verify that this has been successful by cloning a repository from your Factory,
such as your ``containers.git`` repo.
Replace ``<factory>`` with your Factory's name:

.. prompt:: bash host:~$, auto

   host:~$ git clone https://source.foundries.io/factories/<factory>/containers.git

.. tip::

   You can also use ``git config --global --list`` to show the current state of the
   global Git configuration, where ``source.foundries.io`` should be referenced
   along with a username and a helper.

.. seealso::
   
   * :ref:`Fioctl Reference <ref-fioctl>`
   * :ref:`ref-api-access`
