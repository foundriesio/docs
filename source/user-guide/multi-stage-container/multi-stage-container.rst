.. _ug-multi-stage-container:

Multi-Stage Container Builds
============================

When developing for embedded devices, optimization is one of the most 
important things to consider.

Multi-stage builds are useful to optimize your Dockerfiles and keep them 
easy to read and maintain.

You can find more information about it on: `Use multi-stage builds`_.

This guide assumes you have Docker installed on your computer.

To summarize, multi-stage container builds allow you to develop in one stage and 
copy just the necessary artifacts to the next stage. That being said, in the first 
stage you can install dependencies for development, like a toolchain, and compile 
your application. In the final stage, you can keep the image nice and clean with 
just what is necessary for your application while making use of the final artifacts from 
the first stage.

This section will present a Dockerfile implementing a ``helloworld`` application 
written in C. 

In the first example, the Dockerfile is implementing everything 
in a single stage, leaving all the objects and spare software in the image. The 
second example shows how to convert it into a multi-stage container, where the 
build happens in the first stage, and all the objects and spare software 
stay in the first stage. Finally, the second stage copies the binary from the 
first stage and ends up with a smaller and optimized image.

Both examples, single and multi-stage, will use the same file structure:

.. prompt:: text

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

.. prompt:: bash host:~$, auto

    host:~$ gedit helloworld.c

**helloworld.c**:

.. prompt:: text

    #include <stdio.h>
    int main()
    {
      printf("hello, world!\n");
    }
 
    /* helloworld.c */

Create the ``start.sh`` file:

.. prompt:: bash host:~$, auto

    host:~$ gedit start.sh

**start.sh**:

.. prompt:: text

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

.. prompt:: bash host:~$, auto

    host:~$ gedit single/Dockerfile

**single/Dockerfile**:

.. prompt:: text

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

The ``Dockerfile`` is very simple. It installs ``build-essential``, 
copies the files ``helloworld.c`` and ``start.sh`` to the container image, 
compiles ``helloworld.c`` and sets the entrypoint to start the ``start.sh`` script.

Build the docker example and check the image size:

.. prompt:: bash host:~$, auto

    host:~$ docker build --tag single:1.0 -f single/Dockerfile .
    host:~$ docker image ls

**Example Output**:

.. prompt:: text

     docker image ls
     REPOSITORY                         TAG             IMAGE ID       CREATED          SIZE
     single                             1.0             ba94763b6fe4   25 seconds ago   351MB

Run the image and open a second terminal:

.. prompt:: bash host:~$, auto

    host:~$ docker run -it --rm --name single single:1.0

**Example Output**:

.. prompt:: text

     hello, world!
     hello, world!
     hello, world!

In the second terminal, inspect the image and note that the spare files are present in the image:

.. prompt:: bash host:~$, auto

    host:~$ docker exec -it single ls /app

**Example Output**:

.. prompt:: text

     helloworld  helloworld.c  start.sh

Note that the gcc software is present in the image:

.. prompt:: bash host:~$, auto

    host:~$ docker exec -it single sh -c 'type gcc'

**Example Output**:

.. prompt:: text

     gcc is /usr/bin/gcc

Multi-Stage Container
---------------------

Create the ``Dockerfile`` that implements the multi-stage container:

.. prompt:: bash host:~$, auto

    host:~$ gedit multi/Dockerfile

**multi/Dockerfile**:

.. prompt:: text

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

In this case, the ``Dockerfile`` is divided into two stages: ``builder`` and ``final-stage``. 
The first stage starts with ``AS builder`` after specifying the starting image (first line of the Dockerfile). Next, 
it installs ``build-essential`` and compiles ``helloworld.c``.

The second stage starts with ``AS final-stage`` right after specifying the image used 
for the second stage (line 18 of the Dockerfile).
Finally, it ``COPY`` the ``helloworld`` binary from the first stage using the parameter ``--from=builder``.

Build the docker example and check the image size:

.. prompt:: bash host:~$, auto

    host:~$ docker build --tag multi:1.0 -f multi/Dockerfile .
    host:~$ docker image ls

**Example Output**:

.. prompt:: text

     docker image ls
     REPOSITORY                         TAG             IMAGE ID       CREATED          SIZE
     single                             1.0             ba94763b6fe4   25 seconds ago   351MB
     multi                              1.0             bdeac19070ea   50 minutes ago   80.4MB

Note the difference between the `single` and `multi` images. A simple ``helloworld`` 
with just the ``build-essential`` software shows how useful a multi-stage container could be.

Run the image and open a second terminal:

.. prompt:: bash host:~$, auto

    host:~$ docker run -it --rm --name multi multi:1.0

**Example Output**:

.. prompt:: text

     hello, world!
     hello, world!
     hello, world!

In the second terminal, inspect the image and note that only the needed files are 
present in the image (``helloworld.c`` is not installed in the final stage):

.. prompt:: bash host:~$, auto

    host:~$ docker exec -it multi ls /app

**Example Output**:

.. prompt:: text

     helloworld  start.sh

Note that the ``gcc`` software is not installed in the final stage:

.. prompt:: bash host:~$, auto

    host:~$ docker exec -it multi sh -c 'type gcc'

**Example Output**:

.. prompt:: text

     gcc: not found

.. _Use multi-stage builds: https://docs.docker.com/develop/develop-images/multistage-build/