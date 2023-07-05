Flask-MQTT-Nginx
^^^^^^^^^^^^^^^^

``flask-mqtt-nginx`` is a multi-container app,
with more than one container specified in the same ``docker-compose.yml`` file.
There are many reasons to specify multiple containers in the same Docker Compose App.
One is due to *dependencies*. 

If a container depends on another to start-up,
you must use the same ``docker-compose.yml`` file to specify and launch both.

The ``depends_on`` stanza specifies what service it is dependent on.

``flask-mqtt-nginx`` is a typical python3 Flask app, together with Nginx.

In the containers folder, use git to download  ``flask-mqtt-nginx`` from the ``extra-containers`` repo:

.. prompt:: bash host:~$, auto

    host:~$ git checkout remotes/fio/tutorials -- flask-mqtt-nginx

The ``flask-mqtt-nginx`` application should now be inside your containers folder:

.. prompt:: bash host:~$, auto

    host:~$ tree -L 2 .

.. prompt:: text

     .
     ├── flask-mqtt-nginx
     │   ├── docker-compose.yml
     │   └── nginx.conf
     ├── mosquitto
     │   └── docker-compose.yml
     ├── README.md
     ├── shellhttpd
     │   ├── docker-build.conf
     │   ├── docker-compose.yml
     │   ├── Dockerfile
     │   ├── httpd.sh
     │   └── shellhttpd.conf
     └── shellhttpd-mqtt
         ├── docker-compose.yml
         ├── Dockerfile
         └── httpd.sh

Check the content ``flask-mqtt-nginx/docker-compose.yml``:

.. prompt:: bash host:~$, auto

    host:~$ cat flask-mqtt-nginx/docker-compose.yml

.. prompt:: text

     version: "3"
     services:
       flask-mqtt:
         image: hub.foundries.io/${FACTORY}/flask-mqtt:latest
         restart: unless-stopped
         extra_hosts:
           - "host.docker.internal:host-gateway"
       nginx:
         image: nginx:alpine
         restart: unless-stopped
         volumes:
           - ./nginx.conf:/etc/nginx/conf.d/default.conf
         ports:
           - 80:80
         depends_on:
           - flask-mqtt

The ``flask-mqtt-nginx/docker-compose.yml`` file has the configuration for ``flask-mqtt-nginx``: 

- ``flask-mqtt``: Name of the first service.
- ``image``: Specifies the Docker container image from ``hub.foundries.io/${FACTORY}/flask-mqtt:latest``.
  This is the container image created by the FoundriesFactory CI based on the Dockerfile in the ``flask-mqtt`` folder—which will be downloaded in a moment.
- ``extra_hosts``: Maps the container to access the device ``localhost`` over the address ``host.docker.internal``.
- ``nginx``: Name of the second service.
- ``image``:  Specifies the Docker container image ``nginx:alpine`` from ``hub.docker.com``.
- ``depends_on``: Make sure that the ``nginx`` service starts up *after* the ``flask-mqtt`` service.
- ``volume``: replaces the Docker container image's default configuration file ``/etc/nginx/conf.d/default.conf`` with `nginx.conf` from the ``flask-mqtt-nginx`` folder.

In the containers folder, use git to download ``flask-mqtt`` from the ``extra-container`` repo:

.. prompt:: bash host:~$, auto

    host:~$ git checkout remotes/fio/tutorials -- flask-mqtt

The ``flask-mqtt`` application should be inside your containers folder:

.. prompt:: bash host:~$, auto

    host:~$ tree -L 2 .

.. prompt:: text

     .
     ├── flask-mqtt
     │   ├── app.py
     │   └── Dockerfile
     ├── flask-mqtt-nginx
     │   ├── docker-compose.yml
     │   └── nginx.conf
     ├── mosquitto
     │   └── docker-compose.yml
     ├── README.md
     ├── shellhttpd
     │   ├── docker-build.conf
     │   ├── docker-compose.yml
     │   ├── Dockerfile
     │   ├── httpd.sh
     │   └── shellhttpd.conf
     └── shellhttpd-mqtt
         ├── docker-compose.yml
         ├── Dockerfile
         └── httpd.sh

Check the content of your ``flask-mqtt/Dockerfile`` file:

.. prompt:: bash host:~$, auto

    host:~$ cat flask-mqtt/Dockerfile

.. prompt:: text

     # flask-mqtt/Dockerfile
     FROM alpine
     
     RUN apk add --update py-pip
     RUN apk --no-cache add py3-flask
     # install python3 dependencies in advance -- we can copy them later
     RUN pip install --no-cache --upgrade pip && \
         pip install --no-cache --upgrade Flask-MQTT
     
     ENV FLASK_APP=app.py
     ENV PYTHONPATH=/srv
     COPY ./app.py /srv/app.py
     CMD ["python3", "-m", "flask", "run", "-h", "0.0.0.0"]

The Dockerfile starts by creating a layer from the latest `Alpine Docker image <https://hub.docker.com/_/alpine>`_.

Next, ``pip``, ``py3-flask``, and ``Flask-MQTT`` are installed.

Then, environmental variables for the Flask Application are set.
``apps.py`` from your Docker client’s current directory is added to your Docker container Image.
The command to execute python3 with flask parameters is configured.

Check the content of ``flask-mqtt/app.py``:

.. prompt:: bash host:~$, auto

    host:~$ cat flask-mqtt/app.py

.. prompt:: text

     # flask-mqtt/app.py
     import time
     import sys
     
     from flask import Flask
     from flask_mqtt import Mqtt
     
     access = 0
     app = None
     mqtt = None
     
     def create_app():
       print("create_app")
       global app
       app = Flask(__name__)
     
       app.config['SECRET'] = 'my secret key'
       app.config['TEMPLATES_AUTO_RELOAD'] = True
       app.config['MQTT_BROKER_URL'] = 'host.docker.internal'
       app.config['MQTT_BROKER_PORT'] = 1883
       app.config['MQTT_USERNAME'] = ''
       app.config['MQTT_PASSWORD'] = ''
       app.config['MQTT_KEEPALIVE'] = 5
       app.config['MQTT_TLS_ENABLED'] = False
     
       global mqtt
       mqtt = init_mqtt(app)
     
     def init_mqtt(app):
       while True:
         try:
           print("init_mqtt: Connecting to MqTT Broker")
           return Mqtt(app)
         except:
           print("init_mqtt:", sys.exc_info()[0])
           time.sleep(10)
     
     create_app()
     
     @app.route('/')
     def hello_world():
       global access
       return ('Number of Access on shellhttpd Container ' + str(access))
     
     @mqtt.on_connect()
     def handle_connect(client, userdata, flags, rc):
         mqtt.subscribe('containers/requests')
     
     @mqtt.on_message()
     def handle_mqtt_message(client, userdata, message):
       if message.payload.decode().startswith('ACCESS='):
         value = message.payload.decode().split('=')
         if value[1].isnumeric():
           global access
           access = int(value[1])

``app.py`` is a typical python3 Flask application.
Unlike many "getting started with flask" examples which return ``Hello World``, 
it will return the ``Number of Access`` counter value from  ``shellhttpd``.

It also implements MQTT communication and subscribes to the topic ``containers/requests``.

As it receives messages starting with ``ACCESS=``, it parses and gets the value in the access variable.
