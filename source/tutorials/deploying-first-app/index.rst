.. _tutorial-deploying-first-app:

Deploying your first Application
================================

In the previous tutorial ":ref:`tutorial-creating-first-target`", you created your first 
**Target. This is a very important concept to understand how FoundriesFactory works.
In this tutorial, you will learn how devices consume **Target** as well as how to configure 
your device with desired applications.

.. note::

  Tutorial Estimated Time: 20 minutes

Learning Objectives
-------------------

- Understand aktualizr-lite and fioconfig
- Configure your device with specific applications.
- Watch the over-the-air update.
- Test the running application.

Prerequisites and Prework
-------------------------

- Completed the :ref:`tutorial-gs-with-docker` tutorial.
- Completed the :ref:`tutorial-creating-first-target` tutorial.


Instructions
------------

Configure your device
^^^^^^^^^^^^^^^^^^^^^

At this point, your device should be registered to your Factory according to 
the :ref:`Getting Started guide <gs-register>`. Once your device is registered, two applications start to 
communicate with your Factory: ``aktualizr-lite`` and ``fioconfig``.

**aktualizr-lite**:

This is the daemon responsible for the updates. It checks for new updates and 
implements `The Update Protocol (TUF) <TUF_>`_ to guarantee the integrity of the platform 
and the container updates. 

**fioconfig**:

This is the daemon responsible for managing configuration data for your device. 
The data content used by ``fioconfig`` is encrypted with the device’s public key. 
The device can then get the configuration and use its private key to decrypt. 
``fioconfig`` also stores the encrypted file and extracts it to the userspace.

Both applications are configured to communicate with your Factory every 5 minutes. 
That being said, an update could take from 5 minutes to 10 minutes to be triggered. 
This can be configured according to your product needs.

To improve your experience during this tutorial, you will configure both 
``aktualizr-lite`` and ``fioconfig`` to check every minute.

This configuration will apply just to the device you run the commands below. 
To change it to your entire fleet permanently you have to customize your image.

In your device, create the folder and the file to configure ``aktualizr-lite``:

.. prompt:: bash device:~$

    sudo mkdir -p /etc/sota/conf.d/
    sudo bash -c 'printf "[uptane]\npolling_sec = 60" > /etc/sota/conf.d/z-01-polling.toml'

Create the file to configure ``fioconfig``:

.. prompt:: bash device:~$

    sudo bash -c 'printf "DAEMON_INTERVAL=60" > /etc/default/fioconfig'

Restart both services:

.. prompt:: bash device:~$

    sudo systemctl restart aktualizr-lite
    sudo systemctl restart fioconfig

.. tip::

   In the following instruction, you will disable and enable applications. 
   It will trigger ``aktualizr-lite`` tasks that might be interesting to follow.

   To watch the ``aktualizr-lite`` logs and see the updates, leave a device 
   terminal running the command:

   .. prompt:: bash device:~$

       sudo journalctl -f -u aktualizr-lite


Debugging your device
^^^^^^^^^^^^^^^^^^^^^

Your device should be configured to always download the latest version of a 
specific ``tag``.

By default, devices will run **all** applications that are defined in the ``containers.git`` 
repository and therefore available in the latest **Target**. This behavior can be changed 
by enabling only specific applications. We will cover this in more detail a little later.

To check your device configuration, you can click on the tab :guilabel:`devices` 
on your Factory and find the column :guilabel:`TAGS:`

.. figure:: /_static/tutorials/deploying-first-app/tutorial-device.png
   :width: 900
   :align: center

   Device List

You can also use ``fioctl`` to read information about your device.

.. prompt:: bash host:~$, auto

    host:~$ fioctl device show <device-name>

**Example Output**:

.. prompt:: text

     UUID:		a06b0bab-38be-409b-b7f8-f1125231a91e
     Owner:		6025791fd93b37d33e03b349
     Factory:	cavel
     Up to date:	true
     Target:		raspberrypi3-64-lmp-4 / sha256(3abd308ea6d4caffcdf250c7170e0dc9c8ff9082c64538bf14ca07c2df1beeff)
     Ostree Hash:	3abd308ea6d4caffcdf250c7170e0dc9c8ff9082c64538bf14ca07c2df1beeff
     Created:	2021-04-20T20:54:37+00:00
     Last Seen:	2021-04-20T22:42:53+00:00
     Tags:		devel
     Docker Apps:	shellhttpd
     Network Info:
	     Hostname:	raspberrypi3-64
	     IP:		192.168.15.11
	     MAC:		b8:27:eb:07:42:04
     Hardware Info: (hidden, use --hwinfo)
     Aktualizr config: (hidden, use --aktoml)
     Active Config:
	     Created At:    2021-04-20T20:54:39
	     Applied At:    2021-04-20T20:54:39
	     Change Reason: Set Wireguard pubkey from fioconfig
	     Files:
		     wireguard-client
		      | enabled=0
		      | 
		      | pubkey=dy7jqKcyU3HZHG4sMVO77pafa93lGEEe1atS4v0adng=
     
     -----BEGIN PUBLIC KEY-----
     MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEXQbnokyT1q5Ve+AECntNTS9D560Z
     yx6kgczb3QNAEe/imtGemFvVsir/qxRPVODVdXSlf2doAJ21cv0VL1M++g==
     -----END PUBLIC KEY-----

As expected, the device is configured to follow the ``devel`` tag. Based on that, 
it found and updated to the latest ``devel``, which is version 4.
Because you didn't specify what application it should run, it automatically loads 
all applications available in the current **Target**. In this case, ``shellhttpd``.

Another way to verify applications running in the device is with ``docker ps``:

.. prompt:: bash device:~$, auto

    device:~$ docker ps -a

**Example Output**:

.. prompt:: text

     CONTAINER ID   IMAGE                                  COMMAND                  CREATED       STATUS       PORTS                    NAMES
     48f467ea2461   hub.foundries.io/tutorial/shellhttpd   "/usr/local/bin/http…"   6 hours ago   Up 6 hours   0.0.0.0:8080->8080/tcp   shellhttpd_httpd_1

Testing Container
^^^^^^^^^^^^^^^^^
On your device, ``curl`` is not available, instead run ``wget`` as following to 
test the container:

.. prompt:: bash device:~$, auto

    device:~$ wget -qO- 127.0.0.1:8080

**Example Output**:

.. prompt:: text

     Hello world

You can also test the container from an external device connected to the same 
network. For example, your host machine, the same computer you access your device over ssh.
Run the curl command with the device IP address:

.. prompt:: bash host:~$, auto

    host:~$ #Example curl 192.168.15.11:8080
    host:~$ curl <device IP>:8080

**Example Output**:

.. prompt:: text

     Hello world

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

Conclusion
----------
This tutorial shows you important commands to debug an over-the-air update as well 
as how to enable and disable specific applications. The instructions from this 
Tutorial together with all the previous guides will help with your development cycle.

.. _TUF: https://theupdateframework.com/