.. _tutorials:

Tutorials
=========

The following tutorials will help familiarize you with the workflow for your Factory.
As the concepts build upon others, follow them sequentially.

.. important::
   The tutorials assume you have followed the ``Getting Started`` section and that you have a registered device for either a :ref:`Arduino UNO Q / Container-Only Factory <gs-register-fioup>` or an :ref:`LmP Factory <gs-register>`.

   Make sure you have ``git`` and :ref:`Fioctl <gs-install-fioctl>` installed on your host machine.

:ref:`tutorial-gs-with-docker` introduces ``docker-compose`` apps.
Next is :ref:`tutorial-creating-first-target` —learning what a :term:`Target` is through experience is key to using your Factory.

Then you will learn how devices consume Targets with :ref:`tutorial-deploying-first-app`.

:ref:`tutorial-configuring-and-sharing-volumes` introduces ways to configure devices.

:ref:`tutorial-compose-app` provides more in depth experience creating Apps.

If you need to make changes on your device outside running containers,
learning about :ref:`tutorial-customizing-the-platform` is vital.

Learning about :ref:`tutorial-working-with-tags` assists with development workflow.

For further instructional reading,
the :ref:`User Guide <user-guide>` covers common tasks and settings for your Factory.

For advanced use cases and technical details, see the :ref:`Reference Manual <ref-manual>`.

.. toctree::
  
   getting-started-with-docker/getting-started-with-docker
   creating-first-target/creating-first-target
   deploying-first-app/deploying-first-app
   configuring-and-sharing-volumes/configuring-and-sharing-volumes
   compose-app/compose-app
   customizing-the-platform/customizing-the-platform
   working-with-tags/working-with-tags
