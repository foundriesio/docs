.. _ref-dev-mode:

Development Mode
=================================

LmP provides the variable ``DEV_MODE`` that enables a development mode defined by the Factory source code.

The variable is defined as ``lmp:params:DEV_MODE``,
and can be configured by updating the :ref:`factory-config.yml <def-lmp>` in ``ci-scripts.git`` with:

.. code-block:: yaml

  lmp:
    params:
      DEV_MODE: 1

The ``DEV_MODE`` param is set using the ``ref_options`` stanza in :ref:`factory-config.yml <def-lmp>`
for specified testing and debugging branches.
Conditional appends can then control the source code.
For example, if trying to enable systemd coredump:

.. code-block:: console

  $ cat  meta-subscriber-overrides/meta-subrecipes-core/systemd/systemd_%.bbappend
  PACKAGECONFIG += "${@bb.utils.contains('DEV_MODE', '1', 'coredump', '', d)}"

Another example is to enable the Yocto Project ``IMAGE_FEATURES`` to include some development and debug artifacts in the final image, as defined by `Yocto Project image features`_.
The following can be added to the file,
``meta-subscriber-overrides/recipes-samples/images/lmp-factory-image.bb``::

    IMAGE_FEATURES += "${@bb.utils.contains('DEV_MODE', '1', '', 'debug-tweaks tools-sdk', d)}"

.. important::

    * The default LmP configuration has ``DEV_MODE`` disabled.

    * The default FoundriesFactory configuration ** does not** define
      a development mode.

    * The development mode should be defined to archive the intended goal.

    * ``DEV_MODE`` is a helper variable used in LmP to facilitate conditionally
      enabling debug packages to the image.
      Additional packages enabled in this mode should be
      fully supported by the customer.

.. _Yocto Project image features:
   https://docs.yoctoproject.org/scarthgap/ref-manual/features.html#image-features
