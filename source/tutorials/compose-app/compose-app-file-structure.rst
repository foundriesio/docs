.. _tutorial-compose-app-file-structure:

File Structure
^^^^^^^^^^^^^^

Pay attention to the file structure in the ``containers.git`` repo. 
It defines when the FoundriesFactory® CI creates a Docker image or creates a Docker Compose App.

Most Docker Compose App structures will be similar to the ``shellhttpd`` example provided in ``containers.git``.
This is the same example used in the previous tutorials.

Let’s recap the ``shellhttpd`` app structure:

.. prompt:: text

     └── containers
         └── shellhttpd
             ├── docker-build.conf
             ├── docker-compose.yml
             ├── Dockerfile
             ├── httpd.sh
             └── shellhttpd.conf

What is important is the ``shellhttpd`` directory containing ``docker-compose.yml`` and ``Dockerfile``.
The FoundriesFactory CI will produce both a Docker container image and Compose App named ``shellhttpd``.
