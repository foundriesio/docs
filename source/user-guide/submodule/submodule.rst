.. _ug-submodule:

Working with Git Submodules
===========================

This section shows how to add a git submodule to your FoundriesFactory repository.

This is very helpful when you want to use an external private or public git repository, 
such as GitHub_, connected to the FoundriesFactory repository as a submodule.

Submodules can be used to isolate two different application teams to work 
on separated repositories. In this case, each team works in their own repository 
and each repository is added as a submodule in the FoundriesFactory repository.

This section can be adapted for other git repository hosting services.

Create Github Repository
------------------------

Go to GitHub_ and click on the button :guilabel:`New` in the upper left corner.

.. figure:: /_static/userguide/submodule/newrepo.png
   :width: 300
   :align: center

   GitHub New Repo

You can choose to use a private or a public repository.

.. tabs::

   .. group-tab:: Private
      
      Complete the :guilabel:`Repository name` with the name that works best for your repository.

      Select :guilabel:`Private` and :guilabel:`Create repository`.

      .. figure:: /_static/userguide/submodule/private.png
         :width: 800
         :align: center
      
         New Private GitHub repository
      
      The FoundriesFactory CI needs GitHub_ personal access token to download 
      the submodule content during the build.

      Go to GitHub_ and in the upper right corner, click on your avatar and :guilabel:`Settings`.

      .. figure:: /_static/userguide/submodule/settings.png
         :width: 300
         :align: center
      
         GitHub Settings
      
      In the left menu, click on the :guilabel:`Developer settings`.
      
      Next, click on the :guilabel:`Personal access tokens` and click on the 
      button :guilabel:`Generate new token`.

      .. figure:: /_static/userguide/submodule/newtoken.png
         :width: 800
         :align: center
      
         Generate new token

      Complete the :guilabel:`Note` and select the :guilabel:`Expiration` you like. 
      Finally, select the :guilabel:`repo` scope and click on the :guilabel:`Generate token`.

      .. figure:: /_static/userguide/submodule/personaltoken.png
         :width: 800
         :align: center
      
         Personal Token Scope
      
      Make sure to copy your personal access token.

      .. figure:: /_static/userguide/submodule/token.png
         :width: 450
         :align: center
      
         Personal Token Scope      
      
      Configure your FoundriesFactory with the personal access token.

      Use ``fioctl`` to configure the ``githubtok`` variable.

      .. prompt:: bash host:~$, auto

          host:~$ fioctl secrets update githubtok=<PERSONAL_TOKEN>
   
   .. group-tab:: Public

      Complete the :guilabel:`Repository name` with the name work best for your repository.

      Select :guilabel:`Public` and :guilabel:`Create repository`.

      .. figure:: /_static/userguide/submodule/public.png
         :width: 800
         :align: center
      
         New Public GitHub repository

Preparing GitHub Repository
---------------------------

The GitHub_ repository created will be used to specify a Docker Compose Application.

The requirements to the FoundriesFactory CI to build a Docker Image and create a 
Docker Compose App with this image is to have a folder with a ``Dockerfile`` and a ``docker-compose.yml``

If you are not familiar with the ``containers.git`` file structure, read the 
section :ref:`tutorial-compose-app-file-structure`.

That being said, create a folder to initialize the GitHub_ repository.

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

Now you have the files required for a Docker Compose Application:

.. prompt:: bash host:~$, auto

    host:~$ tree ../myapp/

Example output:

.. prompt:: text
    
     ../myapp/
     ├── docker-compose.yml
     ├── Dockerfile
     └── httpd.sh

Update the image url in the ``docker-compose.yml`` file with your repository name.
This example uses ``myapp``:

.. prompt:: bash host:~$, auto

    host:~$ vim docker-compose.yml
     
**docker-compose.yml**:

.. prompt:: text

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
    host:~$ git branch -M devel
    host:~$ git push --set-upstream origin devel

Adding Submodule
----------------

Clone your ``containers.git`` repo and enter its directory:

.. prompt:: bash host:~$

    git clone -b devel https://source.foundries.io/factories/<factory>/containers.git
    cd containers

.. tip::

   If you followed the Tutorials, your ``containers.git`` might have the ``shellhttpd`` 
   app already. If that is the case, to avoid conflict with the submodule example remove 
   or move it to ``shellhttpd.disabled``

Inside the ``containers`` adapt the command below to your GitHub_ repository:

.. prompt:: bash host:~$

    git submodule add git@github.com:<user>/<repository>.git

**Example**:

.. prompt:: bash host:~$, auto

    host:~$ git submodule add -b devel git@github.com:munoz0raul/myapp.git
    host:~$ cd myapp
    host:~$ git add myapp/
    host:~$ git commit -m "Adding myapp submodule"
    host:~$ git push

Go to https://app.foundries.io, select your Factory and click on :guilabel:`Targets`:

The latest **Target** named :guilabel:`containers-devel` should be the CI job you just created.

Click anywhere on the Target’s line in the list to see more details.

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

Updating Submodule Manually
---------------------------

The submodule inside the ``containers.git`` is pinned to the latest GitHub_ repository commit.

As new commits are added to the GitHub_ repository, the ``containers.git`` must 
be updated with the latest submodule changes.

It is possible to do it manually or using GitHub_ Actions.

To update it manually, go to your ``containers`` folder, inside the submodule and run:

.. prompt:: bash host:~$, auto

    host:~$ cd containers/
    host:~$ git submodule update --remote ./myapp
    host:~$ git add myapp
    host:~$ git commit -m "Updating submodule hash"
    host:~$ git push

Updating Submodule Automatically
--------------------------------

To automate the previous steps, you have to allow GitHub_ to access your 
FoundriesFactory repository. For that, you need to create a token.

Go to `Tokens <https://app.foundries.io/settings/tokens/>`_ and create a new **Api Token** by clicking on 
:guilabel:`+ New Token`.

Complete with a **Description** and the **Expiration date** and select :guilabel:`next`.

For GitHub_, check the :guilabel:`Use for source code access` box and 
select your **Factory**.

.. figure:: /_static/userguide/mirror-action/mirror-action.png
   :width: 500
   :align: center

   Token for source code access

Copy the token, go to the Github_ repository and find the repository :guilabel:`Settings`.

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

Create the file ``.github/workflows/source-fio-update.yml`` inside your GitHub_ 
application repository. Follow the example below and make sure you update the 
``<FACTORY_NAME>`` to your Factory Name and ``<SUBMODULE_FOLDER>`` with your 
submodule folder name.

.. prompt:: bash host:~$, auto

    host:~$ cd myapp/
    host:~$ mkdir -p .github/workflows/ 
    host:~$ gedit .github/workflows/source-fio-update.yml

**docker-compose.yml**:

.. prompt:: text

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

Add and commit your GitHub_ Action:

.. prompt:: bash host:~$, auto

    host:~$ git add .github/workflows/source-fio-update.yml
    host:~$ git commit -m "Adding Action"
    host:~$ git push

After this commit, the submodule should be automatically updated inside the 
``containers.git`` repository. As a result, it will automatically trigger a new 
FoundriesFactory CI Job to build your application.

.. _GitHub: https://github.com/
