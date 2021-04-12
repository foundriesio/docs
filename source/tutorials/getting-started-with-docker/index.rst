.. _tutorial-gs-with-docker:

Getting Started with Docker
===========================

FoundriesFactory gives you the ability to over-the-air update docker-compose 
applications, so this page contains step-by-step instructions on how to get 
started with Docker and docker-compose applications. This tutorial will give you 
the basic commands and concepts to help you to create your application.

.. note::

  Estimated Time: 3 minutes

.. _tutorial-gs-with-docker-prerequisite:

Learning Objectives
-------------------

- Download your containers.git repository.
- Build your container on your host machine.
- Run your container on your host machine.
- Inspect running containers.
- Structure your apps inside the repository.
- Run your container using docker-compose.

Prerequisites and Prework
-------------------------

- Installed `Docker`_ on your host machine.
- :ref:`Signed up <gs-signup>` and created your FoundriesFactory.
- :ref:`Configured Git. <gs-git-config>`

.. tip::

   In case you just created your FoundriesFactory and your first build is still 
   running, it is not a problem, this tutorial doesn’t require a device. By the 
   end of this tutorial, your build is probably already finished and you can 
   follow the instructions to flash your device and move to the next tutorials.


Instructions
------------

.. tip::

   When your Factory is first created, 2 branches are established: ``master`` and ``devel``.
   We suggest using the ``devel`` branch for development

Clone your ``containers.git`` repo and enter it:

.. prompt:: bash host:~$

    git clone -b devel https://source.foundries.io/factories/<factory>/containers.git
    cd containers.git

Your ``containers.git`` repository is initialized with a simple compose app example in 
``shellhttpd.disabled``

.. tip::

  Directory names ending with ``.disabled`` in ``containers.git`` are **ignored** by 
  our CI system.


For a better understanding, it is better to consume the files from 
``shellhttpd.disabled`` gradually. Create a new folder with the name ``shellhttpd``:

.. prompt:: bash host:~$

    mkdir shellhttpd

Your container repository should look like this:

.. prompt::

    containers/
    ├── README.md
    ├── shellhttpd
    └── shellhttpd.disabled
        ├── docker-build.conf
        ├── docker-compose.yml
        ├── Dockerfile
        └── httpd.sh

Dockerfile
^^^^^^^^^^

The first file you will use is the Dockerfile. Enter the ``shellhttpd`` folder and move the 
Dockerfile from ``shellhttpd.disabled`` to ``shellhttpd``:

.. prompt:: bash host:~$

    cd shellhttpd
    mv ../shellhttpd.disabled/Dockerfile .

The Dockerfile contains all the commands a user would call on the command line to assemble 
a container image.

A Dockerfile usually starts from a base image. The base image could be a distribution like 
Alpine, Debian, or Ubuntu or it could be a distribution already prepared for a specific 
application like Python, NGINX.

By having your Dockerfile you will be able to customize the base image.

Check the content of your Dockerfile:

.. prompt:: bash host:~$, auto

    host:~$ cat Dockerfile

**Dockerfile**:

.. prompt:: text

      Dockerfile
      FROM alpine
      COPY httpd.sh /usr/local/bin/
      CMD ["/usr/local/bin/httpd.sh"]

This Dockerfile is very simple and a great way to get started. 

The first line creates a layer from the latest 
`Alpine Docker image <https://hub.docker.com/_/alpine>`_. 
This means that your final image contains all the files 
provided by this image plus your additions.

Your first customization is in the second line. ``COPY`` adds files from your Docker client’s 
current directory to your Docker image. In this case, you will copy the shell script 
``httpd.sh`` to the ``/usr/local/bin/`` directory of your Docker image.

Last but not least there is ``CMD``, these are arguments for the ``ENTRYPOINT``. In this example, 
there is no ``ENTRYPOINT`` specified because the default entrypoint is enough.

The default entrypoint is ``/bin/sh -c`` and by passing ``/usr/local/bin/httpd.sh`` as ``CMD`` you 
are configuring the image to execute the command line: ``/bin/sh -c  /usr/local/bin/httpd.sh`` 
when you run the container.

httpd.sh
^^^^^^^^

As mentioned above, Dockerfile will copy the ``httpd.sh`` file to your Docker image. 
Move the file from ``shellhttpd.disabled`` to the ``shellhttpd`` folder:

.. prompt:: bash host:~$

    mv ../shellhttpd.disabled/httpd.sh .

Check the content of your ``httpd.sh``:

.. prompt:: bash host:~$, auto

    host:~$ cat httpd.sh

**httpd.sh**:

.. prompt:: text

     #!/bin/sh -e
     
     PORT="${PORT-8080}"
     MSG="${MSG-OK}"
     
     RESPONSE="HTTP/1.1 200 OK\r\n\r\n${MSG}\r\n"
     
     while true; do
      echo -en "$RESPONSE" | nc -l -p "${PORT}" || true
      echo "= $(date) ============================="
     done

This is a shell script file that will respond to a request on the port defined by the 
PORT environment variable (defaults to ``8080``) with the message defined by the MSG 
environment variable (defaults to ``OK``).

Building your Container
^^^^^^^^^^^^^^^^^^^^^^^

Now that you have a Dockerfile, you can build it locally to make sure it is working properly.

From the same folder containing the Dockerfile, run the command below:

.. prompt:: bash host:~$, auto

    host:~$ docker build --tag shellhttpd:1.0 .

**Example Output**:

.. prompt:: text

     Sending build context to Docker daemon  3.072kB
     Step 1/3 : FROM alpine
     latest: Pulling from library/alpine
     ba3557a56b15: Pull complete 
     Digest: sha256:a75afd8b57e7f34e4dad8d65e2c7ba2e1975c795ce1ee22fa34f8cf46f96a3be
     Status: Downloaded newer image for alpine:latest
      ---> 28f6e2705743
     Step 2/3 : COPY httpd.sh /usr/local/bin/
      ---> 450c272c3201
     Step 3/3 : CMD ["/usr/local/bin/httpd.sh"]
      ---> Running in 92f5efa26f6e
     Removing intermediate container 92f5efa26f6e
      ---> a5984eb19baf
     Successfully built a5984eb19baf
     Successfully tagged shellhttpd:1.0

Now let’s run your first container locally:

.. prompt:: bash host:~$

    docker run -d -p 8080:8080 --name shellhttpd shellhttpd:1.0


- ``-d`` - run the container in detached mode (in the background).
- ``-p 8080:8080`` - map port 8080 of the host to port 8080 in the container.
- ``shellhttpd:1.0`` - the image to use.
- ``--name`` - assigned a name to your container.


To test your container, you can open a browser window on ``http://127.0.0.1:8080/`` or use curl on your terminal:

.. prompt:: bash host:~$, auto

    host:~$ curl 127.0.0.1:8080

**Example Output**:

.. prompt:: text

     OK

Extra commands
^^^^^^^^^^^^^^

Some commands are really useful when you are using a Docker container.

docker ps
^^^^^^^^^

The first one is the ``docker ps``. If you run it with ``-a``, you will see 
all the containers created. In case you run it just ``docker ps``, the 
default command will show just running containers:

.. prompt:: bash host:~$, auto

    host:~$ docker ps

**Example Output**:

.. prompt:: text

     CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
     244a84742697        shellhttpd:1.0       "/usr/local/bin/http…"   6 minutes ago       Up 6 minutes        0.0.0.0:8080->8080/tcp   shellhttpd

docker logs
^^^^^^^^^^^
It is also very useful to watch the Docker container logs. By using the 
``docker logs <image name>`` you will be able to see the container logs. 
In case you want to keep following the logs, you can use the ``-f``:

In this case, the log could be empty and will just have something if you 
have tested it with curl or with the browser:

.. prompt:: bash host:~$, auto

    host:~$ docker logs -f shellhttpd

**Example Output**:

.. prompt:: text

     GET / HTTP/1.1
     Host: 127.0.0.1:8080
     Connection: keep-alive
     Cache-Control: max-age=0
     DNT: 1
     Upgrade-Insecure-Requests: 1
     User-Agent: Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
     Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
     Sec-Fetch-Site: none
     Sec-Fetch-Mode: navigate
     Sec-Fetch-User: ?1
     Sec-Fetch-Dest: document
     Accept-Encoding: gzip, deflate, br
     Accept-Language: en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7
     
     = Thu Mar 18 01:03:14 UTC 2021 =============================
     GET /favicon.ico HTTP/1.1
     Host: 127.0.0.1:8080
     Connection: keep-alive
     Pragma: no-cache
     Cache-Control: no-cache
     User-Agent: Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
     DNT: 1
     Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
     Sec-Fetch-Site: same-origin
     Sec-Fetch-Mode: no-cors
     Sec-Fetch-Dest: image
     Referer: http://127.0.0.1:8080/
     Accept-Encoding: gzip, deflate, br
     Accept-Language: en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7
     
     = Thu Mar 18 01:03:14 UTC 2021 =============================


docker exec
^^^^^^^^^^^

The ``docker exec`` command runs a new command in a running container.

So if you want to verify the files in the container root file system, you could use:

.. prompt:: bash host:~$, auto

    host:~$ docker exec shellhttpd ls /usr/local/bin/

**Example Output**:

.. prompt:: text

     httpd.sh

To check process running inside the container:

.. prompt:: bash host:~$, auto

    host:~$ docker exec shellhttpd ps

**Example Output**:

.. prompt:: text

     PID   USER     TIME  COMMAND
     1 root      0:00 {httpd.sh} /bin/sh -e /usr/local/bin/httpd.sh
     13 root      0:00 nc -l -p 8080
     36 root      0:00 ps

Finally, you can also jump in a shell inside the container with:

.. prompt:: bash host:~$, auto

    host:~$ docker exec -it shellhttpd sh

**Example Output**:

.. prompt:: bash docker:~$, auto

     docker:~$ ls
     bin    dev    etc    home   lib    media  mnt    opt    proc   root   run    sbin   srv    sys    tmp    usr    var
     docker:~$ exit


Where: 
 - ``-i`` - keep STDIN open even if not attached.
 - ``-t`` - allocate a pseudo-TTY.
 - ``shellhttpd`` - container name.
 - ``sh`` - shell command.

docker rm
^^^^^^^^^

To remove the container, run the command below:

.. prompt:: bash host:~$, auto

    host:~$ docker rm -f shellhttpd
    
Where: 
 - ``-f`` - Force the removal of a running container (uses SIGKILL).

During development, it is very common to change the Docker image and test it 
again, so let’s give it a try:

In the file ``httpd.sh``, we specify the MSG variable with ``${MSG-OK}``. 
This means if MSG is not specified, set it with the default value ``OK``.

Let’s change the OK to FoundriesFactory, rebuild and run:

.. prompt:: bash host:~$, auto

    host:~$ gedit httpd.sh

**httpd.sh**:

.. prompt:: text

     #!/bin/sh -e
     
     PORT="${PORT-8080}"
     MSG="${MSG-FoundriesFactory}"
     
     RESPONSE="HTTP/1.1 200 OK\r\n\r\n${MSG}\r\n"
     
     while true; do
	     echo -en "$RESPONSE" | nc -l -p "${PORT}" || true
	     echo "= $(date) ============================="
     done

Build and run the container again:

.. prompt:: bash host:~$, auto

    host:~$ docker build --tag shellhttpd:1.0 .
    host:~$ docker run --name shellhttpd -d -p 8080:8080 shellhttpd:1.0

Test the new change with curl:

.. prompt:: bash host:~$, auto

    host:~$ curl 127.0.0.1:8080

**Example Output**:

.. prompt:: text

     FoundriesFactory

Docker run command could accept many other parameters. One that could be 
nice to this example is the ``--env`` which will specify a shell variable 
to the container. 
Remove the preview image and launch it again with: ``--env MSG=MyFirstContainer``

Test the new change with curl:

.. prompt:: bash host:~$, auto

    host:~$ docker rm -f shellhttpd
    host:~$ docker run --env MSG=MyFirstContainer --name shellhttpd -d -p 8080:8080 shellhttpd:1.0

Testing the new environment variable:

.. prompt:: bash host:~$, auto

    host:~$ curl 127.0.0.1:8080

**Example Output**:

.. prompt:: text

     MyFirstContainer

Use the exec to echo the MSG variable inside the container:

.. prompt:: bash host:~$, auto

    host:~$ docker exec -it shellhttpd sh
     
**Inside the Container**:

.. prompt:: bash docker:~$, auto

     docker:~$ echo $MSG
      MyFirstContainer
     docker:~$ exit

Remove the container:

.. prompt:: bash host:~$, auto

    host:~$ docker rm -f shellhttpd

All these commands are important in understanding how Docker containers work. 
Now let’s see how docker-compose works.

docker-compose.yml
^^^^^^^^^^^^^^^^^^

This is a YAML file defining services, networks, and volumes for multi-container 
Docker applications. In other words, all the parameters you have used with 
``docker run`` you could specify in a docker-compose.yml file. Then, with a 
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

Change the image parameter to the name and tag we built locally (shellhttpd:1.0):

.. prompt:: bash host:~$, auto

    host:~$ cat docker-compose.yml

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

To run your docker-compose app, execute the ``docker-compose up`` command. 
This command will hold your terminal and log all the container messages 
on it. In case you want to run it in the background you should use ``-d``.

.. prompt:: bash host:~$, auto

    host:~$ docker-compose up -d

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

Conclusion
----------
You have learned the basic commands and structure of Docker and docker-compose 
application. At this point, if you just created your Factory, the initial build 
should finish. In the next tutorial, you will start from here, you will commit 
and push your changes to the remote repository. The CI will then start a new 
build and will deploy this application on your device.

.. warning::

  If you follow this tutorial before flashing and registering your device, 
  return to the Getting Started and complete the section below:

   - :ref:`gs-flash-device`.
   - :ref:`gs-register`.

.. _Docker: https://docs.docker.com/get-docker/