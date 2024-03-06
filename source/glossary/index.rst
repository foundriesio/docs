Terminology
===========

.. Glossary::
   :sorted:

   FoundriesFactory
     :term:`Foundries.io`'s Cloud native DevSecOps platform.
     Used for building, testing, deploying and maintaining Linux-based devices.
     Includes the :term:`Linux microPlatform` distro, OTA update mechanisms, and management tools, such as Fioctl.
     An instance of FoundriesFactory—customized to your needs and machine—is a :term:`Factory`.

   Foundries.io
     Provider of FoundriesFactory® DevSecOps platform and the :term:`Linux microPlatform`\™ OS.
     `Website <https://foundries.io>`_.

   Factory
     An instance of :term:`FoundriesFactory` tailored to your device and needs.
     Created to support a specific machine.
     A Factory produces :term:`Target`\s.
     
     * :ref:`Account Management, Factory <account-management>`
     * :ref:`Creating, Factory <gs-signup>`
     * :ref:`Git repositories, Factory <ref-factory-sources>`
   
   Fioctl
     Factory management tool to interact with the Foundries.io REST API.
     Source code available via the `Fioctl GitHub repo <https://github.com/foundriesio/fioctl>`_.

     * :ref:`Installing, Fioctl <gs-install-fioctl>`
     * :ref:`Example use, Fioctl <ug-fioctl>`

   Aktualizr-lite
     Default Update agent for FoundriesFactory.

     * :ref:`Reference Manual, Aktualizr-lite <ref-aktualizr-lite>`
   
   Linux microPlatform  
   LmP
     The FoundriesFactory embedded Linux distro included in your Factory.
     Included via the ``meta-lmp`` Layer.
     Source code available via the `meta-lmp GitHub repo <https://github.com/foundriesio/meta-lmp>`_.
     
     * :ref:`Reference Manual, LmP <ref-linux>`
     * :ref:`Updating, LmP <ref-linux-update>`
     * :ref:`Test plan, LmP <ref-lmp-testplan>`
     * :ref:`Customizing, LmP <tutorial-customizing-the-platform>`
     * :ref:`Porting, LmP <ref-pg>`

   Target
     A description of the software a device should run. This description is visible as metadata in :term:`targets.json`.
     Includes details such as OSTree Hash and Docker-Compose App URIs, but are arbitrary.

     * :ref:`Tutorial, Target <tutorial-creating-first-target>`

   Docker-Compose App
   Compose App
     Also referred to as app. A folder in :term:`containers.git`, containing a ``docker-compose.yml``.
     The name of this folder is the name of your Docker-Compose App.

     * :ref:`Tutorial, Compose Apps <tutorial-compose-app>`
     * :ref:`User Guide, Compose Apps <ref-compose-apps>`

   System Image
     The OS image produced by the Factory that is flashed to all devices.
     The build artifact is usually named ``lmp-factory-image-<hardware-id>.wic.gz``

   ``factory-config.yml``
     A file in the :term:`ci-scripts.git` repository of the Factory which controls all configurable aspects of a Factory.
     Such as :ref:`ref-advanced-tagging`, :ref:`ug-container-preloading` and email alerts.

     * `Factory Definition Reference Manual <ref-factory-definition>`

   ``targets.json``
     Part of `TUF Metadata <https://theupdateframework.com/metadata/>`_ that specifies what Targets are valid to install.
     It can be summarized with ``fioctl targets list``, or viewed in full with ``fioctl targets list --raw``

   ``MACHINE``
     The Yocto machine name.
     Officially supported by Foundries if listed in :ref:`ref-linux-supported`.

