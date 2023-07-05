Shellhttpd-MQTT
^^^^^^^^^^^^^^^

This is similar to the ``shellhttpd`` used in the previous tutorial, 
but instead of returning the specified message like ``Hello World``,
it returns how many requests ``netcat`` had. 

This app also uses MQTT to broadcast the total access count of ``shellhttpd`` in ``containers/requests``.

While in the containers folder, use git to download ``shellhttpd-mqtt`` from the ``extra-containers`` repo:

.. prompt:: bash host:~$, auto

    host:~$ git checkout remotes/fio/tutorials -- shellhttpd-mqtt

The ``shellhttpd-mqtt`` app should now be inside your containers folder:

.. prompt:: bash host:~$, auto

    host:~$ tree -L 2 .

.. prompt:: text

     .
     ├── mosquitto
     │   └── docker-compose.yml
     ├── README.md
     ├── shellhttpd
     │   ├── docker-build.conf
     │   ├── docker-compose.yml
     │   ├── Dockerfile
     │   ├── httpd.sh
     │   └── shellhttpd.conf
     └── shellhttpd-mqtt
         ├── docker-compose.yml
         ├── Dockerfile
         └── httpd.sh

Check the content of ``shellhttpd-mqtt/docker-compose.yml``:

.. prompt:: bash host:~$, auto

    host:~$ cat shellhttpd-mqtt/docker-compose.yml

.. prompt:: text

     # shellhttpd-mqtt/docker-compose.yml
     version: '3.2'
     
     services:
       httpd-mqtt:
         image: hub.foundries.io/${FACTORY}/shellhttpd-mqtt:latest
         restart: unless-stopped
         ports:
           - 8082:${PORT-8082}
         extra_hosts:
           - "host.docker.internal:host-gateway"

The ``shellhttpd-mqtt/docker-compose.yml`` file has the configuration for the ``shellhttpd-mqtt`` app: 

- ``httpd-mqtt``: Name of the first service.
- ``image``: Specifies the Docker container image from ``hub.foundries.io/${FACTORY}/shellhttpd-mqtt:latest``. This was created by the FoundriesFactory CI based on the Dockerfile in ``shellhttpd-mqtt``. In this case, the same folder.
- ``extra_hosts``: Map the container to access the device ``localhost`` over the address ``host.docker.internal``.

``Dockerfile`` contains the commands to assemble the ``hub.foundries.io/${FACTORY}/shellhttpd-mqtt:latest`` Docker container image. 

The FoundriesFactory® CI will build and publish the image.
Finally, the Docker Compose Application above will specify it.

Check the content of ``shellhttpd-mqtt/Dockerfile``:

.. prompt:: bash host:~$, auto

    host:~$ cat shellhttpd-mqtt/Dockerfile

.. prompt:: text

     # shellhttpd-mqtt/Dockerfile
     FROM alpine
     
     RUN apk add --no-cache mosquitto-clients vim
     
     COPY httpd.sh /usr/local/bin/
     
     CMD ["/usr/local/bin/httpd.sh"]

Notice that this image adds the ``mosquitto-clients`` app to the image.
Finally, check the content of ``shellhttpd-mqtt/httpd.sh``:

.. prompt:: bash host:~$, auto

    host:~$ cat shellhttpd-mqtt/httpd.sh

.. prompt:: text

     #!/bin/sh
     PORT="${PORT-8082}"
     ACCESS=1
     while true; do
	     RESPONSE="HTTP/1.1 200 OK\r\n\r\nNumber of Access = ${ACCESS}\r\n"
	     echo -en "$RESPONSE" | nc -l -p "${PORT}" > ./tmp.log || true
	     if grep -q "GET / HTTP/1.1" ./tmp.log; then
		     echo "Number of Access = $ACCESS"
		     mosquitto_pub -h host.docker.internal -t "containers/requests" -m "ACCESS=$ACCESS"
		     ACCESS=$((ACCESS+1))
		     echo "----------------------"
	     fi
     done

This ``httpd.sh`` script is similar to the one used in :ref:`tutorial-gs-with-docker`.

The first line in the ``while`` loop creates the ``RESPONSE`` string from the ``HTTP`` 
response and ``Number of Access``.

Next, ``netcat`` waits for an access and forwards the stdout to ``tmp.log``.
Once it gets access, ``grep``checks that it is a ``GET/HTTP/1.1`` request.
If so, ``ACCESS`` is incremented, and then a message is sent with ``mosquitto_pub``.

``mosquitto_pub`` uses the address ``host.docker.internal`` which is mapped to``localhost`` and corresponds to the mosquitto broker.
It is using the topic ``containers/requests``, and the message carries the access count.
