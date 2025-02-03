.. _ref-team-based-access:

Team Based Factory Access
=========================

.. seealso::
   * :ref:`Account Roles <ref-account-roles>` for account management.

   * :ref:`API Scopes <ref-scopes>` for available token scopes.

.. tip::
   The FoundriesFactory™ Platform :ref:`API documentation<ref-scopes>` covers available scopes.

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

   Teams example

.. figure:: /_static/teams-example-read-only.png
   :align: center
   :scale: 80%
   :alt: Teams example: Team read-only users

   Team read-only users

.. figure:: /_static/teams-example-read-write-ci.png
   :align: center
   :scale: 80%
   :alt: Teams example: Team read-write CI users

   Team read-write CI users

A member is then added to both teams.
The member then has a combined list of scopes:

 * From read-only-users:

   * ``ci:read``
   * ``source:read``
   * ``devices:read``
   * ``targets:read``
   * ``containers:read``

 * From read-write-ci

   * ``ci:read-update``

The user now has read **and** write (update) access to the CI,
while retaining the read-only scopes for the other resources.


.. _Access to Device Groups:

Team Based Access to Device Groups
----------------------------------

.. important::
   The Device view is available for all Factory users.

By default, a user can access:

    1. device groups they created,
    2. devices they own,
    3. devices that are in device groups they created.

A factory admin can grant a user access to any device groups.
To do so, an admin should:

    1. add a user to a team if they are not yet a team member;
    2. add a device group to the team;
    3. set the ``devices:*`` scopes for the team.

As a result, the user will get permission to perform the set actions over the group and its devices.

.. note::

    The ``devices:*`` scopes determine the actions team members can perform over device groups and their devices.

    *  ``devices:read`` - permission to view the details and configuration of a device/group; set to all members of a Factory.
    *  ``devices:read-update`` - permission to modify device/group details and configuration, including config file deletion.
    *  ``devices:delete`` - Ability to delete device/group.

    See :ref:`API Scopes <ref-scopes>` for more details on the scopes.

Example
^^^^^^^

.. tip::
   Members who in no teams can **view** all devices and ci/Targets information.
   By default, they can **only modify devices created by them**.

The members of the "read-only-users" team have read-only access to all Factory resources.
This includes access for viewing all devices in a Factory.
They cannot make changes to the devices as their scope includes ``devices:read``.

.. figure:: /_static/userguide/account-management/team-with-group-and-read-access.png
   :align: center
   :alt: "read-only-users" scopes: read-only team with a device group

   read-only team with a device group

The "lab-dev-users" team includes the ``devices:read-update`` scope.
Therefore, members of this team can modify the ``test-lab-devices`` group and its devices.
They can also view all devices in a Factory, even if they are assigned to other device groups.

.. figure:: /_static/userguide/account-management/team-with-group-and-write-access.png
   :align: center
   :alt: "lab-dev-users" scopes: read-update team with a device group

   read-update team with a device group

.. _team-based-access-tuf:

Changes to TUF Root
-------------------

With Fioctl® v0.35 and newer, if someone makes changes to The Update Framework (TUF) root, others will be required to upgrade to the same version if they wish to make changes.
This is to prevent accidental eraser of the TUF keys ownership information.


.. seealso::
   :ref:`ref-troubleshooting_user-permissions`

