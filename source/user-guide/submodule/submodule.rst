.. _ug-submodule:

Working With Git Submodules
===========================

This section shows how to add a git submodule to your FoundriesFactory® repository.
This is used when you want an external Git repository, such as GitHub, connected to a Factory repository as a submodule.

Submodules can be used to isolate two different application teams, allowing work to take place in separate repositories.
Each team works in their own repository and each repository is added as a submodule in the Factory repository.

.. tip::
   The steps to add a submodule can be adapted for other git repository hosting services.

Create a GithHub Repository
---------------------------

Go to GitHub_ and create a new repo.
You can choose to use a private or a public repository, each involves separate steps:

.. tabs::

   .. group-tab:: Private

      Select :guilabel:`Private` and :guilabel:`Create repository`.

      .. figure:: /_static/userguide/submodule/private.png
         :width: 800
         :align: center
      
         New Private GitHub repository
      
      The FoundriesFactory CI needs a GitHub personal access token to download the submodule content during the build.
      Many organizations require the recommended Fine-grained tokens be used.
      Follow GitHub's `instructions to generate the token <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token>`_.
      Copy the personal access token.
      
      Now Configure your Factory with the personal access token.
      Use ``fioctl`` to configure the ``githubtok`` variable:

      .. prompt:: bash host:~$, auto

          host:~$ fioctl secrets update githubtok=<PERSONAL_TOKEN>
   
   .. group-tab:: Public

      Select :guilabel:`Public` and :guilabel:`Create repository`.

      .. figure:: /_static/userguide/submodule/public.png
         :width: 800
         :align: center
      
         New Public GitHub repository

Preparing the GitHub Repository
--------------------------------

For this guide, the GitHub repo will be used to specify a Docker Compose Application.
The requirements for the FoundriesFactory CI to build this is to have a folder with a ``Dockerfile`` and a ``docker-compose.yml``
If you are not familiar with the ``containers.git`` file structure, see the section on :ref:`tutorial-compose-app-file-structure`.

Create a folder to initialize the repo.

.. prompt:: bash host:~$, auto

    host:~$ mkdir myapp
    host:~$ cd myapp/
    host:~$ git init
    host:~$ git remote add origin git@github.com:munoz0raul/myapp.git
    
Add the ``shellhttpd`` files as reference:

.. prompt:: bash host:~$, auto

    host:~$ git remote add fio https://github.com/foundriesio/extra-containers.git
    host:~$ git remote update
    host:~$ git checkout remotes/fio/tutorials -- shellhttpd

Your repository folder should be the folder containing the application files. 
Move it from the ``shellhttpd`` folder to the repo root directory:

.. prompt:: bash host:~$, auto

    host:~$ git mv shellhttpd/Dockerfile shellhttpd/docker-compose.yml shellhttpd/httpd.sh .
    host:~$ git rm -r shellhttpd/

You have the files required for a Docker Compose Application:

.. prompt:: bash host:~$, auto

    host:~$ tree ../myapp/

.. code-block:: console
    
     ../myapp/
     ├── docker-compose.yml
     ├── Dockerfile
     └── httpd.sh

Update the image url in ``docker-compose.yml`` with your repo's name.
This example uses ``myapp``:

``docker-compose.yml``:

.. code-block:: yaml

     version: '3.2'
     
     services:
       httpd:
         image: hub.foundries.io/${FACTORY}/myapp:latest
         build: .
         restart: always
         ports:
           - 8080:${PORT-8080}
         environment:
           MSG: "${MSG-Hello world}"

Add all new files, changes and commit and push:

.. prompt:: bash host:~$, auto

    host:~$ git add docker-compose.yml Dockerfile httpd.sh
    host:~$ git commit -m "Adding App Structure"
    host:~$ git push

Adding the Submodule
--------------------

Clone your ``containers.git`` repo and enter its directory:

.. prompt:: bash host:~$

    git clone https://source.foundries.io/factories/<factory>/containers.git
    cd containers

.. tip::

   If you followed the tutorials, your ``containers.git`` might have the ``shellhttpd`` app already.
   If that is the case, to avoid conflict with the submodule example remove or move it to ``shellhttpd.disabled``

Inside the ``containers`` directory, adapt the command below using your GitHub repo:

.. prompt:: bash host:~$

    git submodule add git@github.com:<user>/<repository>.git

.. prompt:: bash host:~$, auto

    host:~$ git submodule add -b devel git@github.com:munoz0raul/myapp.git
    host:~$ cd myapp
    host:~$ git add myapp/
    host:~$ git commit -m "Adding myapp submodule"
    host:~$ git push

Go to the `web app <https://app.foundries.io>`_, select your Factory and click on :guilabel:`Targets`.
The latest Target should be the CI job you just created.
Click anywhere on the Target’s line to see more details.

After the CI Job finishes, refresh the page and find your application in Apps:

.. figure:: /_static/userguide/submodule/app.png
   :width: 500
   :align: center
     
   Submodule Application
  
In your Factory, click on :guilabel:`Source` and select the ``container.git`` repository:

.. figure:: /_static/userguide/submodule/source.png
   :width: 600
   :align: center
     
   Containers Repository

Note the application submodule is available but it is not possible to inspect the application files.

Updating the Submodule Manually
-------------------------------

The submodule inside ``containers.git`` is pinned to the latest GitHub repo commit.
As new commits are added, ``containers.git`` must be updated with the latest submodule changes.
It is possible to do it manually or using GitHub Actions.

To update it manually, go to your ``containers`` folder, inside the submodule and run:

.. prompt:: bash host:~$, auto

    host:~$ cd containers/
    host:~$ git submodule update --remote ./myapp
    host:~$ git add myapp
    host:~$ git commit -m "Updating submodule hash"
    host:~$ git push

Updating the Submodule Automatically
------------------------------------

To automate the previous steps, you have to allow GitHub to access your Factory repo.
For that, you need to create a token.

Go to `Tokens <https://app.foundries.io/settings/tokens>`_ and create a new **Api Token** by clicking on 
:guilabel:`+ New Token`.

Complete with a **Description** and the **Expiration date** and select :guilabel:`next`.

For GitHub, check the :guilabel:`Use for source code access` box and select your **Factory**.

.. figure:: /_static/userguide/mirror-action/mirror-action.png
   :width: 500
   :align: center

   Token for source code access

Copy the token, go to the GitHub repo and find :guilabel:`Settings`.

.. figure:: /_static/userguide/submodule/reposetting.png
   :width: 800
   :align: center
     
   Repository Settings

Select :guilabel:`Secrets` in the left menu and :guilabel:`New repository secret`.

Name it with ``FOUNDRIES_API_TOKEN``, paste your ``<Token>`` on Value and click on :guilabel:`Add Secret`:

.. figure:: /_static/userguide/submodule/actiontoken.png
   :width: 800
   :align: center
     
   Action Token

Create the ``.github/workflows/source-fio-update.yml`` inside your GitHub application repo.
Follow the example below and make sure you update ``<FACTORY_NAME>`` with your Factory, and ``<SUBMODULE_FOLDER>`` with your submodule folder.

.. prompt:: bash host:~$, auto

    host:~$ cd myapp/
    host:~$ mkdir -p .github/workflows/ 
    host:~$ vi .github/workflows/source-fio-update.yml

.. code-block:: yaml

     # .github/workflows/source-fio-update.yml
     
     name: Update source.foundries.io
     
     on:
       push:
         branches: [ devel ]
     
     jobs:
       update:
         runs-on: ubuntu-latest
         steps:
         # Checks-out your repository under $GITHUB_WORKSPACE
         - uses: actions/checkout@v2
         - uses: doanac/gh-action-update-submodule@master
           with:
             remote-repo: https://source.foundries.io/factories/<FACTORY_NAME>/containers.git
             api-token: ${{ secrets.FOUNDRIES_API_TOKEN }}
             submodule-path: "./<SUBMODULE_FOLDER>"
             remote-branch: ${{ github.ref }}

Add and commit your GitHub Action:

.. prompt:: bash host:~$, auto

    host:~$ git add .github/workflows/source-fio-update.yml
    host:~$ git commit -m "Adding Action"
    host:~$ git push

After this commit, the submodule should be automatically updated inside the ``containers.git`` repo.
As a result, it will automatically trigger a new CI Job to build your application.

.. _GitHub: https://github.com/new
