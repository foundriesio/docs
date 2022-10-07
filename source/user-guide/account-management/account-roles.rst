.. _ref-account-roles:

Factory Account Roles
=====================

 
Managing and utilizing a Factory  various *roles*, regardless the number of members;


A role consists of set permission levels for **account management** that a *member* of a FoundriesFactory gets assigned.

* **Member**: Default when adding new users, with no permissions.
* **Owner**: The user account that created the factory has the initial "Owner" role, with full permission to:
  
  - add and update members
  - manage teams
  - manage the Factory subscription plan.

The remaining two each get a subset of the Owner permissions.

* **Admin**: Add and update members, and :ref:`manage teams <ref-team-based-access>`.
* **Accounting** limited to managing the :ref:`Factory plan <ref-subscription-and-billing>`.

.. tip::
    No limits exist on how many members can share a role.
    For example, more than one member can have the owner role.
    However,a single member has only one role at a time.

.. csv-table:: Roles and Permission Summary
   :header: "Role", "Edit Members", "Manage Teams", "Subscription/Billing", 

   "Owner", "X", "X", "X"
   "Admin", "X", "X",
   "Accounting", , "X"
   "Member", , ,


How it Works: Walk Through
--------------------------

Upon creating a Factory, the creator automatically gets assigned the role of owner.
The owner then sends invites via the :guilabel:`Member` tab on their Factory page:

.. figure:: /_static/userguide/account-management/invite-members.png
   :align: center
   :alt: sending member invites

.. tip::
   When inviting members, you can also select any teams to assign them automatically.

On creating an account and accepting the invitation, members have no account management permissions.

From the :guilabel:`Member` tab, the owner selects members from the table, and clicks on :guilabel:`role...`,
and assigns the desired role:

.. figure:: /_static/userguide/account-management/member-list.png
   :align: center
   :alt: UI, changing member role

From here roles can be changed anytime.

.. seealso::
   :ref:`Team Based Factory Access <ref-team-based-access>` for permissions related to development and device management.
  
