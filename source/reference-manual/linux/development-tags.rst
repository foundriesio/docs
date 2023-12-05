.. _ref-development-tags:

Understanding FIO Development Tags
==================================

When Foundries.io™ adds a patch to a repository with an upstream, we add a ``FIO`` tag in the Git shortlog. 
This makes the commit easier to see.
For example, in our U-Boot tree::

    [FIO internal] common: foundries.io verified boot utility

The most common tags used throughout the repositories are:

* ``[FIO fromtree]``: patches cherry-picked, rather than merged, from upstream (mainline)
* ``[FIO fromlist]``: patches submitted to upstream for review (in mailing lists, pending PRs etc.), and revisions to them
* ``[FIO toup]``: patches that want to go upstream
* ``[FIO temphack]`` or ``[FIO hack]``: temporary patches that keep things working for now, but need a better solution later for upstreaming
* ``[FIO extras]``: non-critical patches pulled in for extra, potentially useful functionality
* ``[FIO internal]``: patches needed by the LmP, not intended for upstream use
* ``[FIO squash]``: patch should be squashed with an original patch, fixing possible issues in that patch.
  This tag requires a commit message tag ``Fixes:`` to be filled out properly

There are also exceptional tags for patches that were cherry-picked/sent from/to SoC vendor forks:

* ``[FIO from<vendor_name>]``: patches cherry-picked from ``<vendor_name>`` forked tree, for example ``[FIO fromnxp]``
* ``[FIO to<vendor_name>]``: patches, that want to go to SoC vendor forked tree, for example ``[FIO tostm]``
* ``[FIO to<vendor_name>-altered]``: exceptional case, when not a whole patch was cherry-picked, but rather some parts or it was completely reimplemented.
  In this case ``-altered`` is added, for example ``[FIO fromnxp-altered]``


.. important:: When a patch is cherry-picked, the Git cherry-pick command should be invoked with ``-x`` (append commit name) parameter.
   This is so that the original commit hash is added to the new commit message.
   For example, ``cherry-picked from commit 1e24c2671acdbcf81207c43da39e09846f404dc3``.
   With a hash, tracking the original commit in a mainline/SoC vendor tree is easier.
