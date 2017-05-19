.. highlight:: none

.. _genesis-branching:

Genesis Branch Management
=========================

.. todo:: Add a few good diagrams.

As described in :ref:`genesis-getting-started`, every Genesis
installation contains multiple `Git <https://git-scm.com/>`_
repositories, which are managed by an XML file in a `repo
<https://gerrit.googlesource.com/git-repo/>`_ manifest repository.

This document defines the rules governing the branches in these
repositories, and what you can expect from them.

Why Have Branching Rules?
-------------------------

The short answer is that it's the only way to keep things working
while staying close to our upstream projects' latest versions.

The details are given below in :ref:`branching-rationale`.

Branch Names and Rules
----------------------

The Genesis SDK manifest repository (that's the repository with the
XML file naming all the "real" repositories) has multiple branches:

- one branch named ``master``, which tracks the latest development,
  and
- a series of branches named ``YY.MM``, which track the state of
  development in month MM of year YY. For example, the 17.05 branch
  tracks development in May 2017.

These branches have different rules, and you can expect different
things from them.

Trunk Development
~~~~~~~~~~~~~~~~~

The ``master`` branch in the manifest repository tracks the very
latest development.

Thus, to check out the very latest Genesis, you can run::

  mkdir genesis && cd genesis
  repo init -u https://github.com/linaro-technologies/genesis-sdk-manifest
  repo sync

(This clones a local manifest repository in ``.repo/manifests``, and
creates and checks out a branch called ``default`` that tracks
``master`` in the remote repository.)

The rules for the checked out repositories are:

- Repositories which have an upstream will track the
  ``master-upstream-dev`` branch in LTD's tree.

- Genesis-only repositories will track the ``master`` branch in LTD's
  tree.

For example, the ``zephyr`` repository in this case will track the
``master-upstream-dev`` branch in the Linaro Technologies Division
Zephyr Git tree, and the ``zephyr-fota-hawkbit`` repository will track
the ``master`` branch in the LTD tree.

Using ``repo sync`` with this manifest branch always pulls the latest
trees; i.e., this manifest branch tracks mainline development.

Be aware that the ``master-upstream-dev`` **branches are rebased every
month** to start at a new **baseline commit** in the upstream
repository's mainline (master) branch.

When a new baseline commit is established, the history for the commits
that LTD added to the upstream branch is rewritten and cleaned up
(squashing commits, removing hacks that are no longer needed,
etc.). See :ref:`branching-sauce`, below, for rules which make it easy
to see which commits those are.

The ``master`` branches tracked in Genesis-only repositories will
**never be rebased**, however.

Monthly Snapshot Branches
~~~~~~~~~~~~~~~~~~~~~~~~~

As described above, the manifest repository has a series of ``YY.MM``
branches, which track develoment in month MM of year YY, e.g. 17.05
for May of 2017.

To check out one of these monthly snapshots, run::

  mkdir genesis && cd genesis
  repo init -b YY.MM -u https://github.com/linaro-technologies/genesis-sdk-manifest
  repo sync

The rules for the checked out repositories are:

- Repositories which have an upstream will track the
  ``master-upstream-dev-YY.MM`` branch in LTD's tree.

- Genesis-only repositories will track the ``master-YY.MM`` branch in
  LTD's tree.

For example, the ``zephyr`` repository in this case will track the
``master-upstream-dev-YY.MM`` branch in the Linaro Technologies
Division Zephyr Git tree, and the ``zephyr-fota-hawkbit`` repository
will track the ``master-YY.MM`` branch in the LTD tree.

No remote branches in this installation will ever be rebased. However,
**updates will stop after the month ends** and trunk rebases to new
upstream baselines.

What about Upstream Releases?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We don't currently take baseline commits in any LTD branches from
upstream release branches. That is, both trunk development and monthly
snapshots are based on commits in upstream master branches.

However, Genesis may cherry-pick or otherwise merge in changes that
went to upstream release branches during mainline development, which
then end up in that month's snapshot branch.

.. _branching-sauce:

Commit Message Rules: "Sauce Tags"
----------------------------------

Always, always, always:

**When adding commits to a repository with an upstream, add a tag in
the Git shortlog to mark it as coming from LTD**.

These "sauce tags" are:

- [LTD toup]: patches that want to go upstream, and revisions to them
- [LTD noup]: patches needed by LTD, but not for upstream
- [LTD mergeup]: merge commits from upstream into an LTD tree
- [LTD temphack]: patches needed temporarily until some underlying code
  is fixed or refactored upstream
- [LTD fromtree]: patches cherry-picked from upstream (when they're
  only available in a newer version that can't be merged)
- [LTD fromlist]: patches propose for upstream that are under discussion
  and are still being merged, and revisions to them.

These are the rules for each tag.

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
