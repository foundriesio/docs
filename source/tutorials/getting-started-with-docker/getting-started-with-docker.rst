.. _tutorial-gs-with-docker:

Getting Started with Docker
===========================

FoundriesFactory gives you the ability to over-the-air update ``docker-compose`` 
applications.  This tutorial contains step-by-step instructions on how to get 
started with Docker and ``docker-compose`` applications, including the basic 
commands and concepts to help you to create your own application.

.. note::

  Estimated Time to Complete this Tutorial: 20 minutes

.. _tutorial-gs-with-docker-prerequisite:

Learning Objectives
-------------------

- Download your containers.git repository.
- Build your container on your host machine.
- Run your container on your host machine.
- Inspect running containers.
- Structure your applications inside the repository.
- Run your container using ``docker-compose``.

Prerequisites
-------------

- Installed `Docker`_ on your host machine.
- :ref:`Signed up <gs-signup>` and created your FoundriesFactory.
- :ref:`Configured Git. <gs-git-config>`

.. tip::

   It's not a problem if you just created your FoundriesFactory and your first build is 
   still running.  This tutorial **doesn’t require a device**. By the end, your build should 
   be finished and you can follow the instructions to flash and register your device before
   moving to next tutorials.


Instructions
------------

.. toctree::
   :maxdepth: 1

   cloning-container-repository
   gs-dockerfile
   gs-httpd
   building-your-container
   extra-commands
   gs-docker-compose
   gs-summary

.. _Docker: https://docs.docker.com/get-docker/