.. _ref-git-config:

Configuring Git
===============

Pushing to the git repositories in your FoundriesFactory is as simple as
configuring git on your personal machine to use the access token you generated
as part of your account creation. Once configured, ``git`` will know when are
connecting to ``source.foundries.io`` and will use this token to authenticate
you with our git server.

Replace ``YOUR_TOKEN`` in the following command with your access token. An
example token looks like this: ``ebAYLaManEgNdRnWKfnwNDJjU45c5LJPmWsYw78z``

.. code-block:: console
 
   git config --global http.https://source.foundries.io.extraheader "Authorization: basic $(echo -n YOUR_TOKEN | base64 -w0)"

You can verify that this has been done successfully by 'listing' your config.

.. code-block:: console

   git config --list

This will show you the values currently set for your global git configuration.
You should see ``source.foundries.io`` referenced like this in the output.

.. code-block:: console

   http.https://source.foundries.io.extraheader=Authorization: basic SllOTVlRMGtId1NERDZUWmhVRHhlZmEyOTYxZG13ZTFwQlZRYjl2dg==

.. todo::
   
   **git-config** add :ref: to 'FoundriesFactory', 'access token', 'account creation' when pages are available
