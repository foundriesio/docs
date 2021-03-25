Terminology
===========

.. Glossary::
   :sorted:

   Target
     A description of the software a device should run. This description is
     visible as metadata in :term:`targets.json`. Includes details such as OSTree
     Hash and Docker-Compose App URIs, but is arbitrary.

   targets.json
     Part of `TUF Metadata <https://theupdateframework.com/metadata/>`_ that
     specifies what Targets are valid to install. It can be summarized with
     ``fioctl targets list`` or viewed in full with ``fioctl targets list
     --raw``

   Docker-Compose App
     Also referred to as 'app'. A folder in :term:`containers.git`, containing a
     `docker-compose.yml`. The name of this folder is the name of your
     **Docker-Compose App**. Appending ``.disabled`` to the name of the folder will
     prevent it from being built by the Foundries.io CI/CD. Read
     :ref:`gs-create-a-docker-compose-app` for more detail.

   MACHINE
     The Yocto machine name. Officially supported by Foundries if listed
     in :ref:`ref-linux-supported`

   system image
     The OS image produced by the Factory that is flashed to all devices. The
     build artifact is usually named ``lmp-factory-image-<hardware-id>.wic.gz``

   factory-config.yml
     A file in the :term:`ci-scripts.git` repository of the Factory which
     controls all configurable aspects of a Factory. Such as
     :ref:`ref-advanced-tagging`, :ref:`ug-configure-lmp_container-preloading`
     and email alerts.

