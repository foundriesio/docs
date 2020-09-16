.. _ref-git-config:

Configuring Git
===============

Pushing to the Git repositories in your FoundriesFactory is as simple as
configuring Git on your personal machine to use the **api token** you generated
as part of your account creation. Once configured, ``git`` will know when are
connecting to ``source.foundries.io`` and will use this token to authenticate
you with our Git server.

.. note:: Tokens can be generated at https://app.foundries.io/settings/tokens

Replace ``YOUR_TOKEN`` in the following command with your **api token**. An
example token looks like this: ``ebAYLaManEgNdRnWKfnwNDJjU45c5LJPmWsYw78z``

.. code-block:: console

   git config --global http.https://source.foundries.io.extraheader "Authorization: basic $(echo -n YOUR_TOKEN | base64 -w0)"

You can verify that this has been successful by attempting to clone a repository
from your FoundriesFactory. As an example, you can clone your ``containers.git``
repo.

Replace ``<factory>`` with your FoundriesFactory name.

.. code-block:: console

   git clone https://source.foundries.io/factories/<factory>/containers.git

.. tip::

   You can also use ``git config --list`` to show you the current state of the
   global Git configuration, in which ``source.foundries.io`` should be referenced
   along with your **api token**, represented as a base64 string.

.. todo::

   **git-config** add :ref: to 'FoundriesFactory', 'api token', 'account
   creation', 'ci scripts' when pages are available
