.. _ref-zephyr-repo:

Repo Primer for Zephyr microPlatform
====================================

This section describes `Repo`_ and how the Zephyr microPlatform uses
it. If you're unfamiliar with Repo, it may make things clearer.

Manifest Repository
-------------------

A Zephyr microPlatform installation contains multiple `Git`_
repositories, which are managed by a *manifest file* in a Repo
*manifest repository*.

The manifest repository's name is ``zmp-manifest``. It's a Git
repository, just like any of the source code repositories. When
:ref:`installing the Zephyr microPlatform <tutorial-zephyr>`, `repo
init`_ is given the URL for the manifest repository (either a
subscriber or public version).

The manifest repository contains a manifest file, named
``default.xml``.  This file describes the other Git repositories in
the Zephyr microPlatform installation, and their metadata.

Roughly speaking, the manifest file contains:

- *remotes*, which specify where Zephyr microPlatform repositories are
  hosted.
- *projects*, which specify the Git repositories that make up the
  microPlatform, along with the remotes to fetch them from, and Git
  branches to check out.

The following figure ties together the various pieces.

.. figure:: /_static/reference/manifest-example.svg
   :alt: Example Repo manifest
   :align: center
   :figwidth: 5in

Basic Repo Usage
----------------

When you installed the Zephyr microPlatform, you ran something like
this::

  mkdir zmp && cd zmp
  repo init -u https://some-url/zmp-manifest
  repo sync

This checks out the manifest file in the master branch of the manifest
repository and puts it in a hidden ``.repo`` subdirectory of ``zmp``.

During installation, `repo sync`_ is run after ``repo init``. This
parses the manifest file in the ``.repo`` directory, clones the
repositories it names as projects, then checks them out locally in
``zmp``.

Running ``repo sync`` again later on fetches changes to the manifest,
then re-synchronizes the local trees. This also attempts to rebase any
locally checked out branches.

.. warning::

   If you've got locally checked out branches when you run ``repo
   sync``, **your Git history is rewritten**. This happens because the
   local branch is rebased onto the new commit from Open Source
   Foundries.

   If you're concerned about the effects of the rebase, use ``repo
   sync -n`` to fetch changes from the network, but leave local
   working trees unchanged. You can then inspect the OSF branches and
   integrate them manually.

.. _Repo: https://gerrit.googlesource.com/git-repo/

.. _Git: https://git-scm.com/

.. _repo init:
   https://source.android.com/setup/develop/repo#init

.. _repo sync:
   https://source.android.com/setup/develop/repo#sync
