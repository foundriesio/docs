Updating the Linux microPlatform Core
=====================================

Your factory platform manifest has been separated to make consuming core
platform updates easier. At Foundries.io we `release`_ Linux microPlatform
updates early and often in an effort to get the latest security fixes out to
users.

.. _release:
   https://github.com/foundriesio/lmp-manifest/releases

If you would like to try out the latest, here is how to update your factory
manifest::

  #!/bin/sh
  cd lmp-manifest
  git fetch --tags https://github.com/foundriesio/lmp-manifest
  latest=$(git rev-parse FETCH_HEAD)
  git merge-base --is-ancestor $latest HEAD && (echo "No changes found upstream"; exit 0)

  echo "Upstream changes have been found. Merging local code with upstream SHA: $latest"
  git merge $latest
  git push && git push --tags

A new platform build will be triggered, and once published the update can be
deployed.

If something goes wrong, don’t fret! This is why we use version control!::

  git revert HEAD
  git push
