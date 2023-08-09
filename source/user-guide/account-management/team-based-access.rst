.. _ref-team-based-access:

Team Based Factory Access
=========================

.. seealso::
   * :ref:`Account Roles <ref-account-roles>` for account management.

   * :ref:`API Scopes <ref-scopes>` for available token scopes.

.. tip::
   The FoundriesFactory® :ref:`API documentation<ref-scopes>` covers available scopes.

Larger organizations often need to restrict the access level a user has to the Factory.
For example, some users might only need access for managing devices,
while other users only need read-only access to source code.
Factory **Teams** is how FoundriesFactory enables you to control access.

A Team is comprised of:

 * **Access control**: what :ref:`scopes <ref-scopes>` are granted to the team, e.g. ``source:read``.

 * **Members**: what users belong to the team.

 * **Device groups**: what device groups belong to the team.

Once a user is assigned a team, their access will be limited to the scopes granted to that team.
Also, a user will get access to the team's device groups and their devices in accordance with the team scopes.
See :ref:`Access to Device Groups` for more details.

.. important::
   It may take a moment for changes to scope/teams to take effect.

Teams can be created by anyone with either the **Owner** or **Admin** role.
While these roles are granted read-write operations for all Factory resources by default,
checking user scope with ``fioctl users <user id>`` will return blank unless they are part of a team.
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
   :alt: Teams example: Team read-only users

.. figure:: /_static/teams-example-read-write-ci.png
   :align: center
   :scale: 80%
   :alt: Teams example: Team read-write CI users

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

.. _Access to Device Groups:

Team Based Access to Device Groups
----------------------------------
By default, a user can access:

    1. device groups they created,
    2. devices they own,
    3. devices that are in device groups they created.

A factory admin can grant a user access to any device groups.
To do so, an admin should:

    1. add a user to a team if is not a team member yet;
    2. add a device group to the team;
    3. set ``devices:*`` scopes for the team.

As a result, the user will get a permission to perform the set actions over the group and its devices.

.. note::

    The ``devices:*`` scopes determine actions team members can perform over device groups and their devices.

    *  ``devices:read`` - view device/group details and its configuration.
    *  ``devices:read-update`` - view and modify device/group details and its configuration, including config file deletion.
    *  ``devices:delete`` - delete device/group.

    See :ref:`API Scopes <ref-scopes>` for more details on the scopes.

Example
^^^^^^^

A Factory has two teams in place and one device group, ``test-lab-devices``.

Members of the "read-only-users" team have read-only access to all factory resources with one exception—device groups and devices.
They can see only the ``test-lab-devices`` group and devices included into it.

.. figure:: /_static/userguide/account-management/team-with-group-and-read-access.png
   :align: center
   :alt: "read-only-users" scopes: read-only team with a device group

The "lab-dev-users" team includes ``devices:read-update`` scope.
Therefore, members of this team can modify the ``test-lab-devices`` group and its devices.

.. figure:: /_static/userguide/account-management/team-with-group-and-write-access.png
   :align: center
   :alt: "lab-dev-users" scopes: read-update team with a device group
