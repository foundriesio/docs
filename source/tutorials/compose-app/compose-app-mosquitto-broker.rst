Mosquitto Broker
^^^^^^^^^^^^^^^^

Starting with the simplest Docker Compose App from the list of examples, the mosquitto container is a 
message broker that implements the MQTT protocol. It allows any device connected 
to the same network to publish or subscribe to topics, allowing us to establish 
communication between different devices.

In this example, it is used slightly differently, instead of different devices 
communicating, two different containers use MQTT to establish a communication between them.

Open a new terminal on your host machine and find the container folder used in the previous tutorial.

.. prompt:: bash host:~$, auto

    host:~$ cd containers/

In the containers folder, use git to download the ``mosquitto`` application from the reference extra-container repository:

.. prompt:: bash host:~$, auto

    host:~$ git remote add fio https://github.com/foundriesio/extra-containers.git
    host:~$ git remote update
    host:~$ git checkout remotes/fio/tutorials -- mosquitto

The ``mosquitto`` application with the ``docker-compose.yml`` file should be inside your ``containers`` folder:

.. prompt:: bash host:~$, auto

    host:~$ tree -L 2 .

Example output:

.. prompt:: text

     .
     ├── mosquitto
     │   └── docker-compose.yml
     ├── README.md
     └── shellhttpd
         ├── docker-build.conf
         ├── docker-compose.yml
         ├── Dockerfile
         ├── httpd.sh
         └── shellhttpd.conf

Check the content of your ``mosquitto/docker-build.conf`` file:

.. prompt:: bash host:~$, auto

    host:~$ cat mosquitto/docker-compose.yml

**mosquitto/docker-compose.yml**:

.. prompt:: text

     # mosquitto/docker-compose.yml
     version: '3.2'
     
     services:
       mosquitto:
         image: eclipse-mosquitto:1.6.12
         restart: unless-stopped
         ports:
           - 1883:1883


The ``mosquitto/docker-compose.yml`` file has all the configuration for the 
``mosquitto`` Docker Compose App.

Where: 

- ``version``: Denotes what Docker Compose version it is using.
- ``services``: Defines all the different containers it will create.
- ``mosquitto``: Name of the first service.
- ``image``: Specifies the pre-built Docker Container Image eclipse-mosquitto version 1.6.12 from ``hub.docker.com``.
- ``restart``: Specify ``unless-stopped``, which means that the Docker Container will restart,  except that when the container is stopped (manually or otherwise), it is not restarted even after Docker daemon restarts.
- ``port``: Map the container’s ports to the host machine