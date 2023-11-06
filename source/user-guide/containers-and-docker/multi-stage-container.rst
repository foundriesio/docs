.. _ug-multi-stage-container:

Multi-Stage Container Builds
============================

Optimization is always a consideration when developing for embedded devices.
Using Multi-stage builds optimize your Dockerfiles, and keep them easier to read and maintain.

.. seealso::
   Docker's documentation on `multi-stage builds`_.

This guide assumes you have Docker installed on your computer.

To summarize, multi-stage container builds allow you to develop in one stage, then copy only the necessary artifacts to the next stage.
In the first stage you can install dependencies for development, like a toolchain, and compile your application.
In the final stage, the image is kept clean with just the necessities for your application.
This is done by making use of the final artifacts from the first stage.

This guide presents a Dockerfile implementing a ``helloworld`` application written in C. 

In the first example, the Dockerfile is implementing everything in a single stage, leaving all objects and spare software in the image.

The second example shows how to convert this into a multi-stage container.
This time, the build happens in the first stage, and the second stage copies the binary—ending with a smaller and optimized image.

Both examples use the same file structure:

::

     ├── single
     │   └── Dockerfile
     ├── multi
     │   └── Dockerfile
     ├── helloworld.c
     └── start.sh

Create the file structure:

.. prompt:: bash host:~$, auto

    host:~$ mkdir example
    host:~$ cd example
    host:~$ mkdir single multi

Create the ``helloworld.c`` file:

.. code-block:: c

    #include <stdio.h>
    int main()
    {
      printf("hello, world!\n");
    }
 
    /* helloworld.c \*/

Create the ``start.sh`` file:

.. code-block:: bash

    #!/bin/sh
    
    while :
    do
      /app/helloworld
      sleep 5
    done

Add execute permission to ``start.sh``:

.. prompt:: bash host:~$, auto

    host:~$ chmod +x start.sh

Single Stage Container
----------------------

Create the ``Dockerfile`` that implements the single stage container:

``single/Dockerfile``:

.. code-block:: dockerfile

    FROM debian:bullseye-slim
    RUN  echo "-------Single-Stage--------------"
    
    #Install packages
    RUN apt-get update && \
        apt-get install -y --no-install-recommends build-essential && \
        rm -rf /var/lib/apt/lists/*
    
    RUN mkdir -p /app/
    
    COPY ../helloworld.c /app/
    COPY ../start.sh /app/

    WORKDIR /app/
    
    RUN gcc helloworld.c -o helloworld
    
    ENTRYPOINT ["/app/start.sh"]

The ``Dockerfile`` is straightforward.
It installs ``build-essential``, copies the files ``helloworld.c`` and ``start.sh`` to the container image,
then compiles ``helloworld.c`` and sets the entrypoint to start the ``start.sh`` script.

Build the Docker image and check the image size:

.. prompt:: bash host:~$, auto

    host:~$ docker build --tag single:1.0 -f single/Dockerfile .
    host:~$ docker image ls

::

     docker image ls
     REPOSITORY                         TAG             IMAGE ID       CREATED          SIZE
     single                             1.0             ba94763b6fe4   25 seconds ago   351MB

Run the image and open a second terminal:

.. prompt:: bash host:~$, auto

    host:~$ docker run -it --rm --name single single:1.0

::

     hello, world!
     hello, world!
     hello, world!

In the second terminal, inspect the image and note that the spare files are present in the image:

.. prompt:: bash host:~$, auto

    host:~$ docker exec -it single ls /app

::

     helloworld  helloworld.c  start.sh

Note that the GCC compiler is present in the image:

.. prompt:: bash host:~$, auto

    host:~$ docker exec -it single sh -c 'type gcc'

::

     gcc is /usr/bin/gcc

Multi-Stage Container
---------------------

Create the ``Dockerfile`` to implement the multi-stage container:

``multi/Dockerfile``:

.. code-block:: dockerfile

    FROM debian:bullseye-slim AS builder
    RUN  echo "-------Multi-Stage--------------"
    
    #Install packages for the builder stage
    RUN apt-get update && \
        apt-get install -y --no-install-recommends build-essential && \
        rm -rf /var/lib/apt/lists/*
    
    RUN mkdir -p /app/
    
    COPY helloworld.c /app/
    
    WORKDIR /app/
    
    RUN gcc helloworld.c -o helloworld
    
    RUN  echo "-------Final Stage--------------"
    FROM debian:bullseye-slim AS final-stage
    
    #Install packages for the final stage
    RUN apt-get update && \
        rm -rf /var/lib/apt/lists/*
    
    RUN mkdir -p /app/
    
    COPY --from=builder /app/helloworld /app/
    
    WORKDIR /app/
    
    COPY start.sh /app/
    
    ENTRYPOINT ["/app/start.sh"]

This ``Dockerfile`` is divided into two stages: ``builder`` and ``final-stage``. 
The first stage starts with ``AS builder`` after specifying the starting image (first line of the Dockerfile).
Next, it installs ``build-essential`` and compiles ``helloworld.c``.

The second stage starts with ``AS final-stage`` after specifying the image to be used. (line 18 of the Dockerfile).
Finally, ``COPY`` get the ``helloworld`` binary from the first stage using the parameter ``--from=builder``.

Build the Docker image and check the image size:

.. prompt:: bash host:~$, auto

    host:~$ docker build --tag multi:1.0 -f multi/Dockerfile .
    host:~$ docker image ls

::

     docker image ls
     REPOSITORY                         TAG             IMAGE ID       CREATED          SIZE
     single                             1.0             ba94763b6fe4   25 seconds ago   351MB
     multi                              1.0             bdeac19070ea   50 minutes ago   80.4MB

Note the difference between the `single` and `multi` images.

Run the image and open a second terminal:

.. prompt:: bash host:~$, auto

    host:~$ docker run -it --rm --name multi multi:1.0

::

     hello, world!
     hello, world!
     hello, world!

In the second terminal, inspect the image.
Note that only the required files are present in the image (``helloworld.c`` is not installed in the final stage):

.. prompt:: bash host:~$, auto

    host:~$ docker exec -it multi ls /app

::

     helloworld  start.sh

Notice how ``gcc`` is not installed in the final stage:

.. prompt:: bash host:~$, auto

    host:~$ docker exec -it multi sh -c 'type gcc'

::

     gcc: not found

.. _multi-stage builds: https://docs.docker.com/build/building/multi-stage/
