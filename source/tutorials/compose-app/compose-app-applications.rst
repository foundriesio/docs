Applications
^^^^^^^^^^^^

This tutorial will now guide you through examples of three Docker Compose Apps.
The ``containers.git`` repo will then have three different application folders:

* ``shellhttpd-mqtt``: Based on ``shellhttpd``.
  This app counts the number of requests and sends them over the Message Queuing Telemetry Tranport (MQTT) network messaging protocol.

* ``flask-mqtt-nginx``: A python3 Flask app that implements a web app and receives the MQTT messages from ``shellhttpd-mqtt``.
  The Nginx reverse proxy forwards all the requests to the Flask application.

* ``mosquitto``: Enables the MQTT communication between ``shellhttpd-mqtt`` and ``flask-mqtt`` as an MQTT broker.

``shellhttpd-mqtt`` and ``mosquitto`` are examples of Docker Compose Apps using a single Docker container image.

``flask-mqtt-nginx`` is an example of Docker Compose Apps using multiple Docker container images.
In this case, ``flask-mqtt`` and ``nginx``.
