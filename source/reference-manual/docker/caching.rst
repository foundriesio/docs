.. _ref-containers-caching:

Caching
=======

Each container built in a Factory publishes the build cache layers to our private registry, ``hub.foundries.io``.
Subsequent builds pull/import from this cache.
This provides efficient, incremental container builds.
This exporting and importing of build cache layers uses built-in features of `Docker Buildx <https://docs.docker.com/build/>`_.

While the cache is useful, there are a few things to note:

 * The build cache for each container image is *branch specific*
 * It is *architecture specific*
 * It can be invalidated for a few reasons, such as source files changing or a base image update.

Cache Invalidation
------------------

When trying to understand why a cache has been invalidated, there is not any tools that can assist.
That said, in a Factory, each container build automatically uses the Docker build context to create a list of md5sums of all source files used.

Each :ref:`Compose App <ref-compose-apps>` generates an artifact named ``<compose-app-name>-md5sum.txt``.
This can then be used to generate a ``diff`` between builds, assisting in understanding what files may have changed, and how the cache may have been effected.

Generally, each line of your ``Dockerfile`` creates an image layer with a corresponding cache layer.
If source files change, or any direct modification to the ``Dockerfile`` occurs, it will invalidate the cache from that point forward.
Due to the importance of these concepts towards building  :ref:`ref-compose-apps`, it is recommended to read the `Dockerfile best practices. <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/>`_.
