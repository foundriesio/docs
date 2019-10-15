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

How To Enable?
--------------

Assuming you have a targets.json with Docker Apps and your version of
aktualizr/aktualizr-lite includes support, then you simply configure your
``/var/sota/sota.toml`` with::

 [pacman]
 # type is usually "ostree", this enables the feature
 type = "ostree+docker-app"

 # configure which docker-apps you want your device to install
 docker_apps = "httpd"
 # where to store the docker-compose "project" directories:
 docker_apps_root = "/var/sota/docker-apps"

 #override the location of the docker-app binary with:
 #docker_app_bin = "/var/sota/docker-app"

 #set device specific parameters used by docker-app. An example:
 # https://github.com/docker/app/blob/master/examples/voting-app/example-parameters/my-environment.yml
 #docker_app_params = "/var/sota/params.yml"

Your next OTA update will include docker-apps.  However, you can force the
current update to include docker-apps by running the following::

  # stop aktualizr-lite
  sudo systemctl stop aktualizr-lite
  # run a manual update
  sudo aktualizr-lite update
  # start aktualizr-lite
  sudo systemctl start aktualizr-lite

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
