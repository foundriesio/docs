Cloning Container Repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Clone and enter your ``containers.git``:

.. code-block:: console

    $ git clone https://source.foundries.io/factories/<factory>/containers.git
    $ cd containers

Your ``containers.git`` repository is initialized with a simple application example in ``shellhttpd.disabled``.

.. tip::

  Directory names ending with ``.disabled`` in ``containers.git`` are **ignored** by the FoundriesFactory™ Platform CI.

For better understanding, it is best to go through the files in  ``shellhttpd.disabled`` gradually.
Create a new folder with the name ``shellhttpd``:

.. code-block:: console

    $ mkdir shellhttpd

Your ``containers.git`` repository should look like this:

.. code-block:: none

    containers/
    ├── README.md
    ├── shellhttpd
    └── shellhttpd.disabled
        ├── docker-build.conf
        ├── docker-compose.yml
        ├── Dockerfile
        └── httpd.sh
