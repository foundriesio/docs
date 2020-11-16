Terminology
===========

.. Glossary::
   :sorted:

   containers.git
     The repository in your Factory sources where containers and docker-compose
     apps are defined, to be built by Foundries.io CI/CD. Read
     :ref:`ref-factory-sources` for more detail.
  
   Target
     A description of the software a device should run. This description is
     visible as metadata in :term:`targets.json`. Includes details such as OSTree
     Hash and Docker-Compose App URIs, but is arbitrary.
  
   targets.json
     The output of ``fioctl targets list -r``
  
   Docker-Compose App
     Also referred to as 'app'. A folder in :term:`containers.git`, containing a
     `docker-compose.yml`. The name of this folder is the name of your
     **Docker-Compose App**. Appending ``.disabled`` to the name of the folder will
     prevent it from being built by the Foundries.io CI/CD. Read
     :ref:`gs-create-a-docker-compose-app` for more detail.
  
   MACHINE
     The Yocto machine name. Only supported if listed in :ref:`ref-linux-supported`
