.. _tutorial-creating-first-target:

Creating your first Target
==========================

In the previous tutorial ":ref:`tutorial-gs-with-docker`", you created your first 
application locally. This provided a brief overview of Docker containers and 
docker-compose apps. In this tutorial, you will learn what is a Target, how to generate 
one, and how your device consumes it.

.. note::

  Tutorial Estimated Time: 20 minutes

Learning Objectives
-------------------

- Understand what is a Target.
- Commit and send your changes to your Factory’s container repository.
- Use our dashboard at https://app.foundries.io/ to find your build and follow the build logs.
- Use fioctl to get information about Targets and Devices.

Prerequisites and Prework
-------------------------

- Completed the :ref:`tutorial-gs-with-docker` tutorial.
- Completed the :ref:`gs-install-fioctl` section.
- Completed the :ref:`gs-flash-device` section.
- Completed the :ref:`gs-register` section.

Instructions
------------

Instead of going direct to What is a **Target**, this tutorial will guide you over 
the steps that will end up creating a new Target.

Commit and Push our changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the preview tutorial :ref:`tutorial-gs-with-docker`, you have walked through 
most of the files inside the ``shellhttpd.disabled`` folder.

In this chapter, you will work on final adjustments to send your changes to 
the remote repository. This will trigger a new build in the CI, it will 
compile and publish your application on your `Factory hub <https://hub.foundries.io/>`_.

Open a new terminal in your host machine and find the container folder used in 
the preview tutorial.

.. prompt:: bash host:~$

     cd containers/

Edit the file ``shellhttpd/docker-compose.yml`` and change the image back 
to hub.foundries.io.

.. prompt:: bash host:~$, auto

    host:~$ gedit shellhttpd/docker-compose.yml

**docker-compose.yml**:

.. prompt:: text

     version: '3.2'
     
     services:
       httpd:
         image: hub.foundries.io/unique-name/shellhttpd:latest
     #    image: shellhttpd:1.0
         restart: always
         ports:
           - 8080:${PORT-8080}
         environment:
           MSG: "${MSG-Hello world}"       

In the folder ``shellhttpd.disabled`` there is still one file, the ``docker-build.conf``.

Move the ``docker-build.conf`` to your ``shellhttpd`` folder:

.. prompt:: bash host:~$, auto

    host:~$ mv shellhttpd.disabled/docker-build.conf shellhttpd/

This file will specify advanced configurations for your CI build. We don’t need 
to go further on it right now but just to let you know, one of the features of 
the CI is to execute commands after building the image to test the container.

Check the content of your ``docker-build.conf``:

.. prompt:: bash host:~$, auto

    host:~$ cat shellhttpd/docker-build.conf 

**docker-build.conf**:

.. prompt:: text

     # Allow CI loop to unit test the container by running a command inside it
     TEST_CMD="/bin/true"

``TEST_CMD`` tells CI to run the simple command ``/bin/true``. If this command 
fails for some reason, it will mark the container build as failed.

Use ``git status`` in the ``containers`` directory to verify all the changes you have done:

.. prompt:: bash host:~$, auto

    host:~$ git status

**Example Output**:

.. prompt:: text

     On branch devel
     Your branch is up to date with 'origin/devel'.
     
     Changes not staged for commit:
       (use "git add/rm <file>..." to update what will be committed)
       (use "git restore <file>..." to discard changes in working directory)
	     deleted:    shellhttpd.disabled/Dockerfile
	     deleted:    shellhttpd.disabled/docker-build.conf
	     deleted:    shellhttpd.disabled/docker-compose.yml
	     deleted:    shellhttpd.disabled/httpd.sh
     Untracked files:
       (use "git add <file>..." to include in what will be committed)
	     shellhttpd/
     no changes added to commit (use "git add" and/or "git commit -a")

Remove from git the folder ``shellhttpd.disabled``: 

.. prompt:: bash host:~$, auto

    host:~$ git rm -r shellhttpd.disabled/

**Example Output**:

.. prompt:: text

     rm 'shellhttpd.disabled/Dockerfile'
     rm 'shellhttpd.disabled/docker-build.conf'
     rm 'shellhttpd.disabled/docker-compose.yml'
     rm 'shellhttpd.disabled/httpd.sh'

Add the folder ``shellhttpd``:

.. prompt:: bash host:~$, auto

    host:~$ git add shellhttpd/
    
Check the status again before we commit:

.. prompt:: bash host:~$, auto

    host:~$ git status

**Example Output**:

.. prompt:: text

     On branch devel
     Your branch is up to date with 'origin/devel'.
     Changes to be committed:
       (use "git restore --staged <file>..." to unstage)
	     renamed:    shellhttpd.disabled/Dockerfile -> shellhttpd/Dockerfile
	     renamed:    shellhttpd.disabled/docker-build.conf -> shellhttpd/docker-build.conf
	     renamed:    shellhttpd.disabled/docker-compose.yml -> shellhttpd/docker-compose.yml
	     renamed:    shellhttpd.disabled/httpd.sh -> shellhttpd/httpd.sh

Commit your changes with the message:

.. prompt:: bash host:~$, auto

    host:~$ git commit -m "shellhttpd: add application"

Push all committed modification to the remote repository:

.. prompt:: bash host:~$, auto

    host:~$ git push

**Example Output**:

.. prompt:: text

     Enumerating objects: 6, done.
     Counting objects: 100% (6/6), done.
     Delta compression using up to 16 threads
     Compressing objects: 100% (5/5), done.
     Writing objects: 100% (5/5), 795 bytes | 795.00 KiB/s, done.
     Total 5 (delta 0), reused 0 (delta 0), pack-reused 0
     remote: Trigger CI job...
     remote: CI job started: https://ci.foundries.io/projects/unique-name/lmp/builds/4/
     To https://source.foundries.io/factories/unique-name/containers.git
        daaca9c..d7bc382  devel -> devel

.. note::

   ``git push`` output will indicate the start of a new CI job.

Find your build
^^^^^^^^^^^^^^^

Remember that in the previous tutorial, you cloned the ``devel`` branch. 
Right after the push, our CI will automatically trigger a new ``container-devel`` build.
Go to https://app.foundries.io, select your Factory and click on :guilabel:`Targets`:

The last **Target** named :guilabel:`containers-devel` should be the CI job you just created.

.. figure:: /_static/tutorials/creating-first-target/tutorial-find-build.png
   :width: 900
   :align: center

   FoundriesFactory Targets

Click on it and if you are checking it right after the ``git push``, you might 
be able to see the CI jobs on :guilabel:`queued` and/or :guilabel:`building` status.

Your FoundriesFactory is configured by default to build your container for 
``arm32``, ``arm64``, and ``x86``. If you select the :guilabel:`+` signal in a 
:guilabel:`building` architecture you will be able to see the live build log:

.. figure:: /_static/tutorials/creating-first-target/tutorial-containers.png
   :width: 900
   :align: center

   containers-devel

A live log example:

.. figure:: /_static/tutorials/creating-first-target/tutorial-logs.png
   :width: 900
   :align: center

   Containers build log

When the CI finishes the three different architecture builds, it will launch a 
final job to publish your images.

.. tip::

   At this point is where the CI job creates a **Target**

If all the builds finished without error, the **Target** was created and published correctly, 
everything will be marked as :guilabel:`passed`:

.. figure:: /_static/tutorials/creating-first-target/tutorial-finish.png
   :width: 900
   :align: center

   Containers build log

If you reload the :guilabel:`Target` page, it will indicate a new :guilabel:`Apps` available:

.. figure:: /_static/tutorials/creating-first-target/tutorial-tag.png
   :width: 900
   :align: center

   Apps available


What is a Target?
^^^^^^^^^^^^^^^^^

The CI has just created your first **Target** triggered by your changes in the ``containers.git``.

It is extremely important to understand what is a **Target**.

.. tip::

   A **Target** is a description of the software a device should run.

You just pushed changes to the branch ``devel`` of your ``containers.git`` repository. 
By default, your Factory is configured to automatically trigger a ``containers-devel`` 
CI job to build your container application changes.

After a successful build, it is created the **Target** description where:

- It’s tied together with the latest successful ``containers-devel`` and ``platform-devel``.
- It's configured by default to add the tag ``devel`` to **targets** triggered by changes in the ``devel`` branch.
- Added the Hardware ID based on what machine you have selected when created your Factory.

Last but not least, devices configured with tag and Hardware ID that matches 
with your latest **Target** will receive an update.

.. tip::

   At this point, your device should be registered to your Factory according to 
   the :ref:`Getting Started guide <gs-register>`. If your device is online, it 
   will automatically receive an update with your latest Target, but we will 
   cover more on that in the next tutorial.

.. note::

   Read the blog, `What is a Target?
   <https://foundries.io/insights/blog/2020/05/14/whats-a-target/>`_ 
   to get a high-level overview of Target. Don't worry about the instructions. 
   We will replicate them for your Factory here.

To help you understand What is a **Target**, the instructions below will guide you 
through a similar idea to the blog.

If you have an online device, ``fioctl status`` will list all devices registered 
to your Factory and what tag they are following.

It also lists what **TARGET** is installed in each device.

.. prompt:: bash host:~$, auto

    host:~$ fioctl status -f <factory_name>

**Example Output**:

.. prompt:: text

     Total number of devices: 1
     
     TAG    LATEST TARGET  DEVICES  ON LATEST  ONLINE
     ---    -------------  -------  ---------  ------
     devel  4              1        1          1
     
     ## Tag: devel
	     TARGET  DEVICES  DETAILS
	     ------  -------  -------
	     4       1        `fioctl targets show 4`

Before you inspect **Target 4**, list all your targets available with the command below:

.. prompt:: bash host:~$, auto

    host:~$ fioctl targets list -f <factory_name>

**Example Output**:

.. prompt:: text

     VERSION  TAGS    APPS        HARDWARE IDs
     -------  ----    ----        ------------
     2        devel               raspberrypi3-64
     3        master              raspberrypi3-64
     4        devel   shellhttpd  raspberrypi3-64

When your Factory is created, two platform builds are launched in the CI: ``devel`` and ``master``.

Based on my output example, they correspond to versions 2 and 3 respectively.

As you probably noticed, we suggest you start your development with the ``devel`` 
branch and installed the image from the ``platform-devel``.

When you push your ``containers.git`` changes, it resulted in version 4. 
Making it simple, version 4, created a **Target** with the latest 
container build (Version 4) + the latest platform build (Version 2).

Use the command to have a better overview of **Target 4**:

.. prompt:: bash host:~$, auto

    host:~$ fioctl targets show 4 -f <factory_name>

**Example Output**:

.. prompt:: text

     Tags:	devel
     CI:	https://ci.foundries.io/projects/cavel/lmp/builds/4/
     Source:
	     https://source.foundries.io/factories/cavel/lmp-manifest.git/commit/?id=fb119f5
	     https://source.foundries.io/factories/cavel/meta-subscriber-overrides.git/commit/?id=d89efb2
	     https://source.foundries.io/factories/cavel/containers.git/commit/?id=0bec425
     
     TARGET NAME            OSTREE HASH - SHA256
     -----------            --------------------
     raspberrypi3-64-lmp-4  3abd308ea6d4caffcdf250c7170e0dc9c8ff9082c64538bf14ca07c2df1beeff
     
     COMPOSE APP  VERSION
     -----------  -------
     shellhttpd   hub.foundries.io/cavel/shellhttpd@sha256:3ce57a22faa2484ce602c86f522b72b1b105ce85a14fc5b2a9a12eb12de4ec7f

The example above, shows a **Target** named ``raspberrypi3-64-lmp-4``, it is:

- Tagged with ``devel``.
- Specifying the OStree HASH corresponding to the latest ``platform-devel`` build.
- Listing all the container apps available, which in this case is just the ``shellhttpd``.

Conclusion
----------

This tutorial shows you what is a **Target** and all the steps to create one.
All the commands used in this Tutorial together with ":ref:`tutorial-gs-with-docker`",
will be part of a daily development flow when you are working with FoundriesFactory.

The flow to develop your application is simple:

- Try it locally.
- Send your changes to the CI.
- CI will build and create a **Target**.
- The device will receive it over-the-air.
