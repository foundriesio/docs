.. _ug-custom-ci-for-apps:

.. _ug-custom-ci-app:

Custom CI To Build Compose App Targets
======================================

FoundriesFactory® includes all you need to build a containerized application and securely deploy it on devices.
This includes: 

* a git repository
* a CI service that handles the steps to build and delivery apps leveraging the TUF compliant OTA service.

You can learn more through this :ref:`tutorial <tutorial-compose-app>`.

FoundriesFactory consists of well integrated but loosely coupled services.
This allows for using the FoundriesFactory OTA framework directly, without using either FoundriesFactory git repos or the CI service.
This means you can host your source code anywhere, and build your App through any framework, and still leverage the rest of FoundriesFactory.

This section guides you through the steps of creating a custom CI pipeline in GitHub that:

- builds multi-arch container images and pushes them to `FoundriesFactory Registry`_;
- builds a `FoundriesFactory Compose App`_ and pushes it to the `FoundriesFactory Registry`_;
- composes `TUF Targets role metadata`_ compliant with FoundriesFactory TUF requirements;
- adds the composed TUF Targets to `FoundriesFactory Targets`_.

Prerequisites
-------------

#. A successful build with a corresponding Target and tag, and the hardware ID, to use for this guide.

#. A GitHub repo with source code, Dockerfiles, and a Docker compose file.

Below is an example of how the prerequisites would look like:

1. Factory ``lmp-demo`` with a successfully built Target having the tag ``custom-ci-devel`` and the hardware ID ``raspberrypi4-64``.

    .. code-block:: bash

        Fioctl targets show 1 -f lmp-demo
            APP  HASH
            ---  ----
        ## Target: raspberrypi4-64-lmp-1
           Created:       2022-11-30T00:20:31Z
           Tags:          custom-ci-devel
           OSTree Hash:   fe15cf8ad5e09136725ef996c93299d70fa0d20bfa2f10651437b8860b9edcdb

3. `The GitHub repo`_ that contains a working App implementation.


Creating And Setting the Access Token
-------------------------------------

The GitHub action needs to be authentication for the FoundriesFactory OTA service and the `FoundriesFactory Registry`_.
You can create the token to add to the GitHub action via the `FoundriesFactory WebApp`_.
The token must have ``containers:read-update`` and ``targets:read-update`` scopes to access the registry and the OTA service, respectively.

Set Token in GitHub Repo
------------------------

Go to ``https://github.com/foundriesio/<your repo>/settings/secrets/actions`` and add a secret named ``FIO_TOKEN`` with the value of the token obtained in the previous step.

Define GitHub Actions Workflow
------------------------------

The next step is to define a GitHub actions workflow in your repo or extend an existing one.
`The sample GitHub actions workflow`_ demonstrates a workflow that communicates with FoundriesFactory to achieve the `goals <ug-custom-ci-app>` of this guide.
The workflow does the following:

1. Builds and pushes images to the registry.
2. Stores the built image URIs (must be digest/hashed references) so they can be referenced from the App compose project.
3. Builds and pushes the Compose App by utilizing the `compose-publish`_ utility.
4. Composes and posts new Target(s) that references the App built in step 3.
   The ``fioctl targets add`` command is utilized to accomplish it.

Learn App Repo Structure Details
--------------------------------
It is important to understand the structure of the sample App before creating your own App and CI job that communicates with the FoundriesFactory services.

Docker files and build directories for the container images are located in sub-directories of ``<root>/docker``.
The name of each sub-directory corresponds to a container image name.
The compose project definition refers to the container images defined in the repo, and built by the CI job with the reference ``hub.foundries.io/lmp-demo/<app-name|dir>``.

The App compose file and any supplementary files are placed under the ``<root>/compose/<app-dir>`` directory.
The container images in the same repo as the App, built by the repo CI job, should be referenced in the compose file *without* any tag or hash, e.g., ``image: hub.foundries.io/lmp-demo/ha-app``.
Container images that are not hosted in the given repo (``external``), and not built by the CI job, must be referenced *with* a tag or a hash, e.g. ``image: ghcr.io/home-assistant/home-assistant:2022.11.4``.

FoundriesFactory Utilities: Usage Details
-----------------------------------------
The `compose-publish`_ CLI utility does the following:

1. Pins images referenced from the App compose file.

    a) If an image is already pinned (digest, a reference with sha256 hash) it does nothing.
    b) If an image is referred by a tag it tries to get the image digest—a reference with sha256 hash.
       If it fails to obtain an image digest, the utility exists with an error.
    c) If an image reference has no tag or hash, it checks if the digest is specified via the ``--pinned-images`` parameter.
       If not found, the utility exists with an error.

2. Creates the compose App container image.

    a) Creates an archive (``tgz``) containing the App compose file and any supplementary files.
    b) Creates a container image manifest referencing the App archive as an image layer/blob.

3. Pushes the App container image to the `FoundriesFactory Registry`_.

The utility outputs the built and pushed App image digest to the file specified via ``-d``.
The published App can now be referenced with a hashed URI — ``hub.foundries.io/<factory>/<app-name>@sha256:<hash>``.

Once the App is successfully built and pushed to the registry, a new Target referring to it can be created.
Use the Fioctl® command ``fioctl targets add`` to do so.

Check the Workflow Result
-------------------------

Use ``fioctl targets list`` and ``fioctl targets show`` to check whether the new Targets are registered in the FoundriesFactory OTA service, and whether their content is correct.

.. note::

    In some cases a user may want to keep their App source code in their private repo yet still use the FoundriesFactory CI service.
    If it is the case, then you can check out the following two approaches:

    1. :ref:`Git Mirroring <ug-mirror-action>`
    2. :ref:`Git Submodules <ug-submodule>`

.. seealso::
    :ref:`ug-custom-ci-for-rootfs`

.. _FoundriesFactory Registry:
    https://hub.foundries.io

.. _FoundriesFactory Compose App:
    https://docs.foundries.io/latest/tutorials/compose-app/compose-app.html

.. _TUF Targets role metadata:
   https://theupdateframework.io/metadata/#targets-metadata-targetsjson

.. _FoundriesFactory Targets:
    https://docs.foundries.io/latest/tutorials/creating-first-target/what-is-a-target.html

.. _The GitHub repo:
    https://github.com/foundriesio/custom-ci-app

.. _FoundriesFactory WebApp:
    https://app.foundries.io/settings/tokens/

.. _The sample GitHub actions workflow:
    https://github.com/foundriesio/custom-ci-app/blob/custom-ci-devel/.github/workflows/fio-app-ci.yml

.. _compose-publish:
    https://github.com/foundriesio/compose-publish
