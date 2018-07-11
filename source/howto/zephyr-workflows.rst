.. _howto-zephyr-workflows:

Zephyr microPlatform Workflows HOWTO
====================================

This page describes the workflows for developing and deploying
embedded applications with the Zephyr microPlatform. It assumes that the
Zephyr microPlatform has successfully been installed as described in
:ref:`tutorial-zephyr`.

.. _howto-zephyr-repo:

Use Repo to Fetch Updates
-------------------------

The Zephyr microPlatform uses the Repo tool to manage its Git
repositories. In :ref:`tutorial-zephyr`, you used this tool to clone
these Git repositories into a Zephyr microPlatform installation
directory on a development computer. See :ref:`ref-zephyr-repo` for
more details.

After the installation, you'll continue to use Repo to fetch upstream
changes as follows.

#. Enter the ``.repo/manifests`` subdirectory of the Zephyr
   microPlatform (this is where the Repo manifest repository is
   installed on your system).

#. Use git to note the current Git commit SHA of the manifest
   repository. For example:

   .. code-block:: console

      git --no-pager log -n1 --pretty='%H'

   We'll call the current SHA ``STARTING_MANIFEST_SHA``.

#. Go back to the top level Zephyr microPlatform installation
   directory, and use Repo to sync updates:

   .. code-block:: console

      repo sync

   .. warning::

      If you make any changes to any repositories managed by Repo,
      this will attempt to rebase your local branches, which **can
      cause conflicts**. Please see :ref:`howto-zephyr-out-of-tree`
      for more details.

      You can use ``repo sync -n`` to fetch changes only, without
      rebasing, and then use Git to inspect the differences between your
      local and the upstream branches, merge or rebase appropriately,
      etc.

      This is currently considered an advanced use case. If you are
      trying this during the beta period and you run into problems,
      please contact us.

#. After running ``repo sync``, you can use the ``zmp`` helper script
   documented above to re-build and re-test your application, and make
   adjustments.

   We recommend comparing your application with the updated version
   of the sample application you started from for relevant
   updates. This will let you adjust your application if needed to
   keep up with upstream.

If you run into problems, you can temporarily roll back to a previous
Zephyr microPlatform release as follows:

.. code-block:: console

   $ cd .repo/manifests
   $ git checkout STARTING_MANIFEST_SHA
   $ cd ../..
   $ repo sync

However, this defeats the purpose of receiving continuous updates from
Foundries.io.

.. _howto-zephyr-out-of-tree:

Managing Out of Tree Patches
----------------------------

While an upstream first approach is recommended for development, situations
come up when out-of-tree patches are necessary for a microPlatform project
such as Zephyr. `Repo`_ has built-in tooling to handle this workflow. The
``repo start`` command informs Repo that development will take place in a
given branch name for a project. Once Repo is aware there are development
branches for a project, ``repo sync`` will take care of rebasing the patch(es).

.. code-block:: console

   # work starts at latest microPlatform release
   # A fix is required in Zephyr, the patch was submitted upstream, but is
   # is still awaiting review. In the meantime, a branch can be used with:
   $ repo start github-pr-XXX zephyr
   $ cd zephyr
   # apply the patch(es) to zephyr
   $ git commit -a -m "out-of-tree patch waiting for zephyr merge #12"
   ...
   # A new update comes in for the microPlatform
   $ repo sync
   ...
   # If no merge conflicts are detected, everything is done. Otherwise
   # you will have to drop into the zephyr directory and use Git to
   # resolve the merge conflict.

.. _Repo: https://gerrit.googlesource.com/git-repo/
