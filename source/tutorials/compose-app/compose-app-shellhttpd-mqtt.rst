Shellhttpd-MQTT
^^^^^^^^^^^^^^^

This application is very similar to the ``shellhttpd`` used in the previous tutorial, 
but instead of returning the specified message like ``Hello World``, it will return 
how many requests the ``netcat`` had. 

The application will also use MQTT to broadcast in the ``containers/requests`` topic 
the total access ``shellhttpd`` had.

In the containers folder, use git to download the ``shellhttpd-mqtt`` application 
from the reference extra-container repository:

.. prompt:: bash host:~$, auto

    host:~$ git checkout remotes/fio/tutorials -- shellhttpd-mqtt

The ``shellhttpd-mqtt`` application should be inside your containers folder:

.. prompt:: bash host:~$, auto

    host:~$ tree -L 2 .

Example output:

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

Check the content of your ``shellhttpd-mqtt/docker-compose.yml`` file:

.. prompt:: bash host:~$, auto

    host:~$ cat shellhttpd-mqtt/docker-compose.yml

**shellhttpd-mqtt/docker-compose.yml**:

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

The ``shellhttpd-mqtt/docker-compose.yml`` file has all the configuration for the 
``shellhttpd-mqtt`` Docker Compose Application.

Where: 

- ``httpd-mqtt``: Name of the first service.
- ``image``: Specifies the Docker Container Image from ``hub.foundries.io/${FACTORY}/shellhttpd-mqtt:latest``. Which is the Container Image created by the FoundriesFactory CI based on the Dockerfile in the ``shellhttpd-mqtt`` folder. In this case, the same folder.
- ``extra_hosts``: Map the container to access the device localhost over the address ``host.docker.internal``.

The ``Dockerfile`` is a text file that contains all the commands to assemble 
the ``hub.foundries.io/${FACTORY}/shellhttpd-mqtt:latest`` Docker Container Image. 

The FoundriesFactory CI will build and publish the image. Finally, the 
Docker Compose Application above will specify it.

Check the content of your ``shellhttpd-mqtt/Dockerfile`` file:

.. prompt:: bash host:~$, auto

    host:~$ cat shellhttpd-mqtt/Dockerfile

**shellhttpd-mqtt/Dockerfile**:

.. prompt:: text

     # shellhttpd-mqtt/Dockerfile
     FROM alpine
     
     RUN apk add --no-cache mosquitto-clients vim
     
     COPY httpd.sh /usr/local/bin/
     
     CMD ["/usr/local/bin/httpd.sh"]

Notice that this image adds the ``mosquitto-clients`` application to the image.

Finally, check the content of your ``shellhttpd-mqtt/httpd.sh`` file:

.. prompt:: bash host:~$, auto

    host:~$ cat shellhttpd-mqtt/httpd.sh

**shellhttpd-mqtt/httpd.sh**:

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

The ``httpd.sh`` in this example is very similar to the one used in the :ref:`tutorial-gs-with-docker`.

The first line in the ``while`` creates the ``RESPONSE`` string with the ``HTTP`` 
response plus the ``Number of Access``.

Next, netcat waits for an access and forward the stdout to the ``tmp.log`` file.
Once it gets an access, the ``grep`` guarantees that it is a ``GET/HTTP/1.1`` 
request and if so, it increments the ``ACCESS`` and sends a message with ``mosquitto_pub``.

The ``mosquitto_pub`` uses the address ``host.docker.internal`` which is mapping 
to the ``localhost`` and will correspond to the mosquitto broker. It is using 
the topic ``containers/requests`` and the message carries the number of access.