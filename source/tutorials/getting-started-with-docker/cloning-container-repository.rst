Cloning Container Repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. tip::

   When your Factory is first created, 2 branches are established: ``master`` and ``devel``.
   We suggest using the ``devel`` branch for development.

Clone your ``containers.git`` repo and enter its directory:

.. prompt:: bash host:~$

    git clone -b devel https://source.foundries.io/factories/<factory>/containers.git
    cd containers

Your ``containers.git`` repository is initialized with a simple compose app example in 
``shellhttpd.disabled``

.. tip::

  Directory names ending with ``.disabled`` in ``containers.git`` are **ignored** by 
  our CI system.


For a better understanding, it is better to consume the files from 
``shellhttpd.disabled`` gradually. Create a new folder with the name ``shellhttpd``:

.. prompt:: bash host:~$

    mkdir shellhttpd

Your ``containers.git`` repository should look like this:

.. prompt::

    containers/
    ├── README.md
    ├── shellhttpd
    └── shellhttpd.disabled
        ├── docker-build.conf
        ├── docker-compose.yml
        ├── Dockerfile
        └── httpd.sh
