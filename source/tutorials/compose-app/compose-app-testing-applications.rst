Testing Applications
^^^^^^^^^^^^^^^^^^^^

Use ``fioctl`` to enable your new applications but before, make sure to follow 
the ``aktualizr-lite`` logs on your device with the following command:

.. prompt:: bash device:~$, auto

    device:~$  sudo journalctl --follow --unit aktualizr-lite

On your host machine, enable all the new application with the command below:

.. prompt:: bash host:~$, auto

    host:~$ fioctl devices config updates --apps mosquitto,shellhttpd-mqtt,flask-mqtt-nginx <device-name>

**Example Output**:

.. prompt:: text

    Changing apps from: [] -> [mosquitto,shellhttpd-mqtt,flask-mqtt-nginx]
    Changing packagemanager to ostree+compose_apps

In a maximum of 2 minutes, you should see ``aktualizr-lite`` add the application.

Once ``aktualizr-lite`` finishes, check the running containers:

.. prompt:: bash device:~$, auto

    device:~$ docker ps

**Example Output**:

.. prompt:: text

     CONTAINER ID   IMAGE                                    COMMAND                  CREATED          STATUS              PORTS                    NAMES
     9c563d12b2c6   hub.foundries.io/cavel/shellhttpd-mqtt   "/usr/local/bin/http…"   9 minutes ago    Up 9 minutes        0.0.0.0:8082->8082/tcp   shellhttpd-mqtt_httpd-mqtt_1
     ab91fca6c88b   eclipse-mosquitto                        "/docker-entrypoint.…"   9 minutes ago    Up 9 minutes        0.0.0.0:1883->1883/tcp   mosquitto_mosquitto_1
     0b88c1dc7bbf   nginx                                    "/docker-entrypoint.…"   10 minutes ago   Up About a minute   0.0.0.0:80->80/tcp       flask-mqtt-nginx_nginx_1
     129a54e5821b   hub.foundries.io/cavel/flask-mqtt        "python3 -m flask ru…"   10 minutes ago   Up 7 minutes                                 flask-mqtt-nginx_flask-mqtt_1

On your device, follow the ``shellhttpd-mqtt_httpd-mqtt_1`` container logs:

.. prompt:: bash device:~$, auto

    device:~$ docker logs -f shellhttpd-mqtt_httpd-mqtt_1

Using a second terminal, test your applications using ``curl`` in any external device connected to the same network (e.g. your host machine: the same computer you use to access your device with ssh).

.. prompt:: bash host:~$, auto

    host:~$ #Example curl 192.168.15.11:8082
    host:~$ curl <device IP>:8082

**Example Output**:

.. prompt:: text

     Number of Access = 1

At the same time, in the first terminal connected to your device, 
``shellhttpd-mqtt_httpd-mqtt_1`` application logs should show:

**Example Output**:

.. prompt:: text

     Number of Access = 1
     ----------------------

Now, test the ``flask-mqtt-nginx_flask-mqtt_1`` application. First, follow the 
container log on your device with the command:

.. prompt:: bash device:~$, auto

    device:~$ docker logs -f flask-mqtt-nginx_flask-mqtt_1

Using a second terminal, test your applications using ``curl`` in any external 
device connected to the same network (e.g. your host machine: the same computer 
you use to access your device with ssh).

.. prompt:: bash host:~$, auto

    host:~$ #Example curl 192.168.15.11:80
    host:~$ curl <device IP>:80

**Example Output**:

.. prompt:: text

     Number of Access on shellhttpd Container 1

At the same time, in the first terminal connected to your device, 
``flask-mqtt-nginx_flask-mqtt_1`` application logs should show:

**Example Output**:

.. prompt:: text

     172.20.0.3 - - [] "GET / HTTP/1.0" 200 -

Now, as you access the ``shellhttpd-mqtt_httpd-mqtt_1`` application, 
the ``flask-mqtt-nginx_flask-mqtt_1`` will know how many accesses it had and 
will display it when you check the port 80.

Access ``shellhttpd-mqtt_httpd-mqtt_1`` a few more times

.. prompt:: bash host:~$, auto

    host:~$ #Example curl 192.168.15.11:8082
    host:~$ curl <device IP>:8082
    host:~$ curl <device IP>:8082
    host:~$ curl <device IP>:8082
    host:~$ curl <device IP>:8082

**Example Output**:

.. prompt:: text

     Number of Access = 1
     Number of Access = 2
     Number of Access = 3
     Number of Access = 4

Verify if ``flask-mqtt-nginx_flask-mqtt_1`` received all messages and updated the flask page:

.. prompt:: bash host:~$, auto

    host:~$ #Example curl 192.168.15.11:8082
    host:~$ curl <device IP>:80

**Example Output**:

.. prompt:: text

     Number of Access on shellhttpd Container 4