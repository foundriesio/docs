.. _ref-zephyr-branch:

Zephyr microPlatform Branches
=============================

This document describes the rules governing the branches in the
Zephyr microPlatform Git repositories, and what you can expect from them.

.. note::

   The important things to know are:

   - The ``master`` branch in the `ZmP west manifest repository`_
     always tracks the latest development.

   - Commits in the Foundries.io Zephyr and mcuboot trees
     which aren't present upstream have special tags, called
     :ref:`sauce tags <zephyr-branching-sauce>`, in their `Git`_
     shortlogs, so they can be easily identified and their purpose
     made clear.

   - When upstream projects release new versions, the Zephyr
     microPlatform branches receive non-fast-forward updates onto the
     new upstream development versions.

   - Currently, Zephyr microPlatform repositories provided by
     Foundries.io (i.e., projects without external upstreams)
     always get `fast-forward`_ updates.

Why Have Branching Rules?
-------------------------

The short answer is that it keeps things working while patches flow
up- and downstream, and as we periodically rebase microPlatform
patches on our upstream projects' latest versions.

The details are given below in :ref:`zephyr-branching-rationale`.

.. _ref-zephyr-branch-maint:

Branch Maintenance
------------------

For repositories with upstreams, like Zephyr and MCUBoot, Foundries.io
maintains some out of tree patches. To make this work
smoothly, we typically bring in upstream changes by merging into our
tree. You'll see merge commits with ``[FIO mergeup]`` in the
shortlog when this happens. See below for a complete list of sauce tags.

However, whenever the upstream releases a new version, the Foundries.io
branch history is cleaned up and re-written onto the new
development tree for the next version. This is a destructive change,
but you can always get the old version using the manifests from
previous updates.

The notes in the microPlatform update will always make it clear when
history rewrites have happened. They will also provide pointers to
commits in the new update which match the last update exactly (even
though history is different, the code will be the same). You can use
these commits as a starting point when merging the new history into
your own tree if you are also managing changes to these repositories
-- since the code is the same, the merge will succeed.

For source code repositories without upstreams, where Foundries.io
is maintaining the code, Zephyr microPlatform updates will
always contain fast-forward changes from the previous update.

.. _zephyr-branching-sauce:

Sauce Tags for Foundries.io Patches
-----------------------------------

.. note::

   The important thing to know is:

   When Foundries.io adds a patch to a repository with an
   upstream, we add an "FIO" tag in the Git shortlog to make the
   commit easy to see.

These tags are called "sauce tags". They are:

- **[FIO mergeup]**: merge commits bringing upstream changes into a
  Foundries.io tree
- **[FIO fromlist]**: patches submitted to upstream for review, and
  revisions to them
- **[FIO toup]**: patches that want to go upstream, but haven't yet
- **[FIO noup]**: patches needed by the microPlatforms, that aren't intended
  for upstream use. Avoid these if at all possible.
- **[FIO temphack]**: temporarily patches that keep things working for now,
  but need a better solution later for upstreaming.
- **[FIO fromtree]**: patches cherry-picked, rather than merged, from upstream

Detailed descriptions follow.

[FIO mergeup]

    This tags merge commits when merging an upstream branch into a
    Foundries.io tree. The rest of the shortlog names the upstream, the
    upstream branch being merged in, and the Foundries.io development branch
    that's getting the merge.

    For example, when merging upstream Zephyr master, the merge commit
    shortlog should be:

    .. code-block:: none

       [FIO mergeup] Merge 'zephyrproject-rtos/master' into remote/master

[FIO fromlist]

    This tags commits submitted to upstream for review that needed to
    be merged into a Foundries.io branch before they are accepted upstream.

    As a result of review, changes are often necessary to these
    patches. Foundries.io branches are kept up to date by reverting old
    versions, then adding the new versions on top. When the patches
    are merged upstream, the final ``[FIO fromlist]`` version is
    reverted before the next ``[FIO mergeup]``.

    As an example, consider version 1 (v1) of these patches sent
    upstream:

    .. code-block:: none

       [FIO fromlist] net: lwm2m: add the finest IPSO objects        # v1
       [FIO fromlist] net: lwm2m: fit in 1K RAM                      # v1

    Suppose the series needed changes as a result of upstream
    review. The Foundries.io branch is kept up to date by reverting the patches
    in reverse order, then adding the new versions on top, like this:

    .. code-block:: none

       Revert "[FIO fromlist] net: lwm2m: fit in 1K RAM"             # revert v1
       Revert "[FIO fromlist] net: lwm2m: add cool new IPSO object"  # revert v1
       [FIO fromlist] net: lwm2m: add cool new IPSO object           # add v2
       [FIO fromlist] net: lwm2m: fit in 1K RAM                      # add v2

    Finally, after the series is merged upstream, the final fromlist
    version is reverted the next ``[FIO mergeup]``, like this:

    .. code-block:: none

       Revert "[FIO fromlist] net: lwm2m: fit in 1K RAM"             # revert v2
       Revert "[FIO fromlist] net: lwm2m: add cool new IPSO object"  # revert v2
       [FIO mergeup] Merge 'zephyrproject-rtos/master' into remote/master

    Keeping the history of reverts makes it easy to track which
    patches are still out of tree when cleaning up history following a
    new upstream release as described above in
    :ref:`ref-zephyr-branch-maint`.

[FIO toup]

    This tags patches that should be submitted upstream, but aren't
    quite ready yet.

    Here are some hypothetical examples:

    .. code-block:: none

       [FIO toup] boards: arm: add sweet_new_board
       [FIO toup] samples: http_client: support sweet_new_board

    If ``[FIO toup]`` patches are posted upstream and merged, they are
    reverted before the next ``[FIO mergeup]``, in the same way as
    ``[FIO fromlist]`` commits. For example:

    .. code-block:: none

       [FIO toup] boards: arm: add sweet_new_board
       [FIO toup] samples: http_client: support sweet_new_board
           (...)
       Revert "[FIO toup] samples: http_client: support sweet_new_board"
       Revert "[FIO toup] boards: arm: add sweet_new_board"
           (...)
       [FIO mergeup] Merge 'zephyrproject-rtos/master' into remote/master

[FIO noup]

    This tags patches that aren't upstreamable for whatever reason,
    but are needed in the Foundries.io trees. Use good judgement between
    this and ``[FIO temphack]``.

[FIO temphack]

    This tags hot-fix patches which make things work, but are
    unacceptable to upstream, and will be dropped as soon as
    possible. For longer-term out of tree patches, use ``[FIO noup]``.

[FIO fromtree]

    This tags patches which are cherry-picked from a later upstream
    version. This is used sparingly; we prefer to do mergeups instead.

    The main (perhaps only) good reason to use this is to bring in
    something essential when other upstream patches break something,
    so an upstream merge is not possible at a particular time.

    ``[FIO fromtree]`` patches are reverted before the next mergeup.

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
repositories in a Zephyr microPlatform installation, Foundries.io
maintains its own trees. This is for two reasons.

1. It lets us track known-good revisions, especially when they include
   Foundries.io patches.

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
- The west manifest file in each microPlatform update serves as a
  permanent record despite histories which rebase.

.. _ZmP west manifest repository:
   https://github.com/foundriesio/zmp-manifest

.. _Git: https://git-scm.com/

.. _rebase:
   https://git-scm.com/book/en/v2/Git-Branching-Rebasing

.. _fast-forward:
   https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
