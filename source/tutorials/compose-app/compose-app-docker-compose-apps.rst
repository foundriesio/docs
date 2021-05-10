Docker Compose Apps
^^^^^^^^^^^^^^^^^^^

The file structure responsible for creating a Docker Compose App is:

.. prompt:: text

     └── containers
         └── shellhttpd
             └── docker-compose.yml

The combination of a top-level directory containing a ``docker-compose.yml`` file
will end-up in a Docker Compose App.

The ``docker-compose.yml`` file specifies one or more containers to run and each container configuration. 

Foundries hub as source
"""""""""""""""""""""""

**Dockerfile in the same folder**

In the ``shellhttpd`` example, the ``docker-compose.yml`` file specified the Docker 
Container Image from the Foundries hub: ``hub.foundries.io/${FACTORY}/shellhttpd:latest``.
In this case, the Docker Container Image ``shellhttpd`` is generated 
by ``Dockerfile`` in the ``shellhttpd`` folder.

.. prompt:: text

     └── containers
         └── shellhttpd
             ├── docker-compose.yml
             └── Dockerfile

**shellhttpd/docker-compose.yml**:

.. prompt:: text

     services:
       httpd:
         image: hub.foundries.io/${FACTORY}/shellhttpd:latest

**Dockerfile in a different folder**

In some cases, the Docker Container Image comes from a different 
application created in the ``containers.git`` repository. 
This is very common when you have a Docker Container Image used by multiple Docker Compose Apps.

For example:

.. prompt:: text

     └── containers
         ├── app
         │   └── docker-compose.yml
         └── grafana
             └── Dockerfile

In this case, the ``app/docker-compose.yml`` file looks like this:

**app/docker-compose.yml**:

.. prompt:: text

     services:
       dashboard:
         image: hub.foundries.io/${FACTORY}/grafana:latest

External hub as source
""""""""""""""""""""""

A Docker Compose App can specify a Docker Container Image from an 
external host. A good example is images from `Docker hub. <https://hub.docker.com/>`_

For example:

.. prompt:: text

     └── containers
         └── mosquitto
             └── docker-compose.yml

In this case, the ``app/docker-compose.yml`` file looks like this:

**app/docker-compose.yml**:

.. prompt:: text

     services:
       mosquitto:
         image: eclipse-mosquitto:1.6.12

Multiple source
"""""""""""""""

Last but not least, you can mix all the three examples on simple or multiple 
container applications. For example:

.. prompt:: text

     └── containers
         ├── shellhttpd
         │   ├── docker-compose.yml
         │   └── Dockerfile
         └── grafana
             └── Dockerfile


In this case, the ``shellhttpd/docker-compose.yml`` file specify three different 
Docker Container Images:

**app/docker-compose.yml**:

.. prompt:: text

     services:
       httpd:
         image: hub.foundries.io/${FACTORY}/shellhttpd:latest
       dashboard:
         image: hub.foundries.io/${FACTORY}/grafana:latest
       mosquitto:
         image: eclipse-mosquitto:1.6.12

- ``httpd``: A Docker Container Image created from the same ``shellhttpd`` folder.
- ``dashboard``: A Docker Container Image created from the ``grafana`` folder.
- ``mosquitto``: The mosquitto Docker Container Image from ``hub.docker.com``.