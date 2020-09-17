.. highlight:: sh

.. _ref-ota-architecture:

Architecture Overview
=====================

At a high level the system consists of three entities:

 * LmP Devices
   - running aktualizr-lite and fioconfig

 * The device gateway

 * The Rest API
   - tooling like fioctl and app.foundries.io use

  .. figure:: /_static/ota-arch.png
     :align: center
     :scale: 70 %
     :alt: OTA architecture diagram

Devices talk to the device gateway using `mutual TLS`_. The device gateway
provides a set of REST APIs to support
:ref:`aktualizr-lite <ref-aktualizr-lite>`,
:ref:`fioconfig <ref-fioconfig>`,
:ref:`device testing <ref-fiotest>`, and Docker authentication. Aktualizr-lite
and fioconfig run as separate daemons that are periodically polling the
device gateway with HTTP GET requests on configurable intervals.

Due to the fact devices are polling the server, REST API changes requested by
tooling like fioctl happen asynchronously.

.. _mutual TLS:
   https://codeburst.io/mutual-tls-authentication-mtls-de-mystified-11fa2a52e9cf
