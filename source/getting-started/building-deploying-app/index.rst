.. _gs-building-deploying-app:

Building and Deploying Application
==================================

Clone and enter your ``containers.git``:

.. code-block:: console

   $ git clone https://source.foundries.io/factories/<factory>/containers.git
   $ cd containers

Your ``containers.git`` repository is initialized with a simple application example in ``shellhttpd.disabled``.

.. tip::

  Directory names ending with ``.disabled`` in ``containers.git`` are **ignored** by the FoundriesFactory™ Platform CI.

Move the entire application folder ``shellhttpd.disabled`` to ``shellhttpd``:

.. code-block:: console

    $ git mv shellhttpd.disabled/ shellhttpd

Commit your changes with a message:

.. code-block:: console

    $ git commit -m "shellhttpd: add application"

Push all committed modifications to the remote repository:

.. code-block:: console

    $ git push

     Enumerating objects: 6, done.
     Counting objects: 100% (6/6), done.
     Delta compression using up to 16 threads
     Compressing objects: 100% (5/5), done.
     Writing objects: 100% (5/5), 795 bytes | 795.00 KiB/s, done.
     Total 5 (delta 0), reused 0 (delta 0), pack-reused 0
     remote: Trigger CI job...
     remote: CI job started: https://ci.foundries.io/projects/<factory>/lmp/builds/4/
     To https://source.foundries.io/factories/<factory>/containers.git
        daaca9c..d7bc382  main -> main

.. note::

   The output of ``git push`` indicates the start of a new CI job.

Once your changes to the :term:`containers.git` repository were pushed, the FoundriesFactory® CI automatically started a new ``container-main`` build.
Go to https://app.foundries.io, select your Factory and click on :guilabel:`Targets`:

The latest :term:`Target` named :guilabel:`containers-main` should be the CI job you just created.

.. figure:: /_static/getting-started/building-deploying-app/tutorial-find-build.png
   :width: 900
   :align: center

   FoundriesFactory Targets

Your device is configured to always download the latest **Target** version with a specific ``tag``.

By default, devices run **all** applications defined in the ``containers.git`` repo.
This behavior can be changed by enabling only specific applications.
This will be covered this in more detail later.

When the container build finishes, the device will download and start the shellhttpd application.

Check the device status on the :guilabel:`devices` page.
Watch for the green light under :guilabel:`STATUS`.

.. figure:: /_static/tutorials/deploying-first-app/tutorial-device.png
   :width: 900
   :align: center

   Device List

Testing the Container
^^^^^^^^^^^^^^^^^^^^^

``curl`` is not available on your device, instead run ``wget`` to test the container like so:

.. code-block:: console

    device:~$ wget -qO- 127.0.0.1:8080

     Hello world

You can also test the container from an external device connected to the same network, such as your computer.

.. code-block:: console

    $ #Example curl 192.168.15.11:8080
    $ curl <device IP>:8080
      Hello world

You can get a more detailed guide by following the next section, **Tutorials**, starting with :ref:`tutorial-gs-with-docker`.

.. seealso::
   If you would like to learn about how to customize the platform,
   checkout both our :ref:`tutorial <tutorial-customizing-the-platform>`, and the user guide on :ref:`lmp-customization`.
