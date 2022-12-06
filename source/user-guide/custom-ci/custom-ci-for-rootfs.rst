.. _ug-custom-ci-for-rootfs:

Custom CI For RootFS
====================
FoundriesFactory includes all you need to build Linux-based operating system and securely deploy it on devices.
In particular, it provides you with a git repository and the CI service that does all the necessary steps
to build Linux kernel and rootfs out of source code and deliver them to devices by leveraging the TUF compliant OTA service.
You can learn more details about it by going through this :ref:`reference <ref-linux>`.

In some cases you may need to build your system image and deploy it on devices by means of the Foundries OTA service without using the Foundries CI service.
The following guide walks you through the steps to accomplish it.

Prerequisites
-------------
1. Your Factory has been successfully created.

2. At least one successful Factory CI build and the corresponding Target with the tag and a hardware ID that you will use in the following guide.

Bitbake
-------
Use the :ref:`lmp-sdk container<ref-linux-dev-container>` (aka dev container) to bitbake a system image and/or an ostree repo that contains an OTA-updatable part for rootfs.

1. Disable the steps that are Foundries CI specific, i.e. add the following to conf/local.conf.

.. prompt:: text

    IMAGE_FSTYPES:remove = "ostreepush garagesign garagecheck"

2. Run the following to bitbake both a system image (if flashing of a device is needed) and the ostree repo.

.. prompt:: text

    bitbake lmp-factory-image

3. Run the following to bitbake just the ostree repo.

.. prompt:: text

    bitbake lmp-factory-image -c do_image_ostreecommit


As a result, you should get an ostree repo that contains a rootfs that can be delivered to your devices via the OTA service. For example:

.. prompt:: text

    ./deploy/images/intel-corei7-64/ostree_repo


Push OSTree Repo To Cloud
-------------------------
The :ref:`ref-linux-dev-container` includes utilities called fiopush and fiocheck that pushes an ostree repo to the foundries multi-tenant storage based on GCS.
You need an auth token to run these commands.
The token can be obtained at `FoundriesFactory WebApp`_, and it should have ``targets:read-update`` scope.
Run ``fiopush -factory <factory> -repo ./deploy/images/intel-corei7-64/ostree_repo -token <fio-token>`` to push the bitbaked ostree repo to the FoundriesFactory storage.


Add OSTree Target
-----------------
Once the ostree repo carrying rootfs is built and pushed to the cloud, a user can add a new Target referring to it.

The rootfs committed to the ostree repo is referred by the commit hash.
Run ``find ./deploy/images/intel-corei7-64/ostree_repo -name *.commit`` or ``ostree --repo ./deploy/images/intel-corei7-64/ostree_repo rev-parse <machine|hardware ID>``
to obtain the hash.

Then, you can run the ``fioctl targets add`` add new Target that refer to the given ostree-based rootfs, e.g.

.. prompt:: text

    fioctl targets add --type ostree --tags master,devel --src-tag master intel-corei7-64 094a6d77b7053f2fec1e5e4ccd83c38cb89174f644303c6bb09693648be98912

Check Created OSTree Target
---------------------------
Use ``fioctl targets list`` and ``fioctl targets show`` commands to check whether the new Target is registered in the Foundries OTA service
and whether their content is correct.

If ``aktualizr-lite`` is configured for one of the new Target's tags, then it should be able to enlist and install the Target.

.. prompt:: text

    aktualizr-lite list
    ...
    info: 1589	sha256:094a6d77b7053f2fec1e5e4ccd83c38cb89174f644303c6bb09693648be98912

Then during the update one can see the log saying that aklite is downloading the expected ostree commit.

.. prompt:: text

    info: Fetching ostree commit 094a6d77b7053f2fec1e5e4ccd83c38cb89174f644303c6bb09693648be98912 from https://storage.googleapis.com/ota-lite-ostree-eu/094a6d77b7053f2fec1e5e4ccd83c38cb89174f644303c6bb09693648be98912
    ...
    aktualizr-lite status
    info: Active image is: 1589	sha256:00b2ad4a1dd7fe1e856a6d607ed492c354a423be22a44bad644092bb275e12fa


.. _FoundriesFactory WebApp:
    https://app.foundries.io/settings/tokens/