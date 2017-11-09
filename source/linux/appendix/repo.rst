.. _lmp-appendix-repo:

Appendix: Linux microPlatform Repo Primer
=========================================

This section describes `Repo`_ and how the Linux microPlatform uses
it. If you're unfamiliar with Repo, it may make things clearer.

A Linux microPlatform build tree installation contains multiple Git
repositories, which are managed by a *manifest file* in a Repo
*manifest repository*.

The manifest repository's name is ``lmp-manifest``. It's a Git
repository, just like any of the source code repositories. When
:ref:`installing the Linux microPlatform <linux-getting-started>`,
`repo init`_ is given the URL for the manifest repository (either a
subscriber or public version).

The manifest repository contains a manifest file, named
``default.xml``.  This file describes the other Git repositories in
the Linux microPlatform installation, and their metadata. During
installation, `repo sync`_ is run after ``repo init``. This clones the
other repositories according to the contents of the manifest.

Roughly speaking, the manifest file contains:

- *remotes*, which specify where Linux microPlatform repositories are
  hosted.
- *projects*, which specify the Git repositories that make up the
  microPlatform, along with the remotes to fetch them from, and Git
  branches to check out.

.. _Repo:
   https://gerrit.googlesource.com/git-repo/

.. _repo init:
   https://source.android.com/source/using-repo#init

.. _repo sync:
   https://source.android.com/source/using-repo#sync
