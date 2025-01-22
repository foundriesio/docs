.. _ug-custom-ci-for-rootfs:

Custom CI for RootFS 
====================

The FoundriesFactory™ Platform includes all you need to build a Linux®-based operating system and securely deploy it.
In particular, it provides you with a git repo and a CI service that handles building the kernel and :term:`rootfs`, and delivering them to devices.
This is done while leveraging the TUF compliant OTA service.
You can learn more in the :ref:`reference <ref-linux>` section.

In some cases, you want to build your system image and deploy it via the FoundriesFactory OTA service **without** using the CI service.
This guide walks you through the steps to accomplish this.

Prerequisites
-------------

#. A successful CI build, and a corresponding Target with the tag and hardware ID to use for the following.

Bitbake
-------

Use the :ref:`lmp-sdk container <ref-linux-building>` (aka dev container) to :term:`bitbake` a system image or an ostree repo that contains an OTA-updatable part for rootfs.

1. Disable FoundriesFactory CI specific steps.
   Add the following to ``conf/local.conf``:

   .. prompt:: text

       IMAGE_FSTYPES:remove = "ostreepush garagesign garagecheck"

2. Run the following to build a system image (if flashing of a device is needed) and the ostree repo:

   .. prompt:: text

       bitbake lmp-factory-image

3. To bitbake just the ostree repo:

   .. prompt:: text

       bitbake lmp-factory-image -c do_image_ostreecommit

You should now have an ostree repo that contains a rootfs to deliver to your devices via the OTA service. For example:

   .. code-block:: bash

       ./deploy/images/intel-corei7-64/ostree_repo

Push OSTree Repo To Cloud
-------------------------

The  Linux dev-container includes utilities called ``fiopush`` and ``fiocheck``.
These are used to push an ostree repo to the multi-tenant storage based on GCS.

.. important::
   You need an auth token to run these commands.
   The token can be obtained at `FoundriesFactory WebApp`_.
   It should have ``targets:read-update`` scope.

Run ``fiopush -factory <factory> -repo ./deploy/images/intel-corei7-64/ostree_repo -token <fio-token>`` to push the ostree repo to the FoundriesFactory storage.

Add OSTree Target
-----------------

Once the ostree repo carrying rootfs is pushed to the cloud, you can add a new Target referencing it.

The rootfs committed to the ostree repo is referenced by the commit hash.
To obtain, run ``find ./deploy/images/intel-corei7-64/ostree_repo -name *.commit``
or ``ostree --repo ./deploy/images/intel-corei7-64/ostree_repo rev-parse <machine|hardware ID>``.

Run ``fioctl targets add`` ato add the new Target referencing the given ostree-based rootfs, e.g.,

.. code-block:: bash

    fioctl targets add --type ostree --tags master,devel --src-tag master intel-corei7-64 094a6d77b7053f2fec1e5e4ccd83c38cb89174f644303c6bb09693648be98912

Check the OSTree Target
-----------------------
Use ``fioctl targets list`` and ``fioctl targets show`` to check whether the new Target is registered with the OTA service,
and whether the content is correct.

If ``aktualizr-lite`` is configured for one of the new Target's tags, then it is able to enlist and install the Target.

.. prompt:: text

    aktualizr-lite list
    ...
    info: 1589	sha256:094a6d77b7053f2fec1e5e4ccd83c38cb89174f644303c6bb09693648be98912

During the update, the log can show that aklite is downloading the expected ostree commit:

.. prompt:: text

    info: Fetching ostree commit 094a6d77b7053f2fec1e5e4ccd83c38cb89174f644303c6bb09693648be98912 from https://storage.googleapis.com/ota-lite-ostree-eu/094a6d77b7053f2fec1e5e4ccd83c38cb89174f644303c6bb09693648be98912
    ...
    aktualizr-lite status
    info: Active image is: 1589	sha256:00b2ad4a1dd7fe1e856a6d607ed492c354a423be22a44bad644092bb275e12fa

.. _FoundriesFactory WebApp:
    https://app.foundries.io/settings/tokens/
