Testing Applications
^^^^^^^^^^^^^^^^^^^^

You will use Fioctl® to enable your new apps,
but first follow the ``aktualizr-lite`` logs on your device with the following command:

.. prompt:: bash device:~$, auto

    device:~$  sudo journalctl --follow --unit aktualizr-lite

On your host machine, enable all the new apps:

.. prompt:: bash host:~$, auto

    host:~$ fioctl devices config updates --apps mosquitto,shellhttpd-mqtt,flask-mqtt-nginx <device-name>

::

    Changing apps from: [] -> [mosquitto,shellhttpd-mqtt,flask-mqtt-nginx]
    Changing packagemanager to ostree+compose_apps

You should shortly see ``aktualizr-lite`` add the apps.

Once ``aktualizr-lite`` finishes, check the running containers:

.. prompt:: bash device:~$, auto

    device:~$ docker ps

::

     CONTAINER ID   IMAGE                                    COMMAND                  CREATED          STATUS              PORTS                    NAMES
     9c563d12b2c6   hub.foundries.io/cavel/shellhttpd-mqtt   "/usr/local/bin/http…"   9 minutes ago    Up 9 minutes        0.0.0.0:8082->8082/tcp   shellhttpd-mqtt_httpd-mqtt_1
     ab91fca6c88b   eclipse-mosquitto                        "/docker-entrypoint.…"   9 minutes ago    Up 9 minutes        0.0.0.0:1883->1883/tcp   mosquitto_mosquitto_1
     0b88c1dc7bbf   nginx                                    "/docker-entrypoint.…"   10 minutes ago   Up About a minute   0.0.0.0:80->80/tcp       flask-mqtt-nginx_nginx_1
     129a54e5821b   hub.foundries.io/cavel/flask-mqtt        "python3 -m flask ru…"   10 minutes ago   Up 7 minutes                                 flask-mqtt-nginx_flask-mqtt_1

On your device, follow the ``shellhttpd-mqtt_httpd-mqtt_1`` container logs:

.. prompt:: bash device:~$, auto

    device:~$ docker logs -f shellhttpd-mqtt_httpd-mqtt_1

In a second terminal, test your apps using ``curl``.
Use any external device connected to the same network, such as your computer.

.. prompt:: bash host:~$, auto

    host:~$ #Example curl 192.168.15.11:8082
    host:~$ curl <device IP>:8082

::

     Number of Access = 1

At the same time, in the first terminal connected to your device, 
the ``shellhttpd-mqtt_httpd-mqtt_1`` logs should show:

::

     Number of Access = 1
     ----------------------

Now, test ``flask-mqtt-nginx_flask-mqtt_1``.
First, follow the container log on your device with the command:

.. prompt:: bash device:~$, auto

    device:~$ docker logs -f flask-mqtt-nginx_flask-mqtt_1

In a second terminal, test your apps using ``curl``.
Use any external device connected to the same network, such as your computer.

.. prompt:: bash host:~$, auto

    host:~$ #Example curl 192.168.15.11:80
    host:~$ curl <device IP>:80

::

     Number of Access on shellhttpd Container 1

In the first terminal connected to your device, 
the ``flask-mqtt-nginx_flask-mqtt_1`` logs should show:

::

     172.20.0.3 - - [] "GET / HTTP/1.0" 200 -

Now, as you access the ``shellhttpd-mqtt_httpd-mqtt_1`` app, 
``flask-mqtt-nginx_flask-mqtt_1`` will track how many accesses there have been.
The total count will be displayed when you check port 80.

Access ``shellhttpd-mqtt_httpd-mqtt_1`` a few more times:

.. prompt:: bash host:~$, auto

    host:~$ #Example curl 192.168.15.11:8082
    host:~$ curl <device IP>:8082
    host:~$ curl <device IP>:8082
    host:~$ curl <device IP>:8082
    host:~$ curl <device IP>:8082

::

     Number of Access = 1
     Number of Access = 2
     Number of Access = 3
     Number of Access = 4

Verify ``flask-mqtt-nginx_flask-mqtt_1`` received all messages and updated the flask page:

.. prompt:: bash host:~$, auto

    host:~$ #Example curl 192.168.15.11:8082
    host:~$ curl <device IP>:80

::

     Number of Access on shellhttpd Container 4
