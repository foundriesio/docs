Adapting Shellhttpd
^^^^^^^^^^^^^^^^^^^

Edit ``shellhttpd`` back to its original state.

.. tip::

  If you do not have the ``shellhttpd`` application, complete :ref:`tutorial-creating-first-target`.

Open a terminal on your host machine and go into your ``containers`` repo folder.

.. prompt:: bash host:~$, auto

    host:~$ cd containers/

Edit ``httpd.sh``:

.. prompt:: bash host:~$, auto

    host:~$ vi shellhttpd/httpd.sh

.. prompt:: text

     #!/bin/sh -e
     
     PORT="${PORT-8080}"
     MSG="${MSG-OK}"
     
     RESPONSE="HTTP/1.1 200 OK\r\n\r\n${MSG}\r\n"
     
     while true; do
	     echo -en "$RESPONSE" | nc -l -p "${PORT}" || true
	     echo "= $(date) ============================="
     done

Edit ``Dockerfile``:

.. prompt:: bash host:~$, auto

    host:~$ vi shellhttpd/Dockerfile

.. prompt:: text

     FROM alpine
     
     COPY httpd.sh /usr/local/bin/
     
     CMD ["/usr/local/bin/httpd.sh"]

Edit ``docker-compose.yml``:

.. prompt:: bash host:~$, auto

    host:~$ vi shellhttpd/docker-compose.yml

.. prompt:: text

     version: '3.2'
     
     services:
       httpd:
         image: hub.foundries.io/<factory>/shellhttpd:latest
         restart: always
         ports:
           - 8080:${PORT-8080}
         environment:
           MSG: "${MSG-Hello world}"

Commit and push all changes:

.. prompt:: bash host:~$, auto

    host:~$ git status
    host:~$ git add shellhttpd/docker-compose.yml
    host:~$ git add shellhttpd/httpd.sh
    host:~$ git add shellhttpd/Dockerfile
    host:~$ git commit -m "Changes for adapting shellhttpd tutorial"
    host:~$ git push

Wait for your build to finish by checking the latest Target on the :guilabel:`Devices` tab.

Use ``fioctl`` to configure your device to run just the ``shellhttpd`` application:

.. prompt:: bash host:~$, auto

    host:~$ fioctl devices config updates --apps shellhttpd <device-name>

::

     Changing apps from: [] -> [shellhttpd]
     Changing packagemanager to ostree+compose_apps

In a few minutes your device should receive an update.

Test the container on your device:

.. prompt:: bash device:~$, auto

    device:~$ wget -qO- 127.0.0.1:8080

::

     Hello world

Check the Target version list with ``fioctl``

.. prompt:: bash host:~$, auto

    host:~$ fioctl targets list

::

     VERSION  TAGS    APPS                                                   HARDWARE IDs
     -------  ----    ----                                                   ------------
     2        devel                                                          raspberrypi4-64
     3        main                                                           raspberrypi4-64
     4        devel   shellhttpd                                             raspberrypi4-64
     5        devel   shellhttpd                                             raspberrypi4-64
     6        devel   shellhttpd                                             raspberrypi4-64
     7        devel   shellhttpd                                             raspberrypi4-64
     8        devel   shellhttpd-mqtt,mosquitto,shellhttpd,flask-mqtt-nginx  raspberrypi4-64
     9        devel   mosquitto,shellhttpd,flask-mqtt-nginx,shellhttpd-mqtt  raspberrypi4-64
     10       devel   mosquitto,shellhttpd,flask-mqtt-nginx,shellhttpd-mqtt  raspberrypi4-64

Check what Target your device is running:

.. prompt:: bash host:~$, auto

    host:~$ fioctl device list

::

     NAME           FACTORY     TARGET                 STATUS  APPS                                        UP-TO-DATE
     ----           -------     ------                 ------  ----                                        ----------
     <device-name>  <factory>   raspberrypi4-64-lmp-10 OK      flask-mqtt-nginx,mosquitto,shellhttpd-mqtt  true

Whenever you push changes to the ``devel`` branch, the CI will build and generate a new Target tagged with ``devel``.
As a result, devices following ``devel`` will update to the latest Target.
