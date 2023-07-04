.. _tutorial-configuring-and-sharing-volumes:

Configuring and Sharing Volumes
===============================

In this tutorial, you will learn different techniques that will help you 
configure your device.

The includes using ``fioctl config``. 
With Fioctl® you can securely send configuration files to the device.
``fioconfig`` —a daemon running on the device—pulls secure configuration files and decrypts them during boot.

.. note::

  Estimated Time to Complete this Tutorial: 20 minutes

Learning Objectives
-------------------

- Change the shellhttpd app to consume a static configuration file.
- Share a folder allowing you to change the configuration dynamically.
- Use ``fioctl`` with ``fioconfig`` to securely send a dynamic configuration to the device.

Prerequisites
-------------

- Completed the :ref:`tutorial-gs-with-docker` tutorial.
- Completed the :ref:`tutorial-creating-first-target` tutorial.
- Completed the :ref:`tutorial-deploying-first-app` tutorial.

Instructions
------------

.. toctree::
   :maxdepth: 1

   modify-shellhttpd-container
   copy-configuration-file-using-dockerfile
   sharing-folder
   dynamic-configuration-file
   update-shellhttpd-application
   configuring-and-sharing-volumes-summary
