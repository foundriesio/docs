.. _tutorial-compose-app-file-structure:

File Structure
^^^^^^^^^^^^^^

The file structure in the ``containers.git`` repository is extremely important. 
It defines when the FoundriesFactory CI creates a Docker Image and/or 
creates a Docker Compose Application.

Most Docker Compose App structures will be similar to the ``shellhttpd`` example provided by
default in ``containers.git``, the same example used in the previous tutorials.

Let’s recap the ``shellhttpd`` example structure:

.. prompt:: text

     └── containers
         └── shellhttpd
             ├── docker-build.conf
             ├── docker-compose.yml
             ├── Dockerfile
             ├── httpd.sh
             └── shellhttpd.conf

What is important in the example is the ``shellhttpd`` directory containing 
a ``docker-compose.yml`` and a ``Dockerfile`` file. FoundriesFactory CI will produce 
both a Docker Container Image and Compose App named ``shellhttpd``.