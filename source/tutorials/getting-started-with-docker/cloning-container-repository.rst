Cloning Container Repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. tip::

   When your Factory is first created, a single branch (``main``) is created.
   We suggest using a ``devel`` branch for development.
   Once changes are tested and approved, migrate them to ``main``.

Clone and enter your ``containers.git``:

.. prompt:: bash host:~$

    git clone -b devel https://source.foundries.io/factories/<factory>/containers.git
    cd containers

Your ``containers.git`` repository is initialized with a simple application example in ``shellhttpd.disabled``.

.. tip::

  Directory names ending with ``.disabled`` in ``containers.git`` are **ignored** by the FoundriesFactory™ Platform CI.

For better understanding, it is best to go through the files in  ``shellhttpd.disabled`` gradually.
Create a new folder with the name ``shellhttpd``:

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
