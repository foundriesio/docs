docker-compose.yml
^^^^^^^^^^^^^^^^^^

This is a YAML file defining services, networks, and volumes for multi-container 
Docker applications. In other words, all the parameters you have used with 
``docker run`` you could specify in a ``docker-compose.yml`` file. Then, with a 
single command, create and start all the services with your configurations.

In this example, we will launch just one image, but keep in mind that 
``docker-compose.yml`` could specify more than one at the same time.

Move the default ``docker-compose.yml`` from ``shellhttpd.disabled`` to your folder:

.. prompt:: bash host:~$, auto

    host:~$ mv ../shellhttpd.disabled/docker-compose.yml .

Read the ``docker-compose.yml`` file:

.. prompt:: bash host:~$, auto

    host:~$ cat docker-compose.yml
     
**docker-compose.yml**:

.. prompt:: text

     version: '3.2'
     
     services:
       httpd:
         image: hub.foundries.io/unique-name/shellhttpd:latest
         restart: always
         ports:
           - 8080:${PORT-8080}
         environment:
           MSG: "${MSG-Hello world}"

Most of the parameters were already used in the preview commands. 
The only thing you need to change is the image parameter.

In the next tutorial, you will build and deploy the image with 
FoundriesFactory and there the image with ``hub.foundries.io`` will be necessary.

For now, because you are still developing locally, you need to 
edit the image parameter to use the image you have built in the preview steps.

Change the image parameter to the name and tag we built locally ``shellhttpd:1.0``:

.. prompt:: bash host:~$, auto

    host:~$ gedit docker-compose.yml

**docker-compose.yml**:

.. prompt:: text

     version: '3.2'
     
     services:
       httpd:
     #    image: hub.foundries.io/unique-name/shellhttpd:latest
         image: shellhttpd:1.0
         restart: always
         ports:
           - 8080:${PORT-8080}
         environment:
           MSG: "${MSG-Hello world}"

Notice that the MSG variable is now configured to use ``Hello world`` as default.

To run your docker-compose app, execute the ``docker-compose up -d`` command. 

.. prompt:: bash host:~$, auto

    host:~$ docker-compose up -d

Where: 
 - ``-d`` - Run containers in the background.

To verify the running containers:

.. prompt:: bash host:~$, auto

    host:~$ docker ps

**Example Output**:

.. prompt:: text

     CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
     dbc969a5487d        shellhttpd:1.0       "/usr/local/bin/http…"   3 minutes ago       Up 3 minutes        0.0.0.0:8080->8080/tcp   shellhttpd_httpd_1

Test the container with curl:

.. prompt:: bash host:~$, auto

    host:~$ curl 127.0.0.1:8080

**Example Output**:

.. prompt:: text

     Hello world
