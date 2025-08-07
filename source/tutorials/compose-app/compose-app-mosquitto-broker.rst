Mosquitto Broker
^^^^^^^^^^^^^^^^

We will start with the mosquitto container, which acts as a *message broker* that implements the MQTT protocol.
It allows any device connected to the same network to publish or subscribe to topics.
This allows for establishing communication between different devices.

In this example, it is used slightly differently.
Instead of different devices communicating, two different containers will use MQTT to establish communication between them.

Open a new terminal on your host machine and find the container folder used previously.

.. code-block:: console

    $ cd containers/

While in the containers folder, use git to download ``mosquitto`` from the ``extra-containers`` repo:

.. code-block:: console

    $ git remote add fio https://github.com/foundriesio/extra-containers.git
    $ git remote update
    $ git checkout remotes/fio/tutorials -- mosquitto

The ``mosquitto`` app with ``docker-compose.yml`` should now be inside your ``containers`` folder:

.. code-block:: console

    $ tree -L 2 .

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

Check the content of ``mosquitto/docker-compose.yml``:

.. code-block:: console

    $ cat mosquitto/docker-compose.yml

.. code-block:: yaml

     # mosquitto/docker-compose.yml
     version: '3.2'
     
     services:
       mosquitto:
         image: eclipse-mosquitto:1.6.12
         restart: unless-stopped
         ports:
           - 1883:1883


The ``mosquitto/docker-compose.yml`` file has all the configuration for the ``mosquitto`` app: 

- ``version``: Denotes what Docker Compose version it is using.
- ``services``: Defines the containers it will create.
- ``mosquitto``: Name of the first service.
- ``image``: Specifies the pre-built Docker container image, eclipse-mosquitto version 1.6.12 from ``hub.docker.com``.
- ``restart``: Specifies ``unless-stopped``, which means that the Docker container will not restart if the container is stopped—manually or otherwise—even after the Docker daemon restarts.
- ``port``: Map the container’s ports to the host machine
