Enabling Specific Applications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As you implement more applications in ``containers.git``, you may not 
want to run all of them on all of your devices. You can use ``fioctl`` to 
specify what applications the device should run.

Instead of enabling the ``shellhttpd``, which is already done as mentioned before. 
Let's use ``fioctl`` to first disable and then enable the ``shellhttpd`` application.
Make sure to follow the ``aktualizr-lite`` logs on your device with the following command:

.. prompt:: bash device:~$

     sudo journalctl --follow --unit aktualizr-lite

On your host machine, disable ``shellhttpd`` by replacing the list of apps with a simple comma:

.. prompt:: bash host:~$, auto

    host:~$ fioctl devices config updates --compose-apps --apps , <device-name>

**Example Output**:

.. prompt:: text

     Changing apps from: [shellhttpd] -> []
     Changing packagemanager to ostree+compose_apps

In a maximum of 2 minutes, you should see ``aktualizr-lite`` remove the application.

Once ``aktualizr-lite`` finishes its changes, use ``docker ps`` to see if there 
are any containers running on the device:

.. prompt:: bash device:~$, auto

    device:~$ docker ps

**Example Output**:

.. prompt:: text

     CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

On the device, open the ``aktualizr-lite`` log again and watch as you re-enable ``shellhttpd``:

.. prompt:: bash device:~$

     sudo journalctl --follow --unit aktualizr-lite

Enable the ``shellhttpd`` application on your device:

.. prompt:: bash host:~$, auto

    host:~$ fioctl devices config updates --compose-apps --apps shellhttpd <device-name>

**Example Output**:

.. prompt:: text

     Changing apps from: [] -> [shellhttpd]
     Changing packagemanager to ostree+compose_apps

Again in a maximum of 2 minutes, you should see ``aktualizr-lite`` add the application.

On your device, test the container again by running the following command:

.. prompt:: bash device:~$, auto

    device:~$ wget -qO- 127.0.0.1:8080

**Example Output**:

.. prompt:: text

     Hello world

Check the running containers:

.. prompt:: bash device:~$, auto

    device:~$ docker ps

**Example Output**:

.. prompt:: text

     CONTAINER ID   IMAGE                               COMMAND                  CREATED       STATUS       PORTS                    NAMES
     72a3d00dbc1c   hub.foundries.io/<factory>/shellhttpd   "/usr/local/bin/http…"   2 hours ago   Up 2 hours   0.0.0.0:8080->8080/tcp   shellhttpd_httpd_1

