.. _tutorial-customizing-the-platform:

Customizing the Platform
========================

Docker Compose Apps are the recommended way to create applications.
However, you are also allowed to customize and change the platform when needed.

This is useful when you need to add packages that can not run as containers, or to customize the Linux® kernel for specific hardware requirements. 
It is also done to update the Linux microPlatform (LmP).

Foundries.io™ frequently updates the Linux microPlatform for reference hardware; 
however, the updates are not automatically applied to your Factory.
You are responsible for applying updates to your platform.

When your Factory was created, four repositories were also created, including: ``lmp-manifest.git`` 
and ``meta-subscriber-overrides.git``.

``lmp-manifest.git`` contains a *manifest* of the *meta-layers* used to build your image.
This is the repository you should change to update your platform to newer 
Linux microPlatform versions. For more information, read :ref:`ref-linux-update`.

``meta-subscriber-overrides`` is the suggested meta-layer for customization.
This is a high-priority layer with the power to change anything on the platform.

This tutorial guides you through a ``meta-subscriber-overrides`` customization. 
The same ``shellhttpd`` application used in other tutorials is now being added to your platform to be executed during boot.

.. tip::

  If you are not familiar with the Yocto Project/OpenEmbedded you can still follow this tutorial. 
  The FoundriesFactory® CI helps simplify this process by building the platform in the cloud.

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
