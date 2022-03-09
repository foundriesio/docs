.. _ref-containers-caching:

Caching
=======

Each container built in a FoundriesFactory will publish the build cache layers 
to our private registry, hub.foundries.io. Subsequent builds will pull from this
cache, importing it for the current build. This provides efficient incremental
container builds for our FoundriesFactory users. Exporting and importing
these build cache layers uses the built-in features of
`Docker Buildx. <https://docs.docker.com/buildx/working-with-buildx/>`_

While the cache is very helpful, there are a few things to note:

 * The build cache for each container image is branch specific
 * It is architecture specific
 * It can be invalidated for a few reasons, such as source files changing
   or a base image update.

Cache Invalidation
------------------

When trying to understand why the cache has been invalidated, there are not any
tools that can assist. That said, in a FoundriesFactory each container build 
will automatically use the docker build context to create a list of md5sums of all 
source files used in the build. Each :doc:`compose-apps` will generate an artifact 
named ``<compose-app-name>-md5sum.txt``, which then can be used to 
generate a ``diff`` from build to build to assist in understanding what files may 
have changed, and how that effects the caching. Generally, each line in your ``Dockerfile``
creates it's own image layer, and a corresponding cache layer. If source files change, 
or any direct modification to the ``Dockerfile`` occurs, it will invalidate the cache from 
that point forward. With the importance of these concepts towards building  :doc:`compose-apps`,
it is recommended to read the documentation related to `Dockerfile best practices. <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/>`_
