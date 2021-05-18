.. _tutorial-customizing-the-platform:

Customizing the Platform
========================

Docker Compose Apps are the recommended way to create applications but you are 
also allowed to customize and change the platform according to your needs.

Customization in the platform is usually useful when you need to add 
packages to the platform, customize the Linux for specific hardware requirements, 
update the Linux microPlatform, and so on.

Foundries.io frequently updates the Linux microPlatform for the reference hardwares; 
however, the updates are not automatically applied to your Factory. You are 
responsible to apply updates to your platform.

When you create your Factory, four repositories are created, including: ``lmp-manifest.git`` 
and ``meta-subscriber-overrides.git``.

The ``lmp-manifest.git`` contains a manifest file which gather the meta-layers used to build 
your image. This is the repository you should change to update your platform to newer 
Linux microPlatform versions. For more information, read :ref:`ref-linux-update`.

The ``meta-subscriber-overrides`` is the suggested meta-layer for  
customization. That layer is a high-priority layer and it gives you the power 
to change anything on the platform.

This tutorial guides you through simple ``meta-subscriber-overrides`` customization. 
The same ``shellhttpd`` application used in previous tutorials, such as:  :ref:`tutorial-gs-with-docker`, 
:ref:`tutorial-creating-first-target` and :ref:`tutorial-deploying-first-app` is being added to your platform and is executed during boot.

.. tip::

  If you are not familiar with the Yocto Project/OpenEmbedded source code you can still follow this tutorial. 
  FoundriesFactory CI will help making it simple by building the platform in the cloud.

.. note::

  Estimated Time to Complete this Tutorial: 20 minutes

Learning Objectives
-------------------

- Introduce platform customization.
- Create ``shellhttpd`` recipe.
- Receive a platform update.
- Test the built-in application.


Prerequisites
-------------

- Completed the Getting Started from :ref:`Signed up <gs-signup>` to :ref:`gs-register`.
- Read the :ref:`ref-linux` reference manual.


Instructions
------------

.. toctree::
   :maxdepth: 1

   cloning-meta-sub-repository
   shellhttpd-recipe
   enabling-recipe
   commit-and-push-recipe
   testing-recipe
   customizing-the-platform-summary