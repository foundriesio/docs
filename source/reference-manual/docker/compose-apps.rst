.. _ref-compose-apps:

Compose Apps
============

Docker-compose Apps or "Compose Apps" are the recommended way for doing
application development in a Foundries Factory. Docker-compose has emerged
as a great way to develop applications. However, it doesn't specify how to
**distribute** applications. Compose apps fill in this gap for Factory devices.

Compose Apps in a Factory
-------------------------

Compose apps are automatically managed from containers.git by naming
convention. Any top-level directory containing a docker-compose.yml file
is distributed as compose apps. Here is a simplistic source layout::

  # containers.git
  httpd/
        docker-compose.yml
        nginx.conf

::

  # httpd/docker-compose.yml
  version: "3"
  services:
    web:
      image: nginx:alpine
      volumes:
        - ./nginx.conf:/etc/nginx/conf.d/default.conf


::

  # httpd/nginx.conf
  server {
    location / {
      return 200 'compose-apps';
    }
  }

When changes are made to containers.git, the factory will produce a new
Target that includes the updated ``httpd`` compose app::

  $ fioctl targets show 77

  ... <snip>

  COMPOSE APP  VERSION
  -----------  -------
  httpd        hub.foundries.io/<factory>/httpd@sha256:0bbfe1b8e166e45cff477a731c5797a1ec8724a99a49b8f94d7ff851f2076924

Compose Apps Distribution
-------------------------

Compose apps are distributed by taking advantage of Docker Registry
primitives. The httpd example above becomes a tarball stored
in hub.foundries.io::

  # httpd.tgz
  ./docker-compose.yml
  ./ngix.conf

The tarball is an exact copy of httpd's directory layout in containers.git
with one important exception: The publishing logic looks at each service
image in the compose file and will pin it to the correct sha256 checksum
at the time of publishing. For this example, ``nginx:alpine`` would
become something like ``nginx:sha256@deadbeef``. This ensures each version of
the compose app is immutable.

Aktualizr-lite then has logic to grab this content from the docker registry,
validate it cryptographically, and extract it locally so that docker-compose
can consume it.


How Does It Fit Together?
-------------------------

Changes to containers produce new TUF Targets that aktualizr-lite can
install. The intersting part of the Target in this case will be::

 {
  ...
  "signed": {
    "targets": {
      "raspberrypi3-64-lmp-144" : {
        "custom" : {
          "docker_compose_apps" : {
             "httpd" : {
                "uri" : "hub.foundries.io/<factory>/httpd@sha256:deadbeef"
             }
             ....

Examples
--------

Single container application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Many users can build their entire application as a single container. In
this scenario containers.git layout might look like::

  # simple-app/Dockerfile
  FROM alpine
  RUN apk --no-cache add python3
  COPY ./app.py /usr/local/bin
  CMD ["python3", "/usr/local/bin/app.py"]

::

  # simple-app/app.py
  import os, time
  while True:
      print(os.environ['FROM_COMPOSE'])
      time.sleep(60)

::

  # simple-app/docker-compose.yml
  version: "3"
  services:
    app:
      image: hub.foundries.io/<factory>/simple-app:latest
      environment:
        FROM_COMPOSE: "this came from docker-compose.yml"

::

  # simple-app/.composeappignores - There's no need to distribute the Dockerfile and app.py
  Dockerfile
  app.py

Each change to containers.git will produce a new compose app with contents::

  # simple-app.tgz
  ./docker-compose.yml

In this case ``hub.foundries.io/<factory>/simple-app:latest`` is pinned to
the exact container built during the change to containers.git. The CI logic
does this automatically for the user.

A Flask Web App
~~~~~~~~~~~~~~~

This example uses multiple containers to build a typical python3 Flask
application::

  # hello-world/Dockerfile
  FROM alpine
  RUN apk --no-cache add py3-flask
  ENV FLASK_APP=app.py
  ENV PYTHONPATH=/srv
  COPY ./app.py /srv/app.py
  CMD ["python3", "-m", "flask", "run"]

::

  # hello-world/app.py
  from flask import Flask
  app = Flask(__name__)

  @app.route('/')
  def hello_world():
      return 'Hello, World!'

::

  # hello-world-app/docker-compose.yml
  version: "3"
  services:
    app:
      image: hub.foundries.io/<factory>/hello-world:latest
    nginx:
      image: nginx:alpine
      volumes:
        - ./nginx.conf:/etc/nginx/conf.d/default.conf
      ports:
        - 80:80
      depends_on:
        - app

::

  # hello-world-app/nginx.conf
  server {
    location / {
        proxy_pass           http://app:5000/;
    }
  }

Changes to containers.git does a couple of interesting things here:

#. It will build and publish a version of the hello-world container. For
   this example, call it ``hub.foundries.io/<factory>/hello-world:GIT_SHORT_HASH``

#. A compose app will be published. The compose app will include the
   nginx.conf file and a "pinned" docker-compose.yml. In this case the
   containers will be pinned to:

   a. ``nginx:alpine`` - the sha256 checksum of nginx:alpine at the time
      this was built.

   b. ``hub.foundries.io/<factory>/hello-world`` - the sha256 checksum
      of ``GIT_SHORT_HASH`` at the time this was built.
