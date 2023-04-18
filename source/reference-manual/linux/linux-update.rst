.. _ref-linux-update:

Updating the Linux microPlatform Core
=====================================

The FoundriesFactory® platform manifest is tailored to make consuming core platform updates easily.
At Foundries.io™, we often `release`_ Linux® microPlatform (LmP) updates as an effort to get the latest features and security fixes out to users.

.. _release:
   https://github.com/foundriesio/lmp-manifest/releases

.. note::
   You can subscribe to `Factory Notifications <https://app.foundries.io/settings/notifications/>`_ to be informed of new LmP releases.

We provide a helper script ``update-factory-manifest`` to update your Factory to a new LmP release.
This script automatically updates your manifest to the latest LmP version available if no merge conflicts are found.

Updating Your Factory
~~~~~~~~~~~~~~~~~~~~~

.. prompt:: bash

   git clone https://source.foundries.io/factories/<myfactory>/lmp-manifest.git
   git clone https://github.com/foundriesio/lmp-tools
   cd lmp-manifest/
   git checkout <branch to update>
   ../lmp-tools/scripts/update-factory-manifest

.. tip::
   We recommend testing the update in a separate branch before merging to your active branches. After testing, the changes can be merged to your development branches.

If no merge conflicts are found, this script merges your changes and pushes the updated manifest to your Factory, triggering a new platform build. Once published, the update is deployed to your devices following this tag.

.. tip::
   If something goes wrong, don’t fret! This is why we use version control!

   .. prompt:: bash

      git revert HEAD

   If there are merge conflicts, it is up to you to fix them. Do not hesitate to contact our support at http://support.foundries.io/ if help is needed during your Factory update.
