.. _ref-factory-definition:

Factory Definition
==================

Each Factory can be customized to control how CI handles it.
This is managed in the "Factory Definition" , located in a Factory's ``ci-scripts.git`` repo, in ``factory-config.yml``.

.. _def-notify:

notify
------

Configures who receives an email with build notifications.

.. sidebar:: ``notify:`` Section Example

    .. code-block:: yaml

         notify:
           email:
             users: foo@foo.com,bar@bar.com
             failures_only: false

notify:
 email:
  users: ``<email_1>,<email_2>,<...>``
      **Required:** A Comma separated list of email addresses to email after each CI build.

  failures_only: ``<true|false>``
      **Optional:** If set to ``true``, users will only be notified of CI failures.

      **Default:** ``false``

 webhooks:
     **Optional:**

     **Default:** ``Disabled``

    url: ``https://example.com/your-webhook-endpoint``
      **Required:** A HTTP(s) endpoint you own to send webhooks
    secret_name: ``my-secret-name``
        **Required:**  See :ref:`ref-ci-webhooks` for details.
    failures_only: ``<true|false>``
        **Optional:** If set to ``true``, users will only be notified of CI failures.

        **Default:** ``false``

.. _def-tuf-expiration:

``tuf``
-------
Configures the validity period of the Factory TUF targets role metadata

.. sidebar:: ``tuf:`` Section Example

    .. code-block:: yaml

         tuf:
           targets_expire_after: "2Y33M44D"

tuf:
  targets_expire_after: ``<validity-period>``
    **Optional:** Validity period of the CI TUF targets metadata since Target creation by a CI build.
    It can be expressed in years, months, and days, with each component being optional.
    The format must follow the order of years, months, and days, as demonstrated by ``1Y3M5D``.

    **Default:** ``1Y``

.. _def-lmp:

lmp
---

Configures the LmP aspects of the Factory, including images, distro, and machine names.
Variables to be used with metadata and artifacts.

.. sidebar:: ``lmp:`` Section Example

    .. code-block:: yaml

         lmp:
           preloaded_images:
             enabled: true
             shortlist: "app-09"
           params:
             EXAMPLE_VARIABLE_1: hello_world
           machines:
             - imx8mm-lpddr4-evk
           image_type: lmp-factory-image
           ref_options:
            refs/heads/main:
              machines:
                - raspberrypi4-64
              params:
                IMAGE: lmp-factory-image
                EXAMPLE_VARIABLE_1: foo
           tagging:
             refs/heads/main:
               - tag: postmerge
             refs/heads/feature1:
               - tag: feature1
           mfg_tools:
             - machine: imx8mm-lpddr4-evk
               image_type: mfgtool-files
               params:
                 DISTRO: lmp-mfgtool
                 EXTRA_ARTIFACTS: "mfgtool-files.tar.gz"

lmp:
 preloaded_images:
  enabled: ``<true|false>``
      **Optional:** Whether to preload Docker images into the system-image as part of a platform build.

      **Default:** ``false``

      **Inherits:** ``containers``

  shortlist: ``<app1>,<app2>,<...>``
      **Optional:** Comma separated list of apps to preload.
      If not specified, or its value is empty, then all of a Target's apps are preloaded.

      **Default:**  None

 params:
  EXAMPLE_VARIABLE_1: ``<value>``
      **Optional:** Define an arbitrary environment variable to be passed into the LmP build.
      You can define as many as you want.

      **Default:** This variable is user defined and does not exist unless instantiated.

 machines:|br| ``- <machine_1>`` |br| ``- <machine_2>``
      **Required**: Specify the list of :ref:`Supported LmP Machines <ref-linux-supported>` to build for, using the ``MACHINE`` name.
      A Factory's subscription is generally only for a single machine.

      **Default**: Set during :ref:`gs-signup`.

     .. note::
        
        The CI is configured to decline changes to the ``machines:`` parameter.
        If needed, `ask a support engineer <https://support.foundries.io>`_ to update the machine definition for your Factory.

 image_type:``<lmp_image_type>``
      **Optional:** Set the LmP image type by recipe name.
      For example, ``lmp-mini-image``, ``lmp-base-console-image`` from meta-lmp_.

      **Default:** ``lmp-factory-image`` |br| 
      from ``recipes-samples/images/lmp-factory-image.bb`` in your ``meta-subscriber-overrides.git`` repo.

ref_options:
  refs/heads/``<branch>``:
      **Optional:** Override options when specific git references are updated

      **Example:**

      .. code-block:: yaml

	      # In the below example, when the branch named "feature1" is built by our
	      # CI system, it will have its option values for "machine" and
	      # "params" overriden by what is specified after "refs/heads/feature1:".
	      # In the "feature1" build, IMAGE will now equal "lmp-mini-image" rather than
	      # "lmp-factory-image" as initially defined.

               lmp:
                 params:
                  IMAGE: lmp-factory-image
                machines:
                  - imx8mn-ddr4-evk
                ref_options:
                  refs/heads/feature1:
                    machines:
                      - imx8mn-ddr4-evk
                    params:
                      IMAGE: lmp-mini-image

 tagging:
  refs/heads/``<branch>``:|br| ``-tag: <tag>``
      **Optional:** Control how OTA_LITE tags are handled. See
      :ref:`ref-advanced-tagging` for more details.

 mfg_tools:|br| ``- machine: <machine>``
      **Optional:** Do an OE build to produce manufacturing tooling for a given ``MACHINE``.
      This is used to facilitate the manufacturing process, and to ensure secure boot on devices.
      Currently, only NXP® tools are supported.

      **Default:** None

 image_type: ``<mfg_image_type>``
      **Optional:** Sets the name of the recipe to use to build mfg_tools.

      **Default:** ``mfgtool-files`` |br| (from `meta-lmp-base/recipes-support/mfgtool-files/mfgtool-files_0.1.bb <https://github.com/foundriesio/meta-lmp/blob/main/meta-lmp-base/recipes-support/mfgtool-files/mfgtool-files_0.1.bb>`_)

Variables
^^^^^^^^^

* **BUILD_SDK**:
               With this variable set to ``1``, the SDK artifact will be part of the build.
               Reference: :ref:`ref-building-sdk`.
* **DEV_MODE**:
               This is a flexible variable used to configure the source code into development mode.
               The development mode should be defined by you.
               Reference: :ref:`ref-dev-mode`.
* **DISABLE_GPLV3**:
               When set to ``1``, this variable configures the source code to avoid the LmP default packages under GPLv3.
               Reference: :ref:`ref-remove-gplv3`.
* **DISTRO**:
               Defines the distro being used.
               Reference: :ref:`ref-linux-distro`.
* **SSTATE_CACHE_MIRROR**:
               Defaults to the directory mounted on the SDK build container.
               If this directory exists, it is used as the source for the shared state cache (``sstate-cache``) mirror.
               When the directory does not exist, the ``lmp-manifest`` value is used (currently points to the public HTTP shared state cache).

.. _def-containers:

containers
----------

Defines the container's configuration, including some image configuration and target architecture.

.. sidebar:: ``containers:`` Section Example

    .. code-block:: yaml

         containers:
           preloaded_images:
             enabled: true
             shortlist: "app-09"
           platforms:
             - arm
             - arm64
             - amd64
           tagging:
            refs/heads/main:
              - tag: postmerge
            refs/heads/devel-foundries:
              - tag: devel
            refs/heads/devel-foundries-base:
              - tag: devel-base
                inherit: devel

containers:
 preloaded_images:
  enabled: ``<true|false>``
      **Optional:** Whether to preload Docker images into the system-image as part of a containers build.

      **Default:** ``false``

  shortlist: ``<app1>,<app2>,<...>``
      **Optional:** Comma separated list of apps to preload.
      If it is not specified or its value is empty, then all Target's apps are preloaded.

      **Default:**  None

 platforms:|br| ``- arm`` |br| ``- arm64`` |br| ``- amd64``
      **Optional:** Specify a list of architectures to build containers for.
      Containers are only built for the specified list.

      **Default:** ``arm,arm64,amd64``. 

 tagging:
  refs/heads/``<branch>``:|br| ``-tag: <tag>``
      **Optional:** Control how OTA_LITE tags are handled. See
      :ref:`ref-advanced-tagging` for more details.

      **Default:** This variable does not exist unless instantiated.

 docker_build_secrets:|br| ``true|false``
      **Optional:** Enable secrets to be passed to :ref:`container builds <ref-container-secrets>`.

      **Default:** false

container_registries
--------------------
 container_registries:
  type: |br| ``aws|azure|gar``
      **Optional:** Authenticate with :ref:`third-party registries <ref-private-registries>` during container builds.

      **Default:** none

ci_scripts
----------
Optionally, use a custom version of ci-scripts_ to perform CI builds.

 ci_scripts:
  url:
    **Optional:** Git URL to clone

    **Default:** https://github.com/foundriesio/ci-scripts
  git_ref:
    **Optional:** Git tag, branch, or SHA to use

    **Default:** master

Variables
^^^^^^^^^

* **DISABLE_SBOM**:
               With this variable set to ``1``, container CI builds will skip the SBOM generation step.
               Reference: :ref:`sbom`.


.. # define a hard line break for HTML
.. |br| raw:: html

   <br />

.. _meta-lmp: https://github.com/foundriesio/meta-lmp/tree/main/meta-lmp-base/recipes-samples/images
.. _ci-scripts: https://github.com/foundriesio/ci-scripts
