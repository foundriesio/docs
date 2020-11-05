.. _ref-factory-definition:

Factory Definition
==================

Each Factory can be customized to control how CI handles it. This is managed in
the “Factory Definition” which is located in a factory’s **ci-scripts.git**
repository in the  **factory-config.yml** file.

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

.. sidebar:: ``lmp:`` Section Example

    .. code-block:: yaml

         lmp:
           params:
             IMAGE: lmp-factory-image
             EXAMPLE_VARIABLE_1: hello_world
           machines:
             - imx8mmevk
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
               params:
                 DISTRO: lmp-base
                 IMAGE: mfgtool-signed-files
                 EXTRA_ARTIFACTS: "mfgtools-signed.tar.gz"

lmp:
 params:
  IMAGE: ``<lmp_image_type>``
      **Required:** Define the LmP image type you want to produce.

  EXAMPLE_VARIABLE_1: ``<value>``
      **Optional:** Define an arbitrary environment variable to be passed into
      the LmP build. You can define as many as you want.

 machines:|br| ``- <machine_1>`` |br| ``- <machine_2>``
      **Required**: Specify the list of :ref:`Supported LmP Machines
      <ref-linux-supported>` to build for by their ``MACHINE`` name. A Factory's
      subscription is generally only good for a single machine.

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
      secure boot on imx devices.

.. sidebar:: ``containers:`` Section Example

    .. code-block:: yaml

         containers:
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
 platforms:|br| ``- arm`` |br| ``- arm64`` |br| ``- amd64``
      **Optional:** Specify a list of architectures to build containers for.
      Containers are only built for the specified list.

      **Default:** ``amd64``
 tagging:
  refs/heads/``<branch>``:|br| ``-tag: <tag>``
      **Optional:** Control how OTA_LITE tags are handled. See
      :ref:`ref-advanced-tagging` for more details.

.. todo:: Define the available params for mfg_tools
.. todo:: provide a list of supported architectures for containers:
.. todo:: document DOCKER_SECRETS 
.. todo:: document container preloading

.. # define a hard line break for HTML
.. |br| raw:: html

   <br />
