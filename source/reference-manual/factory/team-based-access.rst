.. _ref-team-based-access:

Team based factory access
=========================

Larger organizations often need to restrict what kind of access a
user has to their Factory. For example, some users might only need
access for managing devices. Other users might only need read-only
access to source code. Factory teams are how this can be managed.

A team consists of two things:

 * **Access control** - What :ref:`scopes <ref-scopes>` are granted to
   the team. e.g. ``source:read``.

 * **Members** - What users belong to the team.

Once a user is assigned a team, their access will be limited to the
scopes granted to that team.

How it works
------------

API authorization has a decision tree like:

 * Is user a member of the org this API is targeting?

   * Combine scopes for each team the user is a member of

     * If empty, they can access resource.
     * If not empty, the authorization code asserts the user has
       the required scope.

An example
----------

This factory has two teams in place. One team is restricted to
read-only access. Members can see everything, but not make any
changes. The 2nd team may do CI read-write operations:

.. figure:: /_static/teams-example.png
   :align: center
   :alt: Teams example

.. figure:: /_static/teams-example-read-only.png
   :align: center
   :scale: 80%
   :alt: Teams example - read-only users

.. figure:: /_static/teams-example-read-write-ci.png
   :align: center
   :scale: 80%
   :alt: Teams example - read-write ci users

If a user is added to both teams, they'll wind up with a list of
scopes like:

 * From read-only-users:

   * ci:read
   * source:read
   * devices:read
   * targets:read
   * containers:read

 * From read-write-ci

   * ci:read-update

In other words, this user will have read-write access to CI.

