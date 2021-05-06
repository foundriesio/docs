.. _gs-git-config:

Configuring Git
===============

Pushing to the Git repositories in your FoundriesFactory is as simple as
configuring Git on your personal machine to use the **api token** you generated
as part of your :ref:`account creation <gs-signup>`. Once configured, ``git`` will know when are
connecting to ``source.foundries.io`` and will use this token to authenticate
you with our Git server.

Source Code Access Token
########################

In the right top corner, click on the avatar and select :guilabel:`Settings` in the 
drop-down list.

.. figure:: /_static/git-config/settings.png
   :width: 900
   :align: center

   FoundriesFactory Settings

Select the tab :guilabel:`Tokens` and create a new **Api Token** by clicking on 
the :guilabel:`+ New Token`.
Complete with a **Description** and the **Expiration date** and select :guilabel:`next`.

Check the :guilabel:`Use for source code access` box and 
select your **Factory**. You can later revoke this access and set up a new 
token once you are familiar with the :ref:`ref-api-access`.

.. figure:: /_static/git-config/token.png
   :width: 500
   :align: center

   Token for source code access


Git Setup
#########

Replace ``YOUR_TOKEN`` in the following command with your access token. An
example token looks like this: ``ebAYLaManEgNdRnWKfnwNDJjU45c5LJPmWsYw78z``

.. prompt:: bash host:~$, auto

   host:~$ git config --global http.https://source.foundries.io.extraheader "Authorization: basic $(echo -n YOUR_TOKEN | openssl base64)"

You can verify that this has been successful by attempting to clone a repository
from your FoundriesFactory. As an example, you can clone your ``containers.git``
repo.

Replace ``<factory>`` with your FoundriesFactory name.

.. prompt:: bash host:~$, auto

   host:~$ git clone https://source.foundries.io/factories/<factory>/containers.git

.. tip::

   You can also use ``git config --list`` to show you the current state of the
   global Git configuration, in which ``source.foundries.io`` should be referenced
   along with your access token, represented as a base64 string.

.. todo::

   **git-config** add :ref: to 'FoundriesFactory', 'access token', 'account
   creation', 'ci scripts' when pages are available
