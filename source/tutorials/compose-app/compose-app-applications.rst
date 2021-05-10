Applications
^^^^^^^^^^^^

This tutorial will guide you over three 
different Docker Compose Apps examples. In other words, ``containers.git`` will have three different folders:

``shellhttpd-mqtt``: Based on the previous ``shellhttpd``. This application counts the number of requests and sends them over MQTT.

``flask-mqtt-nginx``: A typical python3 Flask application implements a web application and receives the MQTT messages from the ``shellhttpd-mqtt`` app. The Nginx reverse proxy forwards all the requests to the Flask application.

``mosquitto``: To enable the MQTT communication between ``shellhttpd-mqtt`` and ``flask-mqtt``, the third container establishes an MQTT broker.

``shellhttpd-mqtt`` and ``mosquitto`` are examples of Docker Compose Apps using single Docker Container Image.

The ``flask-mqtt-nginx`` is an example of Docker Compose Apps using multiple Docker Container Images. In this case, 
``flask-mqtt`` and ``nginx``.