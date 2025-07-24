Debugging Your Device
^^^^^^^^^^^^^^^^^^^^^

Your device is configured to always download the latest **Target** version with a specific ``tag``.

By default, devices run **all** applications defined in the ``containers.git`` repo.
This behavior can be changed by enabling only specific applications.
This will be covered this in more detail later.

To check your device configuration, click on the Factory tab :guilabel:`devices` and find the column :guilabel:`TAGS`:

.. figure:: /_static/tutorials/deploying-first-app/tutorial-device.png
   :width: 900
   :align: center

   Device List

You can also use ``fioctl`` to read information about your device.

.. prompt:: bash host:~$, auto

    host:~$ fioctl device show <device-name>

::

     UUID:          a06b0bab-38be-409b-b7f8-f1125231a91e
     Owner:         6025791fd93b37d33e03b349
     Factory:	    <factory>
     Up to date:    true
     Target:        raspberrypi4-64-lmp-4 / sha256(3abd308ea6d4caffcdf250c7170e0dc9c8ff9082c64538bf14ca07c2df1beeff)
     Ostree Hash:   3abd308ea6d4caffcdf250c7170e0dc9c8ff9082c64538bf14ca07c2df1beeff
     Created:       2021-04-20T20:54:37+00:00
     Last Seen:     2021-04-20T22:42:53+00:00
     Tags:          main
     Docker Apps:   shellhttpd
     Network Info:
	     Hostname:  raspberrypi4-64
	     IP:        192.168.15.11
	     MAC:       b8:27:eb:07:42:04
     Hardware Info:    (hidden, use --hwinfo)
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

The device is configured to follow the ``main`` tag.
Based on that, it found and updated to the latest Target with the tag.
Because we did not specify what application should run, all apps available in the current Target are automatically loaded.
In this case, ``shellhttpd``.

Another way to verify the apps running on a device is with ``docker ps``:

.. prompt:: bash device:~$, auto

    device:~$ docker ps

::

     CONTAINER ID   IMAGE                                  COMMAND                  CREATED       STATUS       PORTS                    NAMES
     48f467ea2461   hub.foundries.io/<factory>/shellhttpd   "/usr/local/bin/http…"   6 hours ago   Up 6 hours   0.0.0.0:8080->8080/tcp   shellhttpd_httpd_1
