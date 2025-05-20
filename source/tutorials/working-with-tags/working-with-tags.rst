.. _tutorial-working-with-tags:

Working With Tags
=================

Your Factory initially has a single branch, ``main``.
By convention, Targets are tagged with the branches they are built from.
This means the Targets have the tag ``main``.

.. warning::
   For this tutorial, it is assumed you have created and worked on a ``devel`` branch.
   This has not yet been covered.
   See the :ref:`ref-factory-sources` reference manual on how to configure the CI with new branches.

This helps keep the development flow fast.
For example: you start with  ``platform-devel``, a ``platform`` build based on ``devel`` branch to install on a device.

Next you develop an application on ``containers.git`` from the ``devel`` branch.
The application is built by the CI with a ``containers-devel`` trigger name, producing a Target tagged with ``devel``.

Finally, the device automatically updates to the latest Target tagged with ``devel``.

There are some use cases where you want to control what tag a device follows, and Targets are tagged:

- Preventing a device from following a tag such as ``devel``, which is automatically created every time you change the ``devel`` branch.
- Testing a specific Target on a specific device.

This tutorial will guide you through examples to help you understand how tags work.

.. note::

  Estimated Time to Complete this Tutorial: 20 minutes

Learning Objectives
-------------------

- Create more ``devel`` Targets.
- Use ``fioctl`` to Tag a specific Target.
- Configure the device to follow a specific tag.

Prerequisites
-------------

- Completed the Getting Started from :ref:`Signed up <gs-signup>` to :ref:`gs-register`.
- Completed the :ref:`tutorial-creating-first-target` tutorial.

Instructions
------------

.. toctree::
   :maxdepth: 1

   inspecting-targets
   adapting-shellhttpd
   following-specific-tag
   creating-targets
   tagging-specific-version
   working-with-tags-summary
