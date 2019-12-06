Docker App Store
================

The Community Factory includes several examples of containers that can be
run on a device based on `Docker App`_.

shellhttpd
~~~~~~~~~~
This is a minimal container that runs a web server using bash and netcat.
Its useful for quick sanity checks of platform functionality.

x-kiosk
~~~~~~~
Runs the chromium browser inside a container and displays a website.

openthread-gateway
~~~~~~~~~~~~~~~~~~
This docker-app establishes the services needed to enable routing of OpenThread
traffic to your standard network. This includes DNS64, CoAP-HTTP proxy,
and NAT64 for IPv6->IPv4 traffic translation.

   .. note::

     This requires an OpenThread compatible NCP to be configured and installed
     on your machine.

k3s
~~~
This docker-app is a minimal installation of kubernetes using Rancher's `k3s`_.
Please refer to :ref:`additional details <docker-apps-k3s>` for running k3s inside lmp devices.

  .. note::

     Requires resources sufficient to run k3s and any additional services it
     may orchestrate.

  .. toctree::
   
     docker-apps-k3s

How to enable a Docker App
==========================

In order to enable a Docker App deployment you first need to configure aktualizr/aktualizr-lite. 

As the root user create a file ``/var/sota/sota.toml`` with the following contents::

 [pacman]
 docker_apps = "shellhttpd"

This example enables the ``shellhttpd`` docker-app. If you would like to enable multiple docker-apps you can simply create a list::

 docker_apps = "shellhttpd, x-kiosk"

Which will enable ``shellhttpd`` and ``x-kiosk``. 

Your next OTA update will include docker-apps.  However, you can force the current update to include docker-apps by running the following::

 # stop aktualizr-lite
 sudo systemctl stop aktualizr-lite
 # run a manual update
 sudo aktualizr-lite update
 # start aktualizr-lite
 sudo systemctl start aktualizr-lite

.. _Docker App:
   https://github.com/docker/app
.. _k3s:
   https://github.com/rancher/k3s
