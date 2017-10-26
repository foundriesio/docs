.. _zephyr-branching:

Branch Management
=================

.. todo:: Add a few good diagrams.

This document defines the rules governing the branches in the
Zephyr microPlatform Git repositories, and what you can expect from them.

.. note:: To keep things simple, we'll use the public repositories on GitHub.
          The rules are the same for subscriber repositories.

Why Have Branching Rules?
-------------------------

The short answer is that it keeps things working while patches flow
up- and downstream, and as we periodically rebase microPlatform
patches on our upstream projects' latest versions.

The details are given below in :ref:`zephyr-branching-rationale`.

.. _zephyr-branching-repo:

Zephyr microPlatform and Repo Primer
------------------------------------

This section describes `Repo`_ and how the Zephyr microPlatform uses it.
If you're unfamiliar with Repo, it may make later explanations
clearer.

A Zephyr microPlatform installation contains multiple `Git`_
repositories, which are managed by a *manifest file* in a Repo
*manifest repository*.

The manifest repository's name is ``zmp-manifest``. It's a Git
repository, just like any of the source code repositories. When
:ref:`installing the Zephyr microPlatform <zephyr-install>`, `repo
init`_ is given the URL for the manifest repository (either a
subscriber or public version).

The manifest repository contains a manifest file, named
``default.xml``.  This file describes the other Git repositories in
the Zephyr microPlatform installation, and their metadata. During
installation, `repo sync`_ is run after ``repo init``. This clones the
other repositories according to the contents of the manifest.

Roughly speaking, the manifest file contains:

- *remotes*, which specify where Zephyr microPlatform repositories are
  hosted.
- *projects*, which specify the Git repositories that make up the
  microPlatform, along with the remotes to fetch them from, and Git
  branches to check out.

Here is an example manifest file:

.. figure:: /_static/zephyr/manifest-example.svg
   :alt: Example Zephyr microPlatform manifest.

Since the ``zmp-manifest`` repository is a Git repository, it
can, and does, contain multiple branches:

- One ``master`` branch, which tracks the latest development.
- Several *monthly working branches* with names that look like
  ``YY.MM``, each of which tracks the state of development in month
  ``MM`` of year ``YY``. For example, the ``17.10`` manifest branch
  tracks development from October 2017.  Similarly, the ``17.11``
  manifest branch tracks November 2017.

The other (non-manifest) Zephyr microPlatform Git repositories have
branches named ``osf-YY.MM``. They also track month ``MM`` of year
``YY``. The ``osf-`` makes it clear they come from Open Source
Foundries, and not, for example, you.

.. important:: Monthly working branches are **not** releases. The
               Zephyr microPlatform is continuously developed and
               released to subscribers, and is released on a fixed
               timeline to the public. The monthly working branches
               exist mostly to preserve history despite rebases in
               some repositories.

The current month's branches can change as development proceeds. Older
monthly branches are left as-is as a record of the past.

.. _zephyr-branching-trunk:

Continuous Development
----------------------

.. note::

   The important things to know are:

   - The ``master`` branch in the :ref:`manifest repository
     <zephyr-branching-repo>` always tracks the current month's
     ``YY.MM`` branch. This means ``master`` always tracks the
     **latest** monthly ``osf-YY.MM`` branches in the other Zephyr
     microPlatform repositories.

   - Each month, Zephyr microPlatform repositories with upstreams,
     like Zephyr and mcuboot, `rebase`_ **onto new upstream baseline
     commits** when new monthly branches are cut.

   - Currently, Zephyr microPlatform repositories without upstreams
     always get `fast-forward`_ updates, even when new branches are
     cut.

.. highlight:: sh

When you installed the Zephyr microPlatform, you ran something like
this::

  mkdir zmp && cd zmp
  repo init -u https://github.com/OpenSourceFoundries/zmp-manifest
  repo sync

Without a ``-b`` argument, ``repo init`` looks in the ``master``
branch of the manifest repository given in the ``-u`` argument. This
checks out the manifest file in the master branch of the manifest
repository and puts it in a hidden ``.repo`` subdirectory of ``zmp``.

The ``repo sync`` line parses the manifest file in the ``.repo``
directory and clones the repositories it names as projects, then
checks them out locally in ``zmp``.

Running ``repo sync`` again later on in the same month fetches changes
from the same upstream ``osf-YY.MM`` branches, and attempts to rebase
any locally checked out branches on top of them.

At the end of each month, the ``master`` branch in the manifest
repository is updated so its manifest file synchronizes from the next
month's ``osf-YY.MM`` branches.

Running ``repo sync`` after this happens fetches and synchronizes your
local trees with the new branches in each of the Zephyr microPlatform
projects.

.. warning::

   When the new monthly branches are cut, **upstream Git history is
   rewritten** for Zephyr microPlatform repositories which have an
   upstream, like Zephyr and mcuboot. This happens because the next
   month's development branch is rebased onto a new baseline commit
   from upstream.

   If you're concerned about the effects of the rebase, use ``repo
   sync -n`` to fetch OSF changes from the network, but leave local
   working trees unchanged.

   For more information on tracking the effects of rebases, see
   :ref:`zephyr-branching-sauce`.

.. _zephyr-branching-monthly:

Monthly Working Branches
------------------------

.. note::

   The important things to know are:

   - It's possible, but not recommended, to use ``YY.MM`` manifest
     branches directly when running ``repo init``.

   - Each ``YY.MM`` branch in the :ref:`manifest repository
     <zephyr-branching-repo>` only tracks the monthly ``osf-YY.MM``
     branches in the other Zephyr microPlatform repositories.

   - At the end of the month, **upstream development stops** in all of
     the ``osf-YY.MM`` branches. You would need to update to a newer
     manifest branch to get more recent changes. By contrast, the
     ``master`` manifest branch always tracks the latest development
     by switching to the next month's ``osf-YY.MM`` branches.

.. highlight:: sh

It's possible to directly use a ``YY.MM`` manifest branch, like so::

  mkdir zmp && cd zmp
  repo init -b YY.MM -u https://github.com/OpenSourceFoundries/zmp-manifest
  repo sync

This clones local repositories tracking ``osf-YY.MM`` branches.
Running `repo sync`_ again later fetches the latest ``osf-YY.MM``
branches from remote repositories, and attempts to `rebase`_ any
locally checked out branches on top of the latest from upstream.

However, updates to ``osf-YY.MM`` branches **stop after the month
ends**, and development moves on to new branches.

Monthly Baseline Rebases
------------------------

As noted above, repositories with upstreams have their history
rewritten when new monthly branches are cut.

For example, in October 2017, development in the ``zephyr`` repository
happened in the ``osf-17.10`` branch. When the ``osf-17.11`` branch
was created in early November 2017, changes made by Open Source
Foundries were rebased onto a new **baseline commit** in the upstream
Zephyr repository.

When this happens, OSF-specific history is rewritten and cleaned up:
earlier versions of patches that were merged upstream are cleaned up,
hacks that are no longer needed are removed, etc. Upstream history is
never changed.

Commits made by Open Source Foundries have tags in their Git shortlogs
so they're easy to spot. See :ref:`zephyr-branching-sauce` below for
details.

What about Upstream Release Branches?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We don't choose baseline commits in any OSF branches from upstream
release branches.

This is because the Zephyr microPlatform is based on continuous
updates to the latest upstream software.

.. _zephyr-branching-sauce:

Sauce Tags for OSF Patches
--------------------------

.. note::

   The important thing to know is:

   When Open Source Foundries adds a patch to a repository with an
   upstream, we add an "OSF" tag in the Git shortlog to make the
   commit easy to see.

These tags are called "sauce tags". They are:

- **[OSF mergeup]**: merge commits bringing upstream changes into an OSF tree
- **[OSF fromlist]**: patches submitted to upstream for review, and
  revisions to them
- **[OSF toup]**: patches that want to go upstream, but haven't yet
- **[OSF noup]**: patches needed by OSF, but not for upstream
- **[OSF temphack]**: temporarily patches that keep things working for now
- **[OSF fromtree]**: patches cherry-picked, rather than merged, from upstream

These are the detailed rules for how sauce tags get used.

[OSF mergeup]

    Use this in the merge commit when merging an upstream branch into
    an OSF tree. The rest of the shortlog should name the upstream,
    the upstream branch being merged in, and the OSF monthly working
    branch that's getting the merge.

    For example, when merging upstream Zephyr master into
    ``osf-17.10``, the merge commit shortlog should be::

      [OSF mergeup] Merge 'zephyrproject-rtos/master' into osf-17.10

[OSF fromlist]

    Use this for commits submitted to upstream for review that should
    be merged into an OSF branch right away, and can't wait to be
    merged upstream and then brought in via mergeup.

    As a result of review, you'll need to make changes to your
    series. Keep ``osf-YY.MM`` up to date by reverting the first
    version of your series, then adding the next version on top.

    For example, let's say you post version 1 (v1) of these patches
    upstream::

      [OSF fromlist] net: lwm2m: add the finest IPSO objects        # v1
      [OSF fromlist] net: lwm2m: fit in 1K RAM                      # v1

    Then, as a result of review, you need to re-work your series. Keep
    the OSF branch up to date by reverting your patches in reverse
    order, then adding the new versions on top, like this::

      Revert "[OSF fromlist] net: lwm2m: fit in 1K RAM"             # revert v1
      Revert "[OSF fromlist] net: lwm2m: add cool new IPSO object"  # revert v1
      [OSF fromlist] net: lwm2m: add cool new IPSO object           # add v2
      [OSF fromlist] net: lwm2m: fit in 1K RAM                      # add v2

    Finally, after your series is merged upstream, revert the final
    fromlist version before doing the next mergeup, like this::

      Revert "[OSF fromlist] net: lwm2m: fit in 1K RAM"             # revert v2
      Revert "[OSF fromlist] net: lwm2m: add cool new IPSO object"  # revert v2
      [OSF mergeup] Merge 'zephyrproject-rtos/master' into osf-17.10

    Keeping these records makes it much easier to do mergeups, and to
    rebase the OSF patches at the end of the month.

[OSF toup]

    Use this for patches that should be submitted upstream, but aren't
    quite ready yet.

    Here are some hypothetical examples::

      [OSF toup] boards: arm: add sweet_new_board
      [OSF toup] samples: http_client: support sweet_new_board

    If toup patches are posted upstream and merged, this needs to be
    recorded before merging upstream master into ``osf-YY.MM``.  Do
    this the same way as fromlist patches, by reverting the toup
    patches in reverse order before doing the next mergeup, like
    this::

      [OSF toup] boards: arm: add sweet_new_board
      [OSF toup] samples: http_client: support sweet_new_board
          (...)
      Revert "[OSF toup] samples: http_client: support sweet_new_board"
      Revert "[OSF toup] boards: arm: add sweet_new_board"
          (...)
      [OSF mergeup] Merge 'zephyrproject-rtos/master' into osf-YY.MM

[OSF noup]

    Use this if the patch isn't upstreamable for whatever reason, but
    it's still needed in the OSF trees. Use good judgement between
    this and [OSF temphack].

[OSF temphack]

    Use this for hot-fix patches which make things work, but are
    unacceptable to upstream, and will be dropped at some point when
    rebasing to a new baseline commit.

    For example, use this if the patch wraps new code added upstream
    with ``#if 0 ... #endif`` because it broke something, while a
    better fix is being worked out.

[OSF fromtree]

    Use this for patches which are cherry-picked from a later upstream
    version. This should be used sparingly; **we strongly prefer to do
    mergeups instead**.

    The only good reason to use this is to bring in something
    essential when earlier upstream patches break something.

    Revert fromtree patches before the next mergeup.

----

.. _zephyr-branching-rationale:

Appendix: Branch Management Rationale
-------------------------------------

This is a detailed rationale for why these rules exist.

There are two "types" of repository in a Zephyr microPlatform installation:

- Projects which have an external upstream, like Zephyr and
  mcuboot.
- Projects which are developed for the Zephyr microPlatform, and which have no
  external upstream, like

Rather than cloning the upstream versions of the Zephyr and mcuboot
repositories in a Zephyr microPlatform installation, Open Source
Foundries maintains its own trees. This is for two reasons.

1. It lets us track known-good revisions, especially when they include
   OSF patches.

2. As active contributors to these projects, it gives us a place to
   carry out our own development.

We're constantly upstreaming features, bug fixes, etc. We're also
constantly tracking upstream and merging updates after they pass
continuous testing. We also sometimes need to keep some temporary
solutions or patches in our trees which aren't useful for upstream,
but are important to our users (i.e. you!).

While this happens, Zephyr microPlatform-only repositories are also
changing, both to track changes from upstream, and in their own right.

This all gets complicated, and the branching rules help keep things
working smoothly:

- Users can see differences between upstream and Zephyr microPlatform
  repositories clearly.
- Developers can stage local and integrate upstream changes into
  Zephyr microPlatform branches.
- Continuous Integration can track and test incoming changes.
- Monthly working branches serve as a permanent record despite
  histories which rebase.

.. _Git: https://git-scm.com/

.. _Repo: https://gerrit.googlesource.com/git-repo/

.. _repo init:
   https://source.android.com/source/using-repo#init

.. _repo sync:
   https://source.android.com/source/using-repo#sync

.. _rebase:
   https://git-scm.com/book/en/v2/Git-Branching-Rebasing

.. _fast-forward:
   https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
