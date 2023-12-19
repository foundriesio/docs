.. _ref-linux-repo:

Repo Source Control Tool
========================

This section describes `Repo`_ and how the Linux® microPlatform uses it.

A Linux microPlatform (LmP) build tree installation contains multiple Git repositories.
These are managed by a *manifest file* in a *Repo manifest repository*.

Your Factory's  manifest repository's name is ``lmp-manifest``.
In :ref:`ref-linux-building`, `repo init`_ is given the URL for the manifest repository.

The manifest repository contains a manifest file, named ``default.xml``.
This file describes the other Git repositories in the Linux microPlatform installation, and their metadata.
During installation, `repo sync`_ is run after ``repo init``.
This clones the other repositories according to the contents of the manifest.

Roughly speaking, the manifest file contains:

- *remotes*, which specify where Linux microPlatform repositories are hosted.
- *projects*, which specify the Git repositories that make up the microPlatform, along with the remotes to fetch them from, and Git branches to check out.

.. _Repo:
   https://gerrit.googlesource.com/git-repo/

.. _repo init:
   https://source.android.com/docs/setup/create/repo#init

.. _repo sync:
   https://source.android.com/docs/setup/create/repo#sync
