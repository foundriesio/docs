.. _ug-custom-ci-for-apps:

Custom CI To Build Compose App Targets
======================================

FoundriesFactory® includes all you need to build a containerized application and securely deploy it on devices.
This includes: 

* a git repository
* a CI service that handles the steps to build and delivery apps leveraging the :term:`TUF` compliant OTA service.

Learn more through this :ref:`tutorial <tutorial-compose-app>` on compose apps.

FoundriesFactory consists of well integrated but loosely coupled services.
This allows for using the OTA framework without also using the FoundriesFactory git repos or CI service.
This means you can host your source code anywhere or build your App through any framework, while still leveraging the rest of FoundriesFactory.

This section guides you through the steps of creating a custom CI pipeline in GitHub that:

- builds multi-arch container images and pushes them to the `FoundriesFactory Registry`_;
- builds a `FoundriesFactory Compose App`_ and pushes it to the `FoundriesFactory Registry`_;
- composes `TUF Targets role metadata`_ compliant with our TUF requirements;
- adds the composed TUF Targets to `FoundriesFactory Targets`_.

Prerequisites
-------------

*  A successful platform build for the corresponding tag (``custom-ci-devel`` in the example), and the hardware ID (machine) of a device for following along

*  GitHub repo with source code, Dockerfiles, and a Docker compose file.

The prerequisites will look like:

1. A Factory (``lmp-demo``) with a built Target. It has the tag ``custom-ci-devel`` and the hardware ID ``raspberrypi4-64``.

    .. code-block:: bash

        Fioctl targets show 1 -f lmp-demo
            APP  HASH
            ---  ----
        ## Target: raspberrypi4-64-lmp-1
           Created:       2022-11-30T00:20:31Z
           Tags:          custom-ci-devel
           OSTree Hash:   fe15cf8ad5e09136725ef996c93299d70fa0d20bfa2f10651437b8860b9edcdb

2. `The GitHub repo`_ that contains a working App implementation.

Creating And Setting the Access Token
-------------------------------------

First, you will need to authenticate the GitHub action for the OTA service and the `FoundriesFactory Registry`_.
Create the token to add to the GitHub action via the `FoundriesFactory WebApp`_.
The token must have ``containers:read-update``, ``targets:read-update`` and ``ci:read-update`` scopes to access the registry, FoundriesFactory CI and the OTA service.

Set Token in GitHub Repo
------------------------

Go to ``https://github.com/<your account>/<your repo>/settings/secrets/actions`` and add a secret named ``FIO_TOKEN`` with the value obtained in the previous step.

Define GitHub Actions Workflow
------------------------------

The next step is to define a GitHub actions workflow in your repo or extend an existing one.
`The sample GitHub actions workflow`_ demonstrates a workflow that communicates with FoundriesFactory to achieve the goal of this guide.
The workflow does the following:

1. Builds and pushes images to the registry.
2. Stores the built image URIs (must be digest/hashed references) for the App compose project to reference.
3. Builds and pushes the Compose App by utilizing the `compose-publish`_ utility.
4. Composes and posts the new Target(s) that reference the App built in step 3.
   It accomplishes this with the  ``fioctl targets add`` command.

Learn App Repo Structure Details
--------------------------------

You need to understand the structure of the sample App before creating your own App and CI job.

The Docker files and build directories for container images are in sub-directories of ``<root>/docker``.
The name of each sub-directory corresponds to a container image name.
The compose project definition refers to the container images defined in the repo and built by the CI job with the reference ``hub.foundries.io/lmp-demo/<app-name|dir>``.

The App compose file and any supplementary files go under ``<root>/compose/<app-dir>``.
In the compose file, reference container images in the same repo and built by the repo CI,*without* any tag or hash, e.g., ``image: hub.foundries.io/lmp-demo/ha-app``.
Reference container images **not** hosted in the given repo (``external``) *with* a tag or a hash, e.g. ``image: ghcr.io/home-assistant/home-assistant:2022.11.4``.

FoundriesFactory Utilities: Usage Details
-----------------------------------------
The `compose-publish`_ CLI utility does the following:

1. Pins images referenced from the App compose file.

    a) If an image is already pinned (digest, a reference with sha256 hash) it does nothing.
    b) If an image is referenced by a tag, it tries to get the image digest—a reference with sha256 hash.
       If it fails to obtain an image digest, the utility exists with an error.
    c) If an image reference has no tag or hash, it checks if the digest is specified via the ``--pinned-images`` parameter.
       If not found, the utility exists with an error.

2. Creates the compose App container image.

    a) Creates an archive (``tgz``) containing the App compose file and any supplementary files.
    b) Creates a container image manifest referencing the App archive as an image layer/blob.

3. Pushes the App container image to the `FoundriesFactory Registry`_.

The utility outputs the App image digest to the file specified via ``-d``.
Reference the published App with a hashed URI: ``hub.foundries.io/<factory>/<app-name>@sha256:<hash>``.

After pushing the App to the registry, you can create a new Target referencing it.
Use the Fioctl® command ``fioctl targets add`` to do so.

Check the Workflow Result
-------------------------

Use ``fioctl targets list`` and ``fioctl targets show`` to check whether the new Targets are registered in the FoundriesFactory OTA service, and whether their content is correct.

.. note::

    What if you may want to keep your App source code in a private repo, yet still use the FoundriesFactory CI service?
    In this case, check out the following two approaches:

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
