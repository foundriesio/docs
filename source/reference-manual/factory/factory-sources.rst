.. _ref-factory-sources:

Factory Source Code
===================

FoundriesFactory® provides you with a private git sandbox, allowing you to maintain and customize your platform.
Navigate to ``https://source.foundries.io/factories/<factory>/``:

.. figure:: /_static/factory-cgit.png
   :alt: Source code navigation
   :align: center
   :width: 5in

   CGit browser

You will find four git repositories:

.. Glossary::

   ``meta-subscriber-overrides.git``
     This OE layer defines what is included in your Factory image.
     You can add board specific customizations and overrides, add and remove the packages provided in the default Linux microPlatform (LmP) base.

   ``lmp-manifest.git``
     The repo manifest for the platform build.
     This defines which layer versions are included in your platform image.
     The ``default.xml`` file is the latest released manifest of the LmP.
     ``<factory>.xml`` includes your Factory changes, allowing you to customize your image against our common base.

   ``containers.git``
     This is where containers and Docker-compose apps are defined.
     It allows you to define what containers to build, and how to orchestrate them on the platform.

   ``ci-scripts.git``
     Defines your platform and container build job to our continuous integration system which uses the data from ``master`` branch.
     Note that you are prevented from making a commit changing the ``lmp:machines:`` stanza , as well as any changes altering the history (force push is disabled).  
     Factories are created to support specific machines.
     If you need to alter this behavior after starting a Factory, please open a `support ticket <https://foundriesio.atlassian.net/servicedesk/customer/portals>`_.

Triggering Builds
~~~~~~~~~~~~~~~~~

If you push changes to either ``lmp-manifest.git`` or ``meta-subscriber-overrides.git``, a new platform build will be triggered.
If successful, the update will deploy to your registered devices.

Changes pushed to ``containers.git`` will trigger a container build job.
Defined containers will be pushed to your Factory’s private Docker registry at:

 ``https://hub.foundries.io/<factory>/<container>:latest``

.. note::

   Commit messages that include ``[skip ci]`` or ``[ci skip]`` will not trigger CI builds.

Configuring the CI to Build New Branches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, ``meta-subscriber-overrides``, ``lmp-manifest`` and ``containers`` have the single branch, ``main``.
For these repos, it is recommended to also have a ``devel`` branch for non-production purposes.
``ci-scripts`` has the single default branch ``master``.

Platform Branches
^^^^^^^^^^^^^^^^^

To create new buildable platform branches, first enable the new branch in ``ci-scripts``.
For example, if you wanted to add a development branch named ``feature1``:

.. code-block:: YAML

    lmp:
      tagging:
        refs/heads/main:
          - tag: main
        refs/heads/feature1:
          - tag: feature1

Then branch out from the wanted branches in ``meta-subscriber-overrides`` and ``lmp-manifest``.
For example, using ``main`` as a base for the new branch:

.. prompt:: bash host:~$

    cd meta-subscriber-overrides
    git checkout main
    git checkout -b feature1
    git commit -m "[skip ci] create devel branch" --allow-empty
    git push --set-upstream origin feature1

The ``lmp-manifest`` repo change is similar as above, but includes an additional change to point to the correct ``meta-subscriber-overrides`` branch:

.. prompt:: bash host:~$

    cd lmp-manifest
    git checkout main
    git checkout -b feature1
    sed -i 's/main/feature1/' <factory_name>.xml
    git add <factory_name>.xml
    git commit -m "point meta-subscriber-overrides to correct branch"
    git push --set-upstream origin feature1

After the last step, a platform build for the ``feature1`` branch is triggered for your Factory.

Container Branches
^^^^^^^^^^^^^^^^^^

To create new buildable container branches, first enable the new branch in ``ci-scripts``, for example:

.. code-block::

    containers:
      tagging:
        refs/heads/main:
          - tag: main
        refs/heads/feature1:
          - tag: feature1

Then branch out from the wanted branch in ``containers``, for example using ``main``:

.. prompt:: bash host:~$

    cd containers
    git checkout main
    git checkout -b feature1
    git push --set-upstream origin feature1

After the last step, a container build for the ``feature1`` is triggered for your Factory.
