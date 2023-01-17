.. _gs-git-config:

Configuring Git
===============

Pushing to your repositories with :ref:`FoundriesFactory® <ref-factory-definition>` is a matter of configuring Git to use :ref:`Fioctl™ <ref-fioctl>` as a credential helper.
Afterwards, Git will know when you are connecting to ``source.foundries.io`` and will use :ref:`ref-fioctl` for authentication when utilizing ``git`` commands.

Source Code Access Token
########################

In the right top corner, click on the avatar and select :guilabel:`Settings` in the drop-down list.

.. figure:: /_static/git-config/settings.png
   :width: 900
   :align: center

   Factory Settings

Select the tab :guilabel:`Application Credentials` and create a new **Application Credential** by clicking  on :guilabel:`+ New Credentials` in the upper right corner.

.. figure:: /_static/git-config/credentials_plus.png
   :align: center

   Add new credentials button

Complete by adding a **Description** and an **Expiration date** and select :guilabel:`next`.

Check the :guilabel:`Use for tools like fioctl` box and select your **Factory**.
You can later revoke this access and set up a new application credential once you are familiar with the :ref:`ref-api-access`.

.. figure:: /_static/git-config/fioctl_token.png
   :width: 500
   :align: center

   Application credential for source code access

.. important::
   You can also add the ``source:read-update`` scope to existing application credentials.

Setting Up Git
##############

Run the following command to add the relevant entries to the Git configuration:

.. prompt:: bash host:~$, auto

   host:~$ sudo fioctl configure-git

.. important::
   This needs to be run as ``sudo`` instead of directly as the ``root`` user.
   This is because it needs to have privileges to create a symlink in the same directory as where ``git`` is located.

.. warning::
   If for some reason the command fails with an error, the following manual steps can be taken to get the exact same result::
     
      git config --global credential.https://source.foundries.io.username fio-oauth2
      git config --global credential.https://source.foundries.io.helper fio
      ln -s /usr/bin/fioctl /usr/bin/git-credential-fio


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
