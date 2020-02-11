.. _ref-docker-apps:

Docker Apps
===========

Mentally, Docker Apps can be thought of like docker-compose. There are some
important differences that Docker Apps solve that make it a nice fit for
something like Aktualizr-lite.

Here’s an example of a minimal Docker App file::

 version: 0.1.0
 name: httpd
 description: "A really dumb httpd example"
 ---

 version: '3.2'

 services:
   httpd:
     image: alpine:3.9
     command:
       - /bin/sh
       - -c
       - "echo '${HTTPD}' > /httpd && exec sh /httpd ${PORT} ${MSG}"
     ports:
       - ${PORT}:${PORT}
 ---

 PORT: 8080
 MSG: Hello from Gavin Gavel
 HTTPD: |
   #!/bin/sh
   set -e

   PORT=$$1; shift; MSG=$$*

   while true; do

     echo -en "HTTP/1.1 200 OK\r\n\r\n$$MSG\r\n" | nc -l -p $$PORT || true

   done

You can play with this by running something like::

 # render it with the port changed to 8081
 docker-app render httpd.dockerapp --set PORT=8081 > ./docker-compose.yml
 # launch
 docker-compose up

How Does It Fit Together?
-------------------------

In the world of Aktualizr and TUF, a Docker App can be sent to the TUF
reposerver as a "Target". This means each Docker app will get all the
advantages that Aktualizr and TUF bring for image update security. Each
OSTree Target (ie things your device can update to) include pointers to the
Docker Apps that are valid for it.

The easiest way to conceptualize this is to see an example of the TUF
targets.json::

 {
  ...
  "signed": {
    "targets": {
      httpd.dockerapp-1 : {
        "custom" : {
          "createdAt" : "2019-08-13T03:26:01Z",
          "hardwareIds" : ["all"],
          "name" : "httpd.dockerapp",
          "targetFormat" : "BINARY",
          "updatedAt" : "2019-08-13T03:26:01Z",
          "version" : "1"
        },
        "hashes" : {
           "sha256" : "f0ad4e3ce6a5e9cb70c9d747e977fddfacd08419deec0714622029b12dde8338"
        },
        "length" : 889
      },
      "raspberrypi3-64-lmp-144" : {
        "custom" : {
          "createdAt" : "2019-08-12T22:18:16Z",
          "docker_apps" : {https://github.com/docker/app/blob/master/examples/voting-app/example-parameters/my-environment.yml
             "httpd" : {
                "filename" : "httpd.dockerapp-1"
             }
          },
          "hardwareIds" : ["raspberrypi3-64"],
          "name" : "raspberrypi3-64-lmp",
          "targetFormat" : "OSTREE",
          "updatedAt" : "2019-08-12T22:18:16Z",
          "version" : "144"
       },
       "hashes" : {
          "sha256" : "20ac4f7cd50cda6bfed0caa1f8231cc9a7e40bec60026c66df5f7e143af96942"
       },
       "length" : 0
      }
    }
  }
 }

In this example we have a single "httpd" Docker App. The "144" LMP image then
points its custom "docker_apps" value to that specific version. We could then
produce a new version of the Docker App which would create two new targets:
one for the docker-app and one for the new OSTree target. **NOTE:** While its
a "new" target, the OSTree hash is the same as the one for "144"::

 {
  ...
  "signed": {
    "targets": {
    ... <previous targets>
      httpd.dockerapp-2 : {
        "custom" : {
          "createdAt" : "2019-08-14T03:26:01Z",
          "hardwareIds" : ["all"],
          "name" : "httpd.dockerapp",
          "targetFormat" : "BINARY",
          "updatedAt" : "2019-08-14T03:26:01Z",
          "version" : "2"
        },
        "hashes" : {
           "sha256" : "f1ad4e3ce6a5e9cb70c9d747e977fddfacd08419deec0714622029b12dde8338"
        },
        "length" : 890
      },
      "raspberrypi3-64-lmp-145" : {
        "custom" : {
          "createdAt" : "2019-08-12T22:18:16Z",
          "docker_apps" : {
             "httpd" : {
                "filename" : "httpd.dockerapp-2"
             }
          },
          "hardwareIds" : ["raspberrypi3-64"],
          "name" : "raspberrypi3-64-lmp",
          "targetFormat" : "OSTREE",
          "updatedAt" : "2019-08-12T22:18:16Z",
          "version" : "144"
       },
       "hashes" : {
          "sha256" : "20ac4f7cd50cda6bfed0caa1f8231cc9a7e40bec60026c66df5f7e143af96942"
       },
       "length" : 0
      }
    }
  }
 }

This allows the next update to be effectively a no-op for the base OS image, but it does bring in the updated Docker App(s).

Parameters
----------

Parameterizing can be useful when specific devices need to override the default
parameters set in the Docker App definition. The Docker App parameters listed in
this section are managed, in the sense that each parameters is defined and given
a default value in the Docker App definition.

Consider the Docker App example above. Lets say we would like to set the ``MSG``
parameter without changing the Docker App definition, we can override the default
value using a parameters file.

On the device, create a ``params.yml`` at a writeable location.

``sudo vim /var/sota/params.yml``

Now add the parameter override using this yaml format.

.. code-block:: yaml

MSG: Hello New Message

Save the file, and add a reference to this parameter file in our ``sota.toml``.

.. note:: Running ``aktualizr-lite`` in daemon mode (default) will allow the system to detect changes to your ``sota.toml`` and ``params.yml``. Meaning that if these files are changed, and the ``aktualizr-lite`` daemon is restarted, it will detect new changes and evaluate the system to ensure the Docker Apps are running with the latest configuration. This feature is helpful to add/remove or update Docker Apps running on your device.

If you are running ``aktualizr-lite`` in daemon mode (default) you must stop it
first before editing the configuration.

``sudo systemctl stop aktualizr-lite``

``sudo vim /var/sota/sota.toml``

Add the following line to the ``[pacman]`` block of your ``sota.toml``

``docker_app_params = "/var/sota/params.yml"``

Then restart the ``aktualizr-lite`` daemon to update the parameters passed to ``shellhttpd``.

What’s Missing?
---------------

The big thing missing here is remote management of device specific configuration.
The ``docker_apps_params`` setting above helps manage some configuration needs,
but it doesn’t automate things.

Why Not The Base Image?
-----------------------

A case can be made that the docker containers should just go into the OSTree
image and then you don’t have to deal with this approach. In some cases this
works fine. However, there are some advantages to our approach including:

 * allowing devices to be configured for specific docker-apps (a heterogeneous fleet)
 * a container-only update doesn’t require reboot
 * containers are quicker to build than the whole OS
