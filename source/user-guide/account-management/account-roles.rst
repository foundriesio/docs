.. _ref-account-roles:

Factory Account Roles
=====================

A role consists of permission levels for **account management** you assign to a *member* of your Factory.

 .. csv-table:: Roles and Permission Summary
   :header: "Role", "Edit Members", "Edit Teams", "Subscription", "PKI", "Waves"

   "Owner", "X", "X", "X", "X", "X"
   "Admin", "X", "X", ,"X", "X"
   "Accounting", , "X", , ,
   "Member", , , , ,
   
There are four roles available. The two core roles being:

* **Member**: Default when adding new users, with no permissions.
* **Owner**: The user account that created the factory has the initial "Owner" role, with full permission to:
  
  - add and update members
  - manage teams
  - manage the Factory subscription plan
  - register, delete, and rename all devices
  - manage the Factory's :term:`Public Key Infrastructure (PKI)<PKI>` and create Waves.
  
The remaining two each get a subset of the **Owner** permissions.

* **Admin**: Add and update members, :ref:`manage teams <ref-team-based-access>` and device groups, manage PKI, and create Waves.
* **Accounting** limited to managing the :ref:`Factory plan <ref-subscription-and-billing>`.

.. tip::
    No limits exist on how many members can share a role.
    For example, more than one member can have the **Owner** role.
    However, a single member has only one role at a time.

By default, users can access device groups they created, the devices in them, and the devices they own.

.. seealso::
   :ref:`Team Based Factory Access <ref-team-based-access>` for permissions related to development and device management.

How it Works: Walk Through
--------------------------

Upon creating a Factory, the creator automatically gets assigned the role of owner.
The owner then sends invites via the :guilabel:`Member` tab on their Factory page:

.. figure:: /_static/user-guide/account-management/invite-members.png
   :align: center
   :alt: sending member invites

   Inviting members to Factory

.. tip::
   When inviting members, you can also select any teams to assign them automatically.

On creating an account and accepting the invitation, members have no account management permissions.

From the :guilabel:`Member` tab, the owner selects members from the table, and clicks on :guilabel:`Role...`,
and assigns the desired role:

.. figure:: /_static/user-guide/account-management/member-list.png
   :align: center
   :alt: UI, changing member role

   Changing member role

From here, roles can be changed anytime.

