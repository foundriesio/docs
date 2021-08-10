.. _ref-containers:

Caching
=======

Each container built in a factory will publish the build cache layers 
to the private image repository used for the final container image. All
subsequent builds will pull this build cache and import it for use in 
the current build. This provides very efficient incremental container 
builds for our factory users.

While cache is very helpful, there are a few things to note:

 * The build cache for each container image is branch specific.
 * The build cache is architecture specific.
 * The build cache can be invalidated for a few reasons, such as source files changing
   or a base image update.

Cache Invalidation
------------------

When trying to understand why the cache has been invalidated, there really isn't any 
tools to assist in this process. That said, in a factory each container build 
automatically will use the docker build context to create a list of md5sums of all 
the files used in the build. These lists are published are build artifacts, which 
then can be used to ``diff`` from build to build to assist in understanding what 
files may have changed, and how that affects the caching. 

