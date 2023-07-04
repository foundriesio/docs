Enabling Specific Applications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As you implement more apps in ``containers.git``, you may not want all of them running on every device.
Fioctl® can specify what apps a device should run.

Instead of enabling ``shellhttpd`` as done before, we will use ``fioctl`` to first disable and then enable ``shellhttpd``.
Make sure to follow the ``aktualizr-lite`` logs on your device with the following command:

.. prompt:: bash device:~$

     sudo journalctl --follow --unit aktualizr-lite

On your host machine, disable ``shellhttpd`` by replacing the list of apps with a simple comma:

.. prompt:: bash host:~$, auto

    host:~$ fioctl devices config updates --apps , <device-name>
    
::

    Changing apps from: [shellhttpd] -> []
    Changing packagemanager to ostree+compose_apps

You should shortly see ``aktualizr-lite`` remove the app.
Once ``aktualizr-lite`` finishes, use ``docker ps`` to see if there are any containers running on the device:

.. prompt:: bash device:~$, auto

    device:~$ docker ps

::
   
   CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

On the device, open the log again and watch as you re-enable ``shellhttpd``:

.. prompt:: bash device:~$

     sudo journalctl --follow --unit aktualizr-lite

Enable the ``shellhttpd`` application on your device:

.. prompt:: bash host:~$, auto

    host:~$ fioctl devices config updates --apps shellhttpd <device-name>

::

 Changing apps from: [] -> [shellhttpd]
 Changing packagemanager to ostree+compose_apps

You should soon see ``aktualizr-lite`` add the app.
On your device, test the container again by running the following command:

.. prompt:: bash device:~$, auto

    device:~$ wget -qO- 127.0.0.1:8080

::

  Hello world

Check the running containers:

.. prompt:: bash device:~$, auto

    device:~$ docker ps

::

    CONTAINER ID   IMAGE                               COMMAND                  CREATED       STATUS       PORTS                    NAMES
    72a3d00dbc1c   hub.foundries.io/<factory>/shellhttpd   "/usr/local/bin/http…"   2 hours ago   Up 2 hours   0.0.0.0:8080->8080/tcp   shellhttpd_httpd_1

