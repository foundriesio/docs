Cloning Meta Subscriber Overrides Repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. tip::

   When your Factory is first created, 2 branches are established for meta-subscriber-overrides: ``master`` and ``devel``.
   We suggest using the ``devel`` branch for development. Once those changes are tested and approved, migrate them to ``master``.

Clone your ``meta-subscriber-overrides.git`` repo and enter its directory:

.. prompt:: bash host:~$

    git clone -b devel https://source.foundries.io/factories/<factory>/meta-subscriber-overrides.git
    cd meta-subscriber-overrides

Your ``meta-subscriber-overrides.git`` repository is initialized with some files 
to meet the Yocto Project/OpenEmbedded meta layer standards and facilitate your first customization.

The ``meta-subscriber-overrides.git`` repository should look like this:

.. prompt::

    meta-subscriber-overrides
    ├── conf
    │   ├── layer.conf
    │   └── machine
    │       └── include
    │           └── lmp-factory-custom.inc
    ├── LICENSE
    ├── LICENSE.MIT
    └── recipes-samples
        └── images
            └── lmp-factory-image.bb

.. tip::

   This tutorial does not cover in detail the Yocto Project/OpenEmbedded file structure and 
   commands. For more information, see the `Yocto Project Documentation <https://docs.yoctoproject.org/>`_
