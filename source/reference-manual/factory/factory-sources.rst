.. _ref-factory-sources:

Factory Source Code
===================

The FoundriesFactory provides you with a private git sandbox which allows you
to maintain and customize your platform.

Navigate to https://source.foundries.io/factories/<factory>/

.. figure:: /_static/factory-cgit.png
   :alt: Source code navigation
   :align: center
   :width: 5in

   CGit browser

You will find four git repositories, below is a brief description of each one.

.. Glossary::

   meta-subscriber-overrides.git
     This OE layer defines what is included into your factory image. You can add
     board specific customizations and override, add and remove packages provided
     in the default Linux microPlatform base.

   lmp-manifest.git
     The repo manifest for the platform build. It defines which layer versions
     are included in your platform image. The ``default.xml`` file is the latest
     released manifest of our Linux microPlatform, and the ``<factory>.xml``
     includes your factory changes which allows you to customize your image
     against our common base.

   containers.git
     This is where containers and docker-compose apps are defined. It allows you
     to define what containers to build, and how to orchestrate them on the
     platform.  By default it will build containers for amd64, aarch64, and
     armhf architectures.

   ci-scripts.git
     Defines your platform and container build job to our continuous integration system
     which uses the data from ``master`` branch.

     The **ci-scripts.git** repository prevents a commit changing the ``lmp:machines:`` 
     stanza as well as any changes altering the history (force push is disabled).  
     Factories are created to support specific machines.
     If you need to alter this behavior after starting a FoundriesFactory, 
     please open a `support ticket <https://foundriesio.atlassian.net/servicedesk/customer/portals>`_.

Triggering Builds
~~~~~~~~~~~~~~~~~

If you push changes to either ``lmp-manifest.git`` or ``meta-subscriber-overrides.git``,
a new platform build will be triggered, and if successful will deploy the
update to any registered devices.

Any changes pushed to ``containers.git`` will trigger a container build job, and
any containers defined will be pushed to your factory’s private Docker
registry at:

 ``https://hub.foundries.io/<factory>/<container>:latest``


.. note::

   Commit messages that include ``[skip ci]`` or ``[ci skip]`` will not
   trigger CI builds.

Configuring CI to Build New Branches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, ``meta-subscriber-overrides``, ``lmp-manifest`` and ``containers``
have ``master`` and ``devel`` branches. ``ci-scripts`` only has the ``master``
branch.

Platform Branches
^^^^^^^^^^^^^^^^^

To create new buildable platform branches, first enable the new branch in
``ci-scripts``, for example:

.. code-block::

    lmp:
      tagging:
        refs/heads/master:
          - tag: master
        refs/heads/devel:
          - tag: devel
        refs/heads/new_branch:
          - tag: new_branch

Then branch out from the wanted branches in ``meta-subscriber-overrides`` and
``lmp-manifest``. For example, using ``devel`` as a base for the new branch:

.. prompt:: bash host:~$

    cd meta-subscriber-overrides
    git checkout devel
    git checkout -b new_branch
    git commit -m "[skip ci] create new branch" --allow-empty
    git push --set-upstream origin new_branch

The ``lmp-manifest`` repo change is similar as above, but includes an additional
change to point to the correct ``meta-subscriber-overrides`` branch:

.. prompt:: bash host:~$

    cd lmp-manifest
    git checkout devel
    git checkout -b new_branch
    sed -i 's/devel/new_branch/' <factory_name>.xml
    git add <factory_name>.xml
    git commit -m "point meta-subscriber-overrides to correct branch"
    git push --set-upstream origin new_branch

After the last step, a platform build for the ``new_branch`` is triggered in the
factory.

Container Branches
^^^^^^^^^^^^^^^^^^

To create new buildable container branches, first enable the new branch in
``ci-scripts``, for example:

.. code-block::

    containers:
      tagging:
        refs/heads/master:
          - tag: master
        refs/heads/devel:
          - tag: devel
        refs/heads/new_branch:
          - tag: new_branch

Then branch out from the wanted branch in ``containers``, for example using
``devel``:

.. prompt:: bash host:~$

    cd containers
    git checkout devel
    git checkout -b new_branch
    git push --set-upstream origin new_branch

After the last step, a container build for the ``new_branch`` is triggered in
the factory.
