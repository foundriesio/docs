.. _ref-containers-caching:

Caching
=======

Each container built in a factory will publish the build cache layers 
to the private image repository used for the final container image. All
subsequent builds will pull this build cache and import it for use in 
the current build. This provides very efficient incremental container 
builds for our factory users. Exporting and importing these build cache
layers uses the built-in features of `Docker Buildx. <https://docs.docker.com/buildx/working-with-buildx/>`_

While cache is very helpful, there are a few things to note:

 * The build cache for each container image is branch specific.
 * The build cache is architecture specific.
 * The build cache can be invalidated for a few reasons, such as source files changing
   or a base image update.

Cache Invalidation
------------------

When trying to understand why the cache has been invalidated, there really aren't any 
tools to assist in this process. That said, in a factory each container build 
automatically will use the docker build context to create a list of md5sums of all 
the source files used in the build. Each :doc:`compose-apps` will generate an artifact 
named ``<compose-app-name>-md5sum.txt`` in your factory, which then can be used to 
generate a ``diff`` from build to build to assist in understanding what files may 
have changed, and how that affects the caching. Generally, each line in your ``Dockerfile``
creates it's own image layer, and also a corresponding cache layer. If source files change, 
or any direct modification to the ``Dockerfile`` occurs it will invalidate the cache from 
that point forward. It is important to understand these concepts as you build your :doc:`compose-apps` 
therefore we recommend reading the documentation related to `Dockerfile best practices. <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/>`_
