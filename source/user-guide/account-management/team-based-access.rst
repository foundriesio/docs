.. _ref-team-based-access:

Team Based Factory Access
=========================

.. tip::
   The FoundriesFactory :ref:`API documentation<ref-scopes>` covers available scopes.

Larger organizations often need to restrict the access level a user has to the Factory.
For example, some users might only need access for managing devices,
while other users only need read-only access to source code.
Factory **Teams** is how FoundriesFactory enables you to control access.

A Team is comprised of:

 * **Access control** - What :ref:`scope <ref-scopes>` is granted to
   the team, e.g. ``source:read``.

 * **Members** - What users belong to the team.

Once a user is assigned a team, their access will be limited to the scope granted to that team. 

.. important::
   It may take a moment for changes to scope/teams to take effect.

Teams can be created by anyone with either the **Owner** or **Admin** role.
Additionally, these roles are granted read-write operations for all Factory resources by default,
but when checking user scope with ``fioctl users <user id>`` ,
it will return blank unless they are part of a team.
Members with devices may manage their own with read-write access.

.. tip::
   You can always edit a Team, changing the name, description, or scope.


How it Works: Walk Through
--------------------------

API authorization can be thought of having the following decision tree:

 * Is the user a :ref:`member <ref-account-roles>` of the Factory this API is targeting?

   * If yes, combine scopes of each team the user is a member of where:

     * If scope was empty, the user can now access the resource.
     * If not empty, the authorization code asserts the user now has the required scope.

Example
^^^^^^^

A Factory has two teams in place.
Team "read-only-users" is restricted to read-only access; members can see everything, but can not make changes.
Team "read-write-ci" can do CI read-write operations:

.. figure:: /_static/teams-example.png
   :align: center
   :alt: Teams example

.. figure:: /_static/teams-example-read-only.png
   :align: center
   :scale: 80%
   :alt: Teams example - Team read-only users

.. figure:: /_static/teams-example-read-write-ci.png
   :align: center
   :scale: 80%
   :alt: Teams example - Team read-write CI users

A member is then added to both teams.
The member then has a combined list of scopes:

 * From read-only-users:

   * ci:read
   * source:read
   * devices:read
   * targets:read
   * containers:read

 * From read-write-ci

   * ci:read-update

The user now has read **and** write (update) access to the CI,
while retaining the read-only scopes for the other resources.

.. seealso::
   * :ref:`Account Roles <ref-account-roles>` for account management.

   * :ref:`API Scopes <ref-scopes>` for available scopes.

