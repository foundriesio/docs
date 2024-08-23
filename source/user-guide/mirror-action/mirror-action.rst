.. _ug-mirror-action:

Configuring Automatic Git Mirroring
===================================

This page shows how to configure source code mirroring to the FoundriesFactory™ Platform repos.
This is useful when using external Git repositories, hosted on services such as GitHub_ or Bitbucket_.
While the focus is on setting up GitHub Actions and Bitbucket pipelines, the steps can be adapted for other hosting services.

.. _ug-mirror-token:

Creating Token
--------------

To allow external hosting services to access your FoundriesFactory repo, you need to create a token.
Create a new `API Token <https://app.foundries.io/settings/tokens/>`_ by clicking on :guilabel:`+ New Token`.
Complete with a **Description** and the **Expiration date** and select :guilabel:`Next`.
Check the :guilabel:`Use for source code access` box and select your **Factory**.

.. figure:: /_static/userguide/mirror-action/mirror-action.png
   :width: 500
   :align: center

   Token for source code access

If Bitbucket is used, the token generated in the previous step is used as the ``<GIT_ACCESS_TOKEN>`` value.
If GitHub is used, convert the token value to a base64 string and save the output of this command. This is your ``<BASE64_FIO_TOKEN>`` value.

.. prompt:: bash host:~$, auto

   host:~$ echo -n <FIO_TOKEN> | base64 -w0

.. code-block:: console

   host:~$ echo -n SQMD1Gx860mPI6jZFlLJLwaCXT5CqAaQi6nEfIfH | base64 -w0
   U1FNRDFHeDg2MG1QSTZqWkZsTEpMd2FDWFQ1Q3FBYVFpNm5FZklmSA==

.. tip::

   ``<BASE64_FIO_TOKEN>`` should end with ``==`` with no carriage return.

Configuring GitHub
------------------

Go to GitHub and find the repository you want to mirror.

Click on :guilabel:`Settings`:

.. figure:: /_static/userguide/mirror-action/mirror-action-github-setting.png
   :width: 900
   :align: center

   GitHub Settings

Click on :guilabel:`Secrets` and create a new **secret** by clicking on :guilabel:`New repository secret`.

.. figure:: /_static/userguide/mirror-action/mirror-action-github-secrets.png
   :width: 900
   :align: center

   GitHub Secrets

The GitHub Action uses the variable ``GIT_ACCESS_TOKEN`` as the token to access your Factory repo.

However, complete the **Name** with ``GIT_ACCESS_TOKEN``, and on **Value** paste the ``<BASE64_FIO_TOKEN>`` provided above.

Finally, click on :guilabel:`Add secret`.

.. figure:: /_static/userguide/mirror-action/mirror-action-github-new-secret.png
   :width: 900
   :align: center

   GitHub New Secret

Creating Mirror Action
^^^^^^^^^^^^^^^^^^^^^^

The FoundriesFactory CI only triggers builds for configured branches.
This is configured in the ``ci-scripts.git`` repository in the ``factory-config.yml`` file.

Your ``factory-config.yml`` can be inspected by updating the following URL with your ``<FACTORY-NAME>``:

- https://source.foundries.io/factories/<FACTORY-NAME>/ci-scripts.git/tree/factory-config.yml

Under ``lmp:`` and ``containers:``, the group ``tagging:`` shows the configured branches on ``refs/heads/<branch>:``.

.. code-block:: YAML

    lmp:
      tagging:
        refs/heads/main:
          - tag: main
    ...
    containers:
      tagging:
        refs/heads/main:
          - tag: main
    ...

In this example, the CI is configured to trigger new builds whenever a new commit is made to the ``main`` branch.
The following commands, guides you to mirror the ``main`` branch.

.. note::

    Notice that this example is updating the FoundriesFactory repository ``containers.git``. 
    The same approach can be used to update ``lmp-manifest.git`` and ``meta-subscriber-overrides.git``.

Clone your GitHub repository and enter its directory:

.. note::

    Make sure to update the clone command with your repository URL.

.. prompt:: bash host:~$

    git clone https://github.com/<host>/<repo_name>
    cd <repo_name>

Check out the ``main`` branch.

.. prompt:: bash host:~$, auto

    host:~$ git checkout main

You must store workflow files in the ``.github/workflows/`` directory of your repository.

.. prompt:: bash host:~$, auto

    host:~$ mkdir -p .github/workflows/

Finally, create the file ``mirror.yml`` and make sure you update the ``<FACTORY-NAME>`` with your Factory Name.

``.github/workflows/mirror.yml``:

.. code-block:: YAML

      name: Mirroring
      
      on: [push]
      
      jobs:
        to_foundries:
          runs-on: ubuntu-20.04
          steps:
            - uses: actions/checkout@v2
              with:
                fetch-depth: 0
            - uses: foundriesio/mirror-action@main
              with:
                REMOTE: "https://source.foundries.io/factories/<FACTORY-NAME>/containers.git"
                GIT_ACCESS_TOKEN: ${{ secrets.GIT_ACCESS_TOKEN }}
                PUSH_ALL_REFS: "false"

.. warning::

    ``PUSH_ALL_REFS`` is **false**.
    If **true**, it synchronizes all branches.

.. warning::

    Make sure you backup any content in your FoundriesFactory repo you want to preserve.
    This action can completely replace all branches.

Add the changed files, commit and push to your GitHub_ repository:

      .. prompt:: bash host:~$, auto

          host:~$ git add .github/workflows/mirror.yml
          host:~$ git commit -m "Adding Mirror Action"
          host:~$ git push

GitHub Action
^^^^^^^^^^^^^

Once ``mirror.yml`` is in place, every change to the configured branch will trigger a GitHub Action that mirrors it to you FoundriesFactory Repo.

You can find the GitHub_ Action by clicking on :guilabel:`Actions`:

.. figure:: /_static/userguide/mirror-action/mirror-action-github-action.png
   :width: 900
   :align: center

   GitHub Action

There, you can find a list of Actions as well as inspect each one.

.. figure:: /_static/userguide/mirror-action/mirror-action-github-action-list.png
   :width: 900
   :align: center

   GitHub Action list

Your FoundriesFactory and GitHub hosted repos should look the same.

.. figure:: /_static/userguide/mirror-action/mirror-action-github-compare.png
   :width: 900
   :align: center

   FoundriesFactory and GitHub_

Configuring Bitbucket
---------------------

Go to the source repo on Bitbucket and click on :guilabel:`Pipelines`:

.. figure:: /_static/userguide/mirror-action/bitbucket-pipelines.png
   :align: center

   Bitbucket Pipelines

Select the ``Starter pipeline``:

.. figure:: /_static/userguide/mirror-action/bitbucket-pipelines-start.png
   :align: center

   Bitbucket Starter Pipeline

Replace the default content with the following:

.. code-block:: YAML

   pipelines:
     default:
       - step:
          name: Mirror to source.foundries.io
          image: alpine/git:latest
          script:
            - git push https://$GIT_ACCESS_TOKEN@source.foundries.io/factories/<factory-name>/<repo-name>.git --all

.. note::
   Make sure to provide the ``GIT_ACCESS_TOKEN`` generated in :ref:`ug-mirror-token` and replace ``<factory-name>`` and ``<repo-name>``.

Click on :guilabel:`Commit file` to enable this pipeline.

After this, every push to the Bitbucket mirrors all branches to ``source.foundries.io``, and triggers builds for the branches enabled in your Factory.

.. tip::

   This pipeline can be customized to mirror only specific branches as needed for your development.

.. _GitHub: https://github.com/
.. _Bitbucket: https://bitbucket.org
