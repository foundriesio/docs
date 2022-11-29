Docker Container Image
^^^^^^^^^^^^^^^^^^^^^^

The file structure responsible for creating the Docker Container Image is:

.. prompt:: text

     └── containers
         └── shellhttpd
             └── Dockerfile

The combination of a top-level directory containing a ``Dockerfile`` will end-up 
in a Docker Container Image. 
It will be compiled by FoundriesFactory CI and published in your `Factory hub. <https://hub-ui.foundries.io/>`_

.. figure:: /_static/tutorials/compose-app/hub.png
   :width: 600
   :align: center

   FoundriesFactory hub.

For FoundriesFactory, Docker Compose Apps are the recommended way for creating applications and a 
Docker Compose App is built using a Docker Container Image.
