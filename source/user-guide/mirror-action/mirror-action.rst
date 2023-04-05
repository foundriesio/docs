.. _ug-mirror-action:

Configuring Automatic Git Mirroring
===================================

This section shows how to configure a GitHub_ Action for mirroring your commits 
to the FoundriesFactory repository.

This is very useful when you want to use an external private or public git repository 
such as GitHub_.

This section can be adapted for other git repository hosting services.

Creating Token
--------------

To allow GitHub_ to access your FoundriesFactory repository, you need to create a token.

Go to `Tokens <https://app.foundries.io/settings/tokens/>`_ and create a new **Api Token** by clicking on 
:guilabel:`+ New Token`.

Complete with a **Description** and the **Expiration date** and select :guilabel:`next`.

For GitHub_, check the :guilabel:`Use for source code access` box and 
select your **Factory**.

.. figure:: /_static/userguide/mirror-action/mirror-action.png
   :width: 500
   :align: center

   Token for source code access

Convert the token value to a base64 string:

.. prompt:: bash host:~$, auto

    host:~$ echo -n <FIO_TOKEN> | base64 -w0

**Example Output**:

.. prompt:: text

     host:~$ echo -n SQMD1Gx860mPI6jZFlLJLwaCXT5CqAaQi6nEfIfH | base64 -w0
     U1FNRDFHeDg2MG1QSTZqWkZsTEpMd2FDWFQ1Q3FBYVFpNm5FZklmSA==

Save the output of this command to your copy buffer. This is your ``<BASE64_FIO_TOKEN>`` value.

.. note::

    Your value should end with ``==`` and the output won't have a carriage return added.


Configuring GitHub Repository
-----------------------------

Go to GitHub_ and find the repository you want to mirror.

Click on :guilabel:`Settings`:

.. figure:: /_static/userguide/mirror-action/mirror-action-github-setting.png
   :width: 900
   :align: center

   GitHub Settings

Click on :guilabel:`Secrets` and create a new **secret** by clicking on 
:guilabel:`New repository secret`.

.. figure:: /_static/userguide/mirror-action/mirror-action-github-secrets.png
   :width: 900
   :align: center

   GitHub Secrets

The Github_ Action uses the variable ``GIT_ACCESS_TOKEN`` as the token to access 
your Foundries Factory repository.

However, complete the **Name** with ``GIT_ACCESS_TOKEN`` and on **Value** paste 
the ``<BASE64_FIO_TOKEN>`` provided above.

Finally, click on :guilabel:`Add secret`.

.. figure:: /_static/userguide/mirror-action/mirror-action-github-new-secret.png
   :width: 900
   :align: center

   GitHub New Secret

Creating Mirror Action
----------------------

The FoundriesFactory CI only triggers builds for configured branches. This is 
configured in the ``ci-scripts.git`` repository in the ``factory-config.yml`` file.

Your ``factory-config.yml`` can be inspected by updating the following URL with your ``<FACTORY-NAME>``:

- https://source.foundries.io/factories/<FACTORY-NAME>/ci-scripts.git/tree/factory-config.yml

Under ``lmp:`` and ``containers:`` the group ``tagging:`` shows the configured branches on ``refs/heads/<branch>:``.

**Example**:

.. prompt:: text

    lmp:
      tagging:
        refs/heads/master:
          - tag: master
        refs/heads/devel:
          - tag: devel
    ...
    containers:
      tagging:
        refs/heads/master:
          - tag: master
        refs/heads/devel:
          - tag: devel
    ...

Based on the example, FoundriesFactory CI is configured to trigger new builds 
whenever a new commit is sent on ``master`` or ``devel`` branches. The following 
commands, guides you to mirror the ``master`` branch.

.. note::

    Notice that this example is updating the FoundriesFactory repository ``containers.git``. 
    The same approach can be used to update ``lmp-manifest.git`` and ``meta-subscriber-overrides.git``.

Clone your GitHub repository and enter its directory:

.. note::

    Make sure to update the clone command with your repository URL.

.. prompt:: bash host:~$

    git clone https://github.com/<host>/<repo_name>
    cd <repo_name>

Check out the ``master`` branch.

.. prompt:: bash host:~$, auto

    host:~$ git checkout master

In case you don't have a master branch yet, create one:

.. prompt:: bash host:~$, auto

    host:~$ git checkout -b master

You must store workflow files in the ``.github/workflows/`` directory of your repository.

.. prompt:: bash host:~$, auto

    host:~$ mkdir -p .github/workflows/

Finally, create the file ``mirror.yml`` and make sure you update the ``<FACTORY-NAME>`` with your Factory Name.

.. prompt:: bash host:~$, auto

    host:~$ gedit .github/workflows/mirror.yml

**.github/workflows/mirror.yml**:

.. prompt:: text

      name: Mirroring
      
      on: [push]
      
      jobs:
        to_foundries:
          runs-on: ubuntu-20.04
          steps:
            - uses: actions/checkout@v2
              with:
                fetch-depth: 0
            - uses: foundriesio/mirror-action@master
              with:
                REMOTE: "https://source.foundries.io/factories/<FACTORY-NAME>/containers.git"
                GIT_ACCESS_TOKEN: ${{ secrets.GIT_ACCESS_TOKEN }}
                PUSH_ALL_REFS: "false"

.. warning::

    ``PUSH_ALL_REFS`` is **false**. If **true** it synchronizes all branches.

.. warning::

    Make sure you make a backup of any content in your FoundriesFactory repository 
    that you want to preserve as this action can completely replace all branches.

Add the changed files, commit and push to your GitHub_ repository:

      .. prompt:: bash host:~$, auto

          host:~$ git add .github/workflows/mirror.yml
          host:~$ git commit -m "Adding Mirror Action"
          host:~$ git push

Github Action
-------------

Once the ``mirror.yml`` is in place on your GitHub_ repository, every change to 
the configured branch will start an Action on GitHub_ to mirror your repository 
to your FoundriesFactory Repository.

You can find the GitHub_ Action by clicking on :guilabel:`Actions`:

.. figure:: /_static/userguide/mirror-action/mirror-action-github-action.png
   :width: 900
   :align: center

   GitHub Action

On that page, you can find the list of Actions as well as inspect each one.

.. figure:: /_static/userguide/mirror-action/mirror-action-github-action-list.png
   :width: 900
   :align: center

   GitHub Action list

Your repositories from FoundriesFactory and GitHub_ should look the same.

.. figure:: /_static/userguide/mirror-action/mirror-action-github-compare.png
   :width: 900
   :align: center

   FoundriesFactory and GitHub_

.. _GitHub: https://github.com/
