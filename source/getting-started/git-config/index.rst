.. _gs-git-config:

Configuring Git
===============

Pushing to your repositories with :ref:`FoundriesFactory <ref-factory-definition>`
is as simple as configuring Git on your computer to use the :ref:`api token <ref-api-access>`
you generated during :ref:`account creation <gs-signup>`.
Afterwards, Git will know when you are connecting to ``source.foundries.io`` and
will use this token to authenticate you with our Git server.

Source Code Access Token
########################

In the right top corner, click on the avatar and select :guilabel:`Settings`
in the drop-down list.

.. figure:: /_static/git-config/settings.png
   :width: 900
   :align: center

   FoundriesFactory Settings

Select the tab :guilabel:`Tokens` and create a new **Api Token** by clicking on 
:guilabel:`+ New Token`. Complete by adding a **Description** and an
**Expiration date** and select :guilabel:`next`.

Check the :guilabel:`Use for source code access` box and select your
**Factory**. You can later revoke this access and set up a new  token once you
are familiar with the :ref:`ref-api-access`.

.. figure:: /_static/git-config/token.png
   :width: 500
   :align: center

   Token for source code access

Git Setup
#########

In the following command, replace ``YOUR_TOKEN`` with your access token. An
example token looks like this: ``ebAYLaManEgNdRnWKfnwNDJjU45c5LJPmWsYw78z``

.. prompt:: bash host:~$, auto

   host:~$ git config --global http.https://source.foundries.io.extraheader "Authorization: basic $(echo -n YOUR_TOKEN | openssl base64)"

Verify that this has been successful by cloning a repository from your Factory,
such as your ``containers.git`` repo. Replace ``<factory>`` with your
FoundriesFactory name:

.. prompt:: bash host:~$, auto

   host:~$ git clone https://source.foundries.io/factories/<factory>/containers.git

.. tip::

   You can also use ``git config --list`` to show you the current state of the
   global Git configuration, Here, ``source.foundries.io`` should be referenced
   along with your access token, represented as a base64 string.
