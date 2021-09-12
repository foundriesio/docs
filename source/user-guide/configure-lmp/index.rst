.. _ug-configure-lmp:

LmP Configuration
=================

.. _ug-configure-lmp_container-preloading:

Container Preloading
--------------------

.. note::

    Preloading container images will increase the size of the system image
    considerably, especially if the containers have not been optimally
    constructed.

    Refer to the official Docker documentation for best practices
    on writing Dockerfiles:

    https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

Container images can be preloaded onto a :term:`system image` to avoid the need
to pull these images from hub.foundries.io on the initial boot of a device. **The
device must still be registered in order to run these containers**.

Enable Preloading of Containers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable preloading, set ``containers.preload`` to ``true`` to the
:term:`factory-config.yml` of the Factory.

.. code-block:: yaml

   containers:
     preload: true

The :ref:`Factory Definition <def-containers>` contains more detailed
information on the possible options in this schema.