.. _ug-custom-ci-for-apps:

.. _ug-custom-ci-app:

Custom CI To Build Compose App Targets
======================================

FoundriesFactory includes all you need to build a containerized application and securely deploy it on devices.
In particular, it provides you with a git repository and the CI service that does all the necessary steps
to build Apps out of source code and deliver them to devices by leveraging the TUF compliant OTA service.
You can learn more details about it by going through this :ref:`tutorial <tutorial-compose-app>`.

The FoundriesFactory solution consists of a few loosely coupled services.
It allows using the FoundriesFactory OTA framework directly, eliminating the need to host
your App source code in the FoundriesFactory git repository and using the FoundriesFactory CI service.
Therefore, you can host your App in any source code repository and build App by any other framework,
yet still leverage the rest part of FoundriesFactory.

This section guides you through the steps of creating a custom CI pipeline in GitHub that:

- builds multi-arch container images and pushes them to `Foundries Registry`_;
- builds `Foundries Compose App`_ and pushes it `Foundries Registry`_;
- composes `TUF Targets role metadata`_ compliant with FoundriesFactory TUF requirements;
- adds the composed TUF Targets to `FoundriesFactory Targets`_.

Prerequisites
-------------

1. Your Factory has been successfully created.

2. At least one successful Factory CI build and the corresponding Target with the tag and a hardware ID that you will use in the following guide.

3. You have a GitHub repo with source code, Dockerfiles, and a Docker compose file that work.

For example, the prerequisites for the following guide are:

1. Factory ``lmp-demo`` is setup and has been successfully created.
2. The successfully built Target with the tag ``custom-ci-devel`` and the hardware ID ``raspberrypi4-64``.

    .. prompt:: text

        Fioctl targets show 1 -f lmp-demo
            APP  HASH
            ---  ----
        ## Target: raspberrypi4-64-lmp-1
	        Created:       2022-11-30T00:20:31Z
            Tags:          custom-ci-devel
            OSTree Hash:   fe15cf8ad5e09136725ef996c93299d70fa0d20bfa2f10651437b8860b9edcdb

3. `The GitHub repo`_ that contains working App implementation.



Create And Set Access Token
---------------------------

The GitHub action needs to authenticate itself at the FoundriesFactory OTA service and the `Foundries Registry`_.
Therefore, an access token must be created and added to the GitHub repo action tokens prior to running any CI pipelines.
You can create the token at `FoundriesFactory WebApp`_.
The token must have ``containers:read-update`` and ``targets:read-update`` scopes to access the registry and the OTA service correspondingly.

Set Token in GitHub Repo
------------------------
Go to the ``https://github.com/foundriesio/<your repo>/settings/secrets/actions`` and add a secret named `FIO_TOKEN`
and value of the token obtained in the previous step.

Define GitHub Actions Workflow
------------------------------
The next step is to define a GitHub actions workflow in your repo or extend an existing one.
`The sample GitHub actions workflow`_ provides an example of the workflow that communicates with FoundiresFactory to achieve the goal,
i.e. the items listed at the end of :ref:`the introductory section<ug-custom-ci-app>`.
The workflow does the following:

1. Builds and pushes images to the registry.
2. Stores the built image URIs (must be digest/hashed reference) so they can be referred from the App compose project.
3. Builds and pushes Compose App by utilizing Foundries utility `compose-publish`_.
4. Composes and posts new Target(s) that refers to the App built in the step 3. The ``fioctl targets add`` command is utilized to accomplish it.

Learn App Repo Structure Details
--------------------------------
It's important to understand the structure of the sample App before creating your own App and CI job that communicates with the FoundriesFactory services.

Docker files and build directories of the container images are located in sub-directories of ``<root>/docker`` directory.
The name of each sub-directory corresponds to a container image name.
The compose project definition refers to the container images defined in the repository and built by the given CI job
by the following reference ``hub.foundries.io/lmp-demo/<app-name|dir>``.

The App compose file and supplementary files (if any) are placed under ``<root>/compose/<app-dir>`` directory.
The container images hosted in the same repo as the given App and built by the repo CI job should be referred
in the compose file without any tag or hash, e.g. ``image: hub.foundries.io/lmp-demo/ha-app``.
Container images that are not hosted in the given repo (further `external`) and are not built by the given CI job must be referred with a tag or a hash, e.g. ``image: ghcr.io/home-assistant/home-assistant:2022.11.4``

Foundries Utilities Usage Details
---------------------------------
The `compose-publish`_ CLI utility does the following:

1. Pins images referred from the App compose file.

    a) If an image is already pinned (digest, a reference with sha256 hash) it does nothing.
    b) If an image is referred by a tag it tries to get the image digest - a reference with sha256 hash. If it fails to obtain an image digest then the utility exists with an error.
    c) If an image reference has not tag nor hash it checks if it's specified via ``--pinned-images`` input parameter. If no digest reference is found in ``pinned-images`` the utility exists with an error.

2. Creates the compose App container image.

    a) Creates an archive (``tgz``) that contains the App compose file and its supplementary files.
    b) Creates a container image manifest referring to the App archive as an image layer/blob.

3. Pushes the App container image to the `Foundries Registry`_.

The utility outputs the built and pushed App image digest to the file specified via ``-d`` input parameter.
Then the published App can be referenced with a hashed URI - ``hub.foundries.io/<factory>/<app-name>@sha256:<hash>``.

Once the App is successfully built and pushed to the registry, a new Target referring to it can be created.
To do so the Fioctl command ``fioctl targets add`` should be used.

Check The Workflow Result
-------------------------

Use ``fioctl targets list`` and ``fioctl targets show`` commands to check whether the new Targets are registered in the Foundries OTA service
and whether their content is correct.

.. note::

    In some cases a user may want to keep their App source code in their private repo yet still use the Foundries CI service.
    If it is the case, then you can check out the following two approaches:

    1. :ref:`Git Mirroring <ug-mirror-action>`
    2. :ref:`Git Submodules <ug-submodule>`

.. _Foundries Registry:
    https://hub.foundries.io

.. _Foundries Compose App:
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