Dockerfile
^^^^^^^^^^

The first file we will look at is ``Dockerfile``.
Enter the ``shellhttpd`` folder and move ``Dockerfile`` from ``shellhttpd.disabled`` to ``shellhttpd``:

.. code-block:: console

    $ cd shellhttpd
    $ mv ../shellhttpd.disabled/Dockerfile .

This file contains all the commands a user would call on the command line to assemble a container image.

A ``Dockerfile`` starts from a base image.
This base could be a distro such as Alpine or Ubuntu, or it could be setup for a specific application, such as Python or Nginx.

Think of the ``Dockerfile`` as your way of customizing the base image.

.. tip::

   For more information, see the `Dockerfile Reference <https://docs.docker.com/engine/reference/builder/>`_

Check the content of your ``Dockerfile``:

.. code-block:: console

    $ cat Dockerfile

.. code-block:: dockerfile

      FROM alpine
      COPY httpd.sh /usr/local/bin/
      CMD ["/usr/local/bin/httpd.sh"]

This ``Dockerfile`` is short and simple to help get started. 

The first line creates a layer from the latest `Alpine Docker image <https://hub.docker.com/_/alpine>`_. 
The final Docker image will contain all the files provided by this base, plus your additions.

Your first customization is on the second line.
``COPY`` adds files from your Docker client’s  current directory to your Docker image.
In this case, the shell script ``httpd.sh`` is copied to ``/usr/local/bin/`` of your Docker image.

Last is ``CMD``, which *can* provide arguments for the ``ENTRYPOINT``.
However no ``ENTRYPOINT`` is specified in this example as the default entrypoint, ``/bin/sh -c``, is enough.
By passing ``/usr/local/bin/httpd.sh`` as ``CMD``, the image will execute ``/bin/sh -c  /usr/local/bin/httpd.sh`` when running the container.
