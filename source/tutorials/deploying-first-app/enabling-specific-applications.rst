Enabling Specific Applications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As you implement more applications to your ``containers.git``, you might not 
want to run all the applications available on ``containers.git`` to your devices. 
The solution for that is to specify what application the device should run.

Instead of enabling the ``shellhttpd``, which is already done as mentioned before. 
Let's disable and enable it again but before, make sure your device is following the ``aktualizr-lite`` logs with the command:

.. prompt:: bash device:~$

     sudo journalctl -f -u aktualizr-lite

On your host machine, disable the ``shellhttpd`` by replacing the list of app with a simple comma:

.. prompt:: bash host:~$, auto

    host:~$ fioctl devices config updates --compose-apps --apps , <device-name>

**Example Output**:

.. prompt:: text

     Changing apps from: [shellhttpd] -> []
     Changing packagemanager to ostree+compose_apps

In a maximum of 2 minutes, you should see the ``aktualizr-lite`` log removing the application.

Once ``aktualizr-lite`` finished its changes, use ``docker ps`` to see if there is any container running in the device:

.. prompt:: bash device:~$, auto

    device:~$ docker ps -a

**Example Output**:

.. prompt:: text

     CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

Open the ``aktualizr-lite`` log again to follow the log when you enable an application:

.. prompt:: bash device:~$

     sudo journalctl -f -u aktualizr-lite

Enable the ``shellhttpd`` application on your device:

.. prompt:: bash host:~$, auto

    host:~$ fioctl devices config updates --compose-apps --apps shellhttpd <device-name>

**Example Output**:

.. prompt:: text

     Changing apps from: [] -> [shellhttpd]
     Changing packagemanager to ostree+compose_apps

Again in a maximum of 2 minutes, you should see the aktualizr-lite log adding the application.

Test the container again, on your device, running the following command:

.. prompt:: bash device:~$, auto

    device:~$ wget -qO- 127.0.0.1:8080

Check the running containers:

.. prompt:: bash device:~$, auto

    device:~$ docker ps

**Example Output**:

.. prompt:: text

     CONTAINER ID   IMAGE                               COMMAND                  CREATED       STATUS       PORTS                    NAMES
     72a3d00dbc1c   hub.foundries.io/cavel/shellhttpd   "/usr/local/bin/http…"   2 hours ago   Up 2 hours   0.0.0.0:8080->8080/tcp   shellhttpd_httpd_1

