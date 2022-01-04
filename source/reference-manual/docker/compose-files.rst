.. _ref-compose-files:

Multiple Compose Files
======================

Docker Compose has the ability to merge multiple `Compose files`_.
This feature can come in handy when managing a Compose file across
different ``containers.git`` branches. Each branch may have merge
conflicts around adding a test container or settings that could be
eliminated with multiple compose files.

.. _compose files:
   https://docs.docker.com/compose/extends/#multiple-compose-files

The trick to making this work is informing the factory about the order
that Compose files should be evaluated. This is managed via the
``factory-config.yml`` file in the ``ci-scripts.git`` repository.
Here's an example of enabling an overrides file for the ``devel``
branch::

 containers:
  ...
  ref_options:
    refs/heads/devel:
      params:
        COMPOSE_FILES: "docker-compose.yml devel-overrides.yml"


With this in place, Foundries.io CI will include the
``devel-overrides.yml`` if its present when building each
:ref:`Compose App <ref-compose-apps>`.


On rare occasions a user may want to use a more complex setup. In this
setup there might be a ``common-services.yml`` as a `building block`_.
In this case the factory configuration could be changed to::

 containers:
   ...
   params:
     COMPOSE_FILES: "common-services.yml docker-compose.yml"

   ref_options:
     refs/heads/devel:
       params:
         COMPOSE_FILES: "common-services.yml docker-compose.yml devel-overrides.yml"

This example all branches except ``devel`` will use the globally
defined ``COMPOSE_FILES`` parameter.

.. _building block:
   https://docs.docker.com/compose/extends/#understand-the-extends-configuration
