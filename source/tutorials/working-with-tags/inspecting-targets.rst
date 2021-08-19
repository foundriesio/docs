Inspecting your Factory Targets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
At this point, your Factory could have a different number of builds/versions 
comparing to the examples below.

To get started, inspect all your **Targets** you have created in your Factory.

Use ``fioctl`` on your host machine to list all **Target** versions:

.. prompt:: bash host:~$, auto

    host:~$ fioctl targets list

**Example Output**:

.. prompt:: text

     VERSION  TAGS    APPS                                                   HARDWARE IDs
     -------  ----    ----                                                   ------------
     2        devel                                                          raspberrypi3-64
     3        master                                                         raspberrypi3-64
     4        devel   shellhttpd                                             raspberrypi3-64
     5        devel   shellhttpd                                             raspberrypi3-64
     6        devel   shellhttpd                                             raspberrypi3-64
     7        devel   shellhttpd                                             raspberrypi3-64
     8        devel   shellhttpd-mqtt,mosquitto,shellhttpd,flask-mqtt-nginx  raspberrypi3-64
     9        devel   mosquitto,shellhttpd,flask-mqtt-nginx,shellhttpd-mqtt  raspberrypi3-64

You might not have ``9`` versions. It depends on how many builds you 
trigger on your FondriesFactory CI.

Note that most versions are tagged with ``devel`` because we have used the 
``devel`` branch on previous tutorials.

This tutorial assumes you have all applications from your ``containers.git`` at 
``devel`` repository successfully building.

Your device should also be following the ``devel`` tag and running its latest 
**Target** with the tag ``devel``. 

Based on the **Target** version listed above, the device should be running version ``9``.

Use ``fioctl`` on your host machine to verify what **Target** the device is running.

.. prompt:: bash host:~$, auto

    host:~$ fioctl device list

**Example Output**:

.. prompt:: text

     NAME           FACTORY     TARGET                 STATUS  APPS                                        UP-TO-DATE
     ----           -------     ------                 ------  ----                                        ----------
     <device-name>  <factory>   raspberrypi3-64-lmp-9  OK      flask-mqtt-nginx,mosquitto,shellhttpd-mqtt  true

As you can see above, the device is running ``raspberrypi3-64-lmp-9`` which is 
the **Target** created for ``raspberrypi3-64`` in the build version ``9``.

To make sure your device is configured to follow the ``devel`` tag, use ``fioctl``
to inspect the device:

.. prompt:: bash host:~$, auto

    host:~$ fioctl device show <device-name>

**Example Output**:

.. prompt:: text

     UUID:		2b7f3164-b288-4c7e-b4e9-2c75c9943dd1
     Owner:		5e13232f73927550af883e7b
     Factory:	<factory>
     Up to date:	true
     Target:		raspberrypi3-64-lmp-9 / sha256(aa7bd4fd638dc1de1459d2d53bcd06887365483e270fb98b84cc8f9f61c44246)
     Ostree Hash:	aa7bd4fd638dc1de1459d2d53bcd06887365483e270fb98b84cc8f9f61c44246
     Created:	2021-05-25T14:36:44+00:00
     Last Seen:	2021-05-25T23:09:33+00:00
     Tags:		devel
     Docker Apps:	flask-mqtt-nginx,mosquitto,shellhttpd-mqtt
     Network Info:
	     Hostname:	raspberrypi3-64
	     IP:		192.168.15.11
         MAC:		b8:27:eb:07:42:04
     Hardware Info: (hidden, use --hwinfo)
     Aktualizr config: (hidden, use --aktoml)
     Active Config:
	     Created At:    2021-05-25T17:24:51
	     Applied At:    2021-05-25T17:25:00
	     Change Reason: Override aktualizr-lite update configuration 
	     Files:
		     z-50-fioctl.toml - [/usr/share/fioconfig/handlers/aktualizr-toml-update]
		      | 
		      | [pacman]
		      |   compose_apps = "mosquitto,shellhttpd-mqtt,flask-mqtt-nginx"
		      |   compose_apps_root = "/var/sota/compose-apps"
		      |   docker_apps = "mosquitto,shellhttpd-mqtt,flask-mqtt-nginx"
		      |   type = "ostree+compose_apps"
		      | 
		     shellhttpd.conf
		     wireguard-client
     	      | enabled=0
		      | 
		      | pubkey=eFGUdEZsSyQ3bR3uEM2ZmCJcC6W1WHc5z287uSd+qw8=
     
     -----BEGIN PUBLIC KEY-----
     MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEIgio7HCdX4yG+cLst5ausM3b6bvd
     /lQvPR8gJM+byg4zx4iu6TIFh0Xx+VkoYjhy0wnamEciV7VbuQZopP4Ffw==
     -----END PUBLIC KEY-----

Note that the device is configured with tag: ``devel``.

In case your device is not following ``devel``, flash the latest ``platform-devel`` 
on your device and register the device again.  