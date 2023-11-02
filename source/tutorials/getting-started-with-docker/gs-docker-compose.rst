Docker Compose YAML
^^^^^^^^^^^^^^^^^^^

``docker-compose.yml`` defines the services, networks, and volumes for multi-container Docker apps.
All the parameters you have used with ``docker run`` you can specify in ``docker-compose.yml``.
Then, with a single command, create and start all the services with your configurations.

In the following example, we will launch a single image, but keep in mind that a  ``docker-compose.yml`` can specify multiple images.

.. tip::

   For more information, see the `Compose File Version 3 Reference <https://docs.docker.com/compose/compose-file/compose-file-v3/>`_

Move the default ``docker-compose.yml`` from ``shellhttpd.disabled`` to your folder:

.. prompt:: bash host:~$, auto

    host:~$ mv ../shellhttpd.disabled/docker-compose.yml .

Review the ``docker-compose.yml`` file:

.. prompt:: bash host:~$, auto

    host:~$ cat docker-compose.yml
     
**docker-compose.yml**:

.. prompt:: text

     version: '3.2'
     
     services:
       httpd:
         image: hub.foundries.io/<factory>/shellhttpd:latest
         restart: always
         ports:
           - 8080:${PORT-8080}
         environment:
           MSG: "${MSG-Hello world}"

Most of the parameters were already used in the previous commands. 
The only thing to change is the image parameter.

In the next tutorial, you will build and deploy with FoundriesFactory®, where ``hub.foundries.io`` will be necessary.

As you are still developing locally, edit the image parameter to use the image and tag from the previous steps, ``shellhttpd:1.0``:

.. prompt:: bash host:~$, auto

    host:~$ vi docker-compose.yml

**docker-compose.yml**:

.. prompt:: text

     version: '3.2'
     
     services:
       httpd:
     #    image: hub.foundries.io/<factory>/shellhttpd:latest
         image: shellhttpd:1.0
         restart: always
         ports:
           - 8080:${PORT-8080}
         environment:
           MSG: "${MSG-Hello world}"

Notice that the MSG variable is configured to use ``Hello world`` as default.

To run your ``docker-compose`` application, execute the ``docker-compose up --detach`` command. 

.. prompt:: bash host:~$, auto

    host:~$ docker-compose up --detach

Using ``--detach`` or ``-d`` runs containers in the background.

To verify the running containers:

.. prompt:: bash host:~$, auto

    host:~$ docker ps

**Example Output**:

.. prompt:: text

     CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
     dbc969a5487d        shellhttpd:1.0       "/usr/local/bin/http…"   3 minutes ago       Up 3 minutes        0.0.0.0:8080->8080/tcp   shellhttpd_httpd_1

Test the container with ``curl``:

.. prompt:: bash host:~$, auto

    host:~$ curl 127.0.0.1:8080

**Example Output**:

.. prompt:: text

     Hello world

