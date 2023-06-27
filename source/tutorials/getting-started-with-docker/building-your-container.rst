Building Your Container
^^^^^^^^^^^^^^^^^^^^^^^

Now that you have a ``Dockerfile``, you can build it locally to make sure it is working properly.

From the same folder containing the ``Dockerfile``, run the command:

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

Next, start the container on your host PC:

.. prompt:: bash host:~$

    docker run -d -p 8080:8080 --name shellhttpd shellhttpd:1.0


- ``-d`` - run the container in detached mode (in the background).
- ``-p 8080:8080`` - map port 8080 of the host to port 8080 in the container.
- ``shellhttpd:1.0`` - the image to use.
- ``--name`` - assigned a name to your container.


To test your container, open a browser window to ``http://127.0.0.1:8080/`` or use the ``curl`` command:

.. prompt:: bash host:~$, auto

    host:~$ curl 127.0.0.1:8080

**Example Output**:

.. prompt:: text

     OK
