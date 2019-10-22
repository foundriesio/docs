Updating the Linux microPlatform Core
=====================================

Your factory platform manifest has been separated to make consuming core
platform updates easier. At Foundries.io we `release`_ Linux microPlatform
updates early and often in an effort to get the latest security fixes out to
users.

.. _release:
   https://github.com/foundriesio/lmp-manifest/releases

If you would like to try out the latest, we provide a helper script in your ``lmp-manifest`` project called ``update-factory-manifest``.

This script will automatically attempt to update your manifest to the latest version of the Linux microPlatform. If there are merge conflicts, it will be up to you to fix and commit them.

To run the script, run the following command from within your ``lmp-manifest`` project::

  git clone https://source.foundries.io/partners/<myfactory>/lmp-manifest.git
  cd lmp-manifest/scripts/
  ./update-factory-manifest

When the new manifest files have been successfully pushed, a new platform build will be triggered, and once published the update can be deployed.

If something goes wrong, don’t fret! This is why we use version control!::

  git revert HEAD
  git push
