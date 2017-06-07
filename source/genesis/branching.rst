.. _genesis-branching:

Genesis Branch Management
=========================

.. todo:: Add a few good diagrams.

This document defines the rules governing the branches in Genesis Git
repositories, and what you can expect from them.

Why Have Branching Rules?
-------------------------

The short answer is that it's the only way to keep things working
while staying close to our upstream projects' latest versions.

The details are given below in :ref:`branching-rationale`.

.. _branching-repo:

Genesis and Repo Primer
-----------------------

Below sections describe the branches in the Genesis manifest and
source code repositories, and how they are related. Before getting
there, this section gives some background on how Genesis uses Repo,
which may make that explanation clearer.

As described in :ref:`genesis-getting-started`, every Genesis
installation contains multiple `Git <https://git-scm.com/>`_
repositories, which are managed by a *manifest file* in a `Repo
<https://gerrit.googlesource.com/git-repo/>`_ *manifest repository*.

The name of the manifest repository is ``genesis-sdk-manifest``. It's
a Git repository, just like any of the source code repositories. While
installing Genesis, you passed `repo init`_ a URL for the manifest
repository.  The manifest repository is special, in that it contains
an XML manifest file, named ``manifest.xml``, which describes all of
the other Git repositories in the Genesis installation. After ``repo
init``, you ran `repo sync`_, which parsed the manifest file and
cloned all of the other Genesis repositories as instructed by its
contents.

The manifest file contains:

- a list of *remotes*, each of which specifies a base URL where other
  Genesis Git repositories are hosted.
- a list of *projects*, each of which specifies a Git repository to
  clone, along with a remote to pull it from, and a revision to check
  out in the local clone.

An example manifest repository, its manifest file, and the manifest
file's contents are as follows.

.. figure:: /_static/genesis/manifest-example.svg
   :alt: Example Genesis manifest.

Since the ``genesis-sdk-manifest`` repository is a Git repository, it
can, and does, contain multiple branches:

- one branch named ``master``, which tracks *trunk development*, or
  the latest changes.
- a series of *monthly snapshot branches* named ``YY.MM``, each of
  which tracks the state of development in month MM of year YY.

For example, the ``17.05`` monthly snapshot branch in the manifest
repository contains a manifest file which tracks the work done in May
2017 for the Genesis source code repositories. Similarly, the
``17.06`` branch in the manifest repository contains a manifest
tracking June 2017.

The other (non-manifest) Genesis Git repositories have branches named
``ltd-YY.MM``. These contain development work for month MM of year YY.

.. _branching-trunk:

Trunk Development
-----------------

.. note::

   The important things to know are:

   - The ``master`` branch in the :ref:`manifest repository
     <branching-repo>` tracks the **latest** monthly ``ltd-YY.MM``
     branches in the other Genesis repositories.

   - Each month, Genesis repositories with upstreams, like Zephyr and
     mcuboot, **will** `rebase`_ **onto new upstream baseline
     commits** when new monthly branches are cut.

   - Currently, updates to Genesis repositories without upstreams are
     always `fast-forward`_, even when new branches are cut. However,
     in the future, these may also rebase.

As described above, the ``master`` branch in the
``genesis-sdk-manifest`` repository tracks the very latest
development.

.. highlight:: sh

Thus, to check out the very latest Genesis, you can run::

  mkdir genesis && cd genesis
  repo init -u https://github.com/linaro-technologies/genesis-sdk-manifest
  repo sync

The ``repo init`` line clones a local manifest repository in
``genesis/.repo/manifests``, and creates and checks out a branch
called ``default`` that tracks ``master`` in the remote manifest
repository. The ``repo sync`` line fetches the latest changes in this
``master`` branch, parses the resulting XML manifest file, and updates
the local repositories based on its new contents.

.. highlight:: xml

Continuing the above example, in May 2017, the manifest file in the
manifest repository's ``master`` branch might look like this::

  <manifest>
    <remote name="ltd" fetch="https://github.com/linaro-technologies"/>

    <project name="zephyr" remote="ltd" revision="ltd-17.05"/>
    <project name="zephyr-fota-hawkbit" remote="ltd" revision="ltd-17.05"/>
    <!-- Other projects, etc. -->
  </manifest>

Running ``repo sync`` again during the same month will fetch changes
from the same upstream ``ltd-17.05`` branches, and attempt to rebase
any locally checked out branches on top of them.

At the end of each month, the ``master`` branch in the manifest
repository is updated so its manifest file synchronizes from the next
month's branches.

Thus, in the beginning of June 2017, the manifest file is updated to
look like this::

  <manifest>
    <remote name="ltd" fetch="https://github.com/linaro-technologies"/>

    <project name="zephyr" remote="ltd" revision="ltd-17.06"/>
    <project name="zephyr-fota-hawkbit" remote="ltd" revision="ltd-17.06"/>
    <!-- Other projects, etc. -->
  </manifest>

Running ``repo sync`` after this happens fetches and synchronizes your
local trees with the ``ltd-17.06`` branches in each of the Genesis
projects named in the manifest. (See `repo sync`_ for
details.)

.. warning::

   When this happens, **upstream Git history is rewritten** for
   Genesis repositories which have an upstream, like Zephyr and
   mcuboot. This happens because the next month's development branch
   is rebased onto a new baseline commit from upstream.

   For more information, see :ref:`branching-sauce`.

.. _branching-monthly:

Monthly Snapshot Branches
-------------------------

.. note::

   The important things to know are:

   - Each ``YY.MM`` branch in the :ref:`manifest repository
     <branching-repo>` tracks the monthly ``ltd-YY.MM`` branches in
     each of the other Genesis repositories.

   - Running ``repo sync`` with this manifest branch results in
     `fast-forward`_ changes only in upstream repositories.

   - At the end of the month, **upstream development stops** in all
     of these snapshot branches. You need to update to a newer
     manifest branch to get more recent changes.

As described above, the manifest repository has multiple ``YY.MM``
branches, each of which tracks develoment in month MM of year YY,
e.g. 17.05 for May of 2017.

.. highlight:: sh

To check out one of these monthly snapshots, run::

  mkdir genesis && cd genesis
  repo init -b YY.MM -u https://github.com/linaro-technologies/genesis-sdk-manifest
  repo sync

This clones local repositories tracking ``ltd-YY.MM`` branches.
Running `repo sync`_ again later fetches the latest ``ltd-YY.MM``
branches from remote repositories, and attempts to `rebase`_ any
locally checked out branches on top of the latest from upstream.

You can sync the latest changes to upstream repositories using the
current month's snapshot branch. All updates to remote repositories
will be fast-forward changes only. However, **updates will stop after
the month ends** and trunk development continues on new branches.

You can continue using Genesis at your site for as long as you'd like,
even when you're using a monthly snapshot manifest branch. However, to
fetch new updates from Linaro Technologies Division after the month
ends, you need to update your manifest repository to sync from more
recent development branches. You can do this using an existing Genesis
installation directory; **you do not need to create a new Genesis
directory to update your manifest repository branch**.

For example, if you have the ``17.05`` manifest branch checked out,
and you want to update to ``17.07``, you can run this from your
existing Genesis installation directory::

  repo init -b 17.07 -u https://github.com/linaro-technologies/genesis-sdk-manifest
  repo sync

.. warning::

   When changing manifest branches, you may synchronize based on
   upstream repository changes that are not fast-forward updates to
   what you have already cloned. This may rewrite Git history in your
   local repositories. Be careful!

   You can use ``repo sync -n`` to fetch changes from the network
   only, without updating your working directories. See
   :ref:`genesis-repo` for more information.

Monthly Baseline Rebases
------------------------

As noted above, some repositories have their history rewritten when
new monthly development branches are cut. This currently only happens
to repositories which have upstreams, namely Zephyr and mcuboot.

For example, in May 2017, the ``zephyr`` repository tracked the
``ltd-17.05`` branch in the Linaro Technologies Division Zephyr Git
tree. When development moved to the ``ltd-17.06`` branch in early June
2017, the ``zephyr`` repository was updated so that Linaro
Technologies Division changes to the mainline Zephyr source code start
at a new **baseline commit** in the upstream repository's mainline
(master) branch.

When a new baseline commit is established, the history for the commits
that LTD added to the upstream branch is rewritten and cleaned up
(squashing commits, removing hacks that are no longer needed,
etc.). See :ref:`branching-sauce`, below, for rules which make it easy
to see which commits those are.

What about Upstream Releases?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We don't currently take baseline commits in any LTD branches from
upstream release branches. That is, both trunk development and monthly
snapshots are based on commits in upstream master branches.

However, Genesis may cherry-pick or otherwise merge in changes that
went to upstream release branches during mainline development, which
then end up in that month's snapshot branch.

.. _branching-sauce:

Extra Rules For Repositories with Upstreams
-------------------------------------------

.. note::

   The important thing to know is:

   **When Linaro Technologies Division adds patches to a repository
   with an upstream, we add an "LTD" tag in the Git shortlog to mark
   the commit as currently LTD-specific**.

These tags are called "sauce tags".

Here is list of sauce tags, with a brief summary of their purposes:

- [LTD toup]: patches that want to go upstream, and revisions to them
- [LTD noup]: patches needed by LTD, but not for upstream
- [LTD mergeup]: merge commits from upstream into an LTD tree
- [LTD temphack]: patches needed temporarily until some underlying code
  is fixed or refactored upstream
- [LTD fromtree]: patches cherry-picked from upstream (when they're
  only available in a newer version that can't be merged)
- [LTD fromlist]: patches propose for upstream that are under discussion
  and are still being merged, and revisions to them.

More detailed rules for each sauce tag follow below.

[LTD toup]

    Use this for patches that are submitted upstream. Also use this
    for subsequent revisions to the LTD branch which follow upstream
    review, and make it possible to `autosquash
    <https://git-scm.com/docs/git-rebase>`_ them together in the next
    baseline rebase.

    For example, let's take this series posted upstream::

      boards: arm: add sweet_new_board
      samples: http_client: support sweet_new_board

    The shortlogs in the master-upstream-dev branch should be::

      [LTD toup] boards: arm: add sweet_new_board
      [LTD toup] samples: http_client: support sweet_new_board

    Then, after rebasing the review series in response to changes
    requested to the "add sweet_new_board" patch, add another commit
    to master-upstream-dev that makes the same change, like this::

      [LTD toup] boards: arm: add sweet_new_board
      [LTD toup] samples: http_client: support sweet_new_board
          (other commits in between)
      squash! [LTD toup] boards: arm: add sweet_new_board

    When the patches are merged into upstream master and it's time to
    merge that into master-upstream-dev, first propose a revert, then
    do the merge, like so::

      [LTD toup] boards: arm: add sweet_new_board
      [LTD toup] samples: http_client: support sweet_new_board
          (...)
      squash! [LTD toup] boards: arm: add sweet_new_board
          (...)
      Revert "[LTD toup] samples: http_client: support sweet_new_board"
      Revert "[LTD toup] boards: arm: add sweet_new_board"
          (...)
      Merge master into master-upstream-dev

[LTD noup]

    Use this if the patch isn't upstreamable for whatever reason, but
    it's still needed in the LTD trees. Use good judgement between
    this and [LTD temphack].

[LTD mergeup]

    Use this for merge commits from upstream into an LTD tree.

[LTD temphack]

    Use this for patches which "get things working again", but are
    unacceptable to upstream, and will be dropped at some point when
    rebasing to a new baseline commit.

    For example, use this if the patch wraps new code added upstream
    with ``#if 0 ... #endif`` because it broke something, while a
    better fix is being worked out.

[LTD fromtree]

    When patches are cherry-picked from a later upstream version. **Do
    not rewrite upstream's history with this tag** when merging
    upstream master into LTD master-upstream-dev.

[LTD fromlist]

    When you've cherry-picked a commit proposed for inclusion
    upstream. Note that if you want to include changes to that patch
    made during review, follow the same autosquash rules as [LTD
    toup].

.. _branching-rationale:

Appendix: Branch Management Rationale
-------------------------------------

This section provides a rationale for why these rules exist.

There are two "types" of repository in a Genesis installation:

- Projects which have an external upstream, namely Zephyr and
  mcuboot.
- Projects which are developed for Genesis, and which have no external
  upstream, like the one containing the documentation you're reading
  now.

Rather than cloning the upstream versions of the Zephyr and mcuboot
repositories in a Genesis installation, Linaro Technologies Division
maintains its own trees. This is for two reasons.

1. It allows us to keep track of known-good revisions that work well
   with Genesis.

2. It gives us a place to carry out our own internal development on
   these repositories.

Changes flow in both directions between the LTD trees and the upstream
trees. In one direction, we're constantly upstreaming these changes as
we add features, fix bugs, etc. In the other, we're keeping track of
what's going on upstream, and merging in new patches as they arrive
and are tested. We also sometimes need to keep some temporary
solutions or patches in our trees which aren't useful for upstream.

While all of this is going on in repositories with an upstream, the
Genesis-only repositories are evolving too, both to use those new
features added in Zephyr and mcuboot, and as they're being developed
in their own right.

This gets complicated, and some extra process is necessary to keep
things working smoothly over time.

The branching rules manage development in a way that allows:

- Genesis users to see clearly what the differences are between the upstream
  and Genesis versions of each repository,
- Genesis developers to stage local and integrate upstream changes,
- Continuous Integration to track versions which should work together
  for testing and test report generation,
- Genesis snapshots and releases to track the state of development
  over time, allowing comparisons between versions.

.. _repo init:
   https://source.android.com/source/using-repo#init

.. _repo sync:
   https://source.android.com/source/using-repo#sync

.. _rebase:
   https://git-scm.com/book/en/v2/Git-Branching-Rebasing

.. _fast-forward:
   https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
