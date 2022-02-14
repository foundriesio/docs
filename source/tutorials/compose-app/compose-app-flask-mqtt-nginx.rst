Flask-MQTT-nginx
^^^^^^^^^^^^^^^^

The ``flask-mqtt-nginx`` is a multiple containers application where more than one container is 
specified in the same ``docker-compose.yml`` file. There are innumerable reasons why to 
specify two or more containers in the same Docker Compose App, one of the reasons 
is dependencies. 

If one container depends on another to start-up, you have to use the same 
``docker-compose.yml`` file to specify and launch both containers.

The stanza ``depends_on`` will specify what service it’s depending on.

``flask-mqtt-nginx`` application is a typical python3 Flask application together with nginx.

In the containers folder, use git to download the ``flask-mqtt-nginx`` folder 
from the reference extra-container repository:

.. prompt:: bash host:~$, auto

    host:~$ git checkout remotes/fio/tutorials -- flask-mqtt-nginx

The ``flask-mqtt-nginx`` application should be inside your containers folder:

.. prompt:: bash host:~$, auto

    host:~$ tree -L 2 .

Example output:

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

Check the content of your ``flask-mqtt-nginx/docker-compose.yml`` file:

.. prompt:: bash host:~$, auto

    host:~$ cat flask-mqtt-nginx/docker-compose.yml

**flask-mqtt-nginx/docker-compose.yml**:

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

The ``flask-mqtt-nginx/docker-compose.yml`` file has all the configuration for the 
``flask-mqtt-nginx`` Docker Compose Application.

Where: 

- ``flask-mqtt``: Name of the first service.
- ``image``: Specifies the Docker Container Image from ``hub.foundries.io/${FACTORY}/flask-mqtt:latest``. Which is the Container Image created by the FoundriesFactory CI based on the Dockerfile in the ``flask-mqtt`` folder. Which will be downloaded in a moment.
- ``extra_hosts``: Map the container to access the device localhost over the address ``host.docker.internal``.
- ``nginx``: Name of the second service.
- ``image``:  Specifies the Docker Container Image ``nginx:alpine`` from ``hub.docker.com``.
- ``depends_on``: Make sure that the ``nginx`` service start-up after the ``flask-mqtt`` service.
- ``volume``: replace the default ``/etc/nginx/conf.d/default.conf`` configuration file inside the Docker Container Image with the nginx.conf file in the ``flask-mqtt-nginx`` folder.

In the containers folder, use git to download the ``flask-mqtt`` folder from the 
reference extra-container repository:

.. prompt:: bash host:~$, auto

    host:~$ git checkout remotes/fio/tutorials -- flask-mqtt

The ``flask-mqtt`` application should be inside your containers folder:

.. prompt:: bash host:~$, auto

    host:~$ tree -L 2 .

Example output:

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

**flask-mqtt/Dockerfile**:

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

The Dockerfile starts by creating a layer from the latest 
`Alpine Docker image <https://hub.docker.com/_/alpine>`_.

Next, it installs ``pip``, ``py3-flask`` and ``Flask-MQTT``.

Then, it sets environment variables for the Flask Application, adds ``apps.py`` file 
from your Docker client’s current directory to your Docker Container Image 
and configures the command to execute python3 with flask parameters.

Check the content of your ``flask-mqtt/app.py`` file:

.. prompt:: bash host:~$, auto

    host:~$ cat flask-mqtt/app.py

**flask-mqtt/app.py**:

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

The ``app.py`` is a  typical python3 Flask application. Unlike most  
getting started with flask examples, instead of returning a  ``Hello World``, 
it will return the ``Number of Access`` on ``shellhttpd`` container.

It also implements MQTT communication and subscribed to the topic ``containers/requests``.

As it receives messages starting with ``ACCESS=`` it parses and gets the value 
in the access variable.
