.. _ref-development-tags:

Understanding Development FIO Tags
==================================

When Foundries.io adds a patch to a repository with an upstream, we add an ``FIO``
tag in the Git shortlog to make the commit easy to see. For example, in
Foundries.io U-Boot tree::

    [FIO internal] common: foundries.io verified boot utility

The most common used tags through the Foundries.io repositories are:

* ``[FIO fromtree]``: patches cherry-picked, rather than merged, from upstream
* ``[FIO fromlist]``: patches submitted to upstream for review, and revisions to them
* ``[FIO toup]``: patches that want to go upstream, but haven't yet
* ``[FIO temphack]``: temporarily patches that keep things working for now, but need a better solution later for upstreaming
* ``[FIO extras]``: patches pulled in for specific functionality that are useful for subscribers, but not critical
* ``[FIO internal]``: patches needed by the LmP, not intended for upstream use
