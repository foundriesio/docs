.. _ref-factory-definition:

Factory Definition
==================

Each Factory can be customized to control how CI handles it. This is managed in
the "Factory Definition" which is located in a factory's **ci-scripts.git**
repository in the  **factory-config.yml** file.

.. _def-notify:

notify
------

.. sidebar:: ``notify:`` Section Example

    .. code-block:: yaml

         notify:
           email:
             users: foo@foo.com,bar@bar.com
           failures_only: false

notify:
 email:
  users: ``<email_1>,<email_2>,<...>``
      **Required:** Comma separated list of addresses to email after each CI build.

  failures_only: ``<true|false>``
      **Optional:** If set to ``true`` users will only be notified of CI failures.

      **Default:** ``false``

 webhooks:
     **Optional:**

     **Default:** ``Disabled``

  - url: ``https://example.com/customer-webhook-endpoint``
      **Required:** Customer owned HTTP(s) endpoint to send webhooks
    secret_name: ``my-secret-name``
        **Required:**  See :ref:`ref-ci-webhooks` for details.
    failures_only: ``<true|false>``
        **Optional:** If set to ``true`` users will only be notified of CI failures.

        **Default:** ``false``

.. _def-lmp:

lmp
---

.. sidebar:: ``lmp:`` Section Example

    .. code-block:: yaml

         lmp:
           preloaded_images:
             enabled: true
             shortlist: "app-09"
           params:
             EXAMPLE_VARIABLE_1: hello_world
           machines:
             - imx8mmevk
           image_type: lmp-factory-image
           ref_options:
            refs/heads/devel:
              machines:
                - raspberrypi3-64
              params:
                IMAGE: lmp-mini
                EXAMPLE_VARIABLE_1: foo
           tagging:
             refs/heads/master:
               - tag: postmerge
             refs/heads/devel:
               - tag: devel
           mfg_tools:
             - machine: imx8mmevk
               image_type: mfgtool-files
               params:
                 DISTRO: lmp-mfgtool
                 EXTRA_ARTIFACTS: "mfgtool-files.tar.gz"

lmp:
 preloaded_images:
  enabled: ``<true|false>``
      **Optional:** Whether to preload docker images into the system-image as
      part of a platform build.

      **Default:** ``false``

      **Inherits:** ``containers``

  shortlist: ``<app1>,<app2>,<...>``
      **Optional:** Comma separated list of apps to preload. If it is not specified 
      or its value is empty, then all Target’s apps are preloaded.

      **Default:**  None

 params:
  EXAMPLE_VARIABLE_1: ``<value>``
      **Optional:** Define an arbitrary environment variable to be passed into
      the LmP build. You can define as many as you want.

      **Default:** This variable is user defined and does not exist unless
      instantiated.

 machines:|br| ``- <machine_1>`` |br| ``- <machine_2>``
      **Required**: Specify the list of :ref:`Supported LmP Machines
      <ref-linux-supported>` to build for by their ``MACHINE`` name. A Factory's
      subscription is generally only good for a single machine.

      **Default:** Set by user during :ref:`gs-signup`

 .. note::

     The CI is configured to decline changes in the ``machines:`` parameter.
     If needed, ask a support engineer to update the machine definition for your
     FoundriesFactory.

 image_type:``<lmp_image_type>``
      **Optional:** Set the LmP image type to produce by recipe name. For
      example, ``lmp-mini-image``, ``lmp-base-console-image`` from meta-lmp_.

      **Default:** ``lmp-factory-image`` |br| (from
      **recipes-samples/images/lmp-factory-image.bb** in your
      **meta-subscriber-overrides.git** repo)

 ref_options:
  refs/heads/``<branch>``:
      **Optional:** Override options when specific git references are updated

      **Example:**

      .. code-block:: yaml

	   # In the below example, when the branch named "devel" is built by our
	   # CI system, it will have its option values for "machine" and
	   # "params" overriden by what is specified after "refs/heads/devel:".
	   # In the "devel" build, IMAGE will now equal "lmp-mini" rather than
	   # "lmp-factory-image" as initially defined.

           lmp:
             params:
               IMAGE: lmp-factory-image
             machines:
               - imx8mmevk
             ref_options:
               refs/heads/devel:
                 machines:
                   - raspberrypi3-64
                 params:
                   IMAGE: lmp-mini
 tagging:
  refs/heads/``<branch>``:|br| ``-tag: <tag>``
      **Optional:** Control how OTA_LITE tags are handled. See
      :ref:`ref-advanced-tagging` for more details.

 mfg_tools:|br| ``- machine: <machine>``
      **Optional:** Do an OE build to produce manufacturing tooling for a given
      ``MACHINE``. This is used to facilitate the manufacturing process and to ensure
      secure boot on devices. Currently only NXP tools are supported.**

      **Default:** None

  image_type: ``<mfg_image_type>``
      **Optional:** Sets the name of the recipe to use to build mfg_tools.

      **Default:** ``mfgtool-files`` |br| (from `meta-lmp-base/recipes-support/mfgtool-files/mfgtool-files_0.1.bb <https://github.com/foundriesio/meta-lmp/blob/master/meta-lmp-base/recipes-support/mfgtool-files/mfgtool-files_0.1.bb>`_)

.. _def-containers:

containers
----------

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
            refs/heads/master:
              - tag: postmerge
            refs/heads/devel-foundries:
              - tag: devel
            refs/heads/devel-foundries-base:
              - tag: devel-base
                inherit: devel

containers:
 preloaded_images:
  enabled: ``<true|false>``
      **Optional:** Whether to preload docker images into the system-image as
      part of a containers build.

      **Default:** ``false``

  shortlist: ``<app1>,<app2>,<...>``
      **Optional:** Comma separated list of apps to preload. If it is not specified 
      or its value is empty, then all Target’s apps are preloaded.

      **Default:**  None

 platforms:|br| ``- arm`` |br| ``- arm64`` |br| ``- amd64``
      **Optional:** Specify a list of architectures to build containers for.
      Containers are only built for the specified list.

      **Default:** ``amd64``

 tagging:
  refs/heads/``<branch>``:|br| ``-tag: <tag>``
      **Optional:** Control how OTA_LITE tags are handled. See
      :ref:`ref-advanced-tagging` for more details.

      **Default:** This variable does not exist unless instantiated.

.. todo:: provide a list of supported architectures for containers:
.. todo:: document DOCKER_SECRETS

.. # define a hard line break for HTML
.. |br| raw:: html

   <br />

.. _meta-lmp: https://github.com/foundriesio/meta-lmp/tree/master/meta-lmp-base/recipes-samples/images
