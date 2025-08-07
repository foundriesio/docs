Inspecting Factory Targets
^^^^^^^^^^^^^^^^^^^^^^^^^^

At this point, your Factory could have a different number of builds/versions compared to the examples below.

To get started, inspect the Targets you have created:

Use ``fioctl`` on your host machine to list all Target versions:

.. code-block:: console

    $ fioctl targets list

     VERSION  TAGS    APPS                                                   HARDWARE IDs
     -------  ----    ----                                                   ------------
     2        devel                                                          raspberrypi4-64
     3        main                                                           raspberrypi4-64
     3        main                                                           raspberrypi4-64
     4        devel   shellhttpd                                             raspberrypi4-64
     5        devel   shellhttpd                                             raspberrypi4-64
     6        devel   shellhttpd                                             raspberrypi4-64
     7        devel   shellhttpd                                             raspberrypi4-64
     8        devel   shellhttpd-mqtt,mosquitto,shellhttpd,flask-mqtt-nginx  raspberrypi4-64
     9        devel   mosquitto,shellhttpd,flask-mqtt-nginx,shellhttpd-mqtt  raspberrypi4-64

Note that though most versions are tagged with ``devel``, yours may be tagged as ``main``.
This depends on if and when you created the ``devel`` branch.

This tutorial assumes you have applications from  ``containers.git`` on the ``devel`` branch successfully building.

Your device should also be following the ``devel`` tag and running its latest Target with the tag ``devel``. 

Based on the Target version listed above, the device should be running version ``9``.

Use ``fioctl`` on your host machine to verify what Target the device is running.

.. code-block:: console

    $ fioctl device list

     NAME           FACTORY     TARGET                 STATUS  APPS                                        UP-TO-DATE
     ----           -------     ------                 ------  ----                                        ----------
     <device-name>  <factory>   raspberrypi4-64-lmp-9  OK      flask-mqtt-nginx,mosquitto,shellhttpd-mqtt  true

The device is running ``raspberrypi4-64-lmp-9``, which is the Target created for ``raspberrypi4-64`` in the build version ``9``.

To check if your device is following the ``devel`` tag, use ``fioctl`` to inspect the device:

.. code-block:: console

    $ fioctl device show <device-name>

     UUID:		2b7f3164-b288-4c7e-b4e9-2c75c9943dd1
     Owner:		5e13232f73927550af883e7b
     Factory:	<factory>
     Up to date:	true
     Target:		raspberrypi4-64-lmp-9 / sha256(aa7bd4fd638dc1de1459d2d53bcd06887365483e270fb98b84cc8f9f61c44246)
     Ostree Hash:	aa7bd4fd638dc1de1459d2d53bcd06887365483e270fb98b84cc8f9f61c44246
     Created:	2021-05-25T14:36:44+00:00
     Last Seen:	2021-05-25T23:09:33+00:00
     Tags:		devel
     Docker Apps:	flask-mqtt-nginx,mosquitto,shellhttpd-mqtt
     Network Info:
	     Hostname:	raspberrypi4-64
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


If your device is not following ``devel``, flash the latest ``platform-devel`` on your device and register the device again.
