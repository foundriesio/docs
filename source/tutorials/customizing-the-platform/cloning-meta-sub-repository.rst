Cloning Meta Subscriber Overrides Repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Clone your ``meta-subscriber-overrides.git`` repo and enter its directory:

.. prompt:: bash host:~$

    git clone https://source.foundries.io/factories/<factory>/meta-subscriber-overrides.git
    cd meta-subscriber-overrides

``meta-subscriber-overrides`` is initialized with some files to meet the Yocto Project/OpenEmbedded meta layer standards and facilitate your first customization.

The directory should look like this:

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
