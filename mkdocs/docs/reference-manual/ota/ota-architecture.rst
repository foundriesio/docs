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

How A Device Finds Updates
~~~~~~~~~~~~~~~~~~~~~~~~~~

Aktualizr-lite uses `TUF`_ to find and validate available Targets that
a device may install. Aktualizr-lite will periodically check-in using
this high level logic:

 * Ask if a new root.json exists. This allows a device to know about
   key rotations before going further. This call is almost always going
   to result in an HTTP 404 response.

 * Ask for the timestamp.json metadata. If this file hasn't changed,
   there's no need to ask for more metadata - nothing has changed.

 * Ask for the snapshot.json metadata. If this file hasn't changed,
   there's no need to ask for more metadata - the targets have
   not changed.

 * Ask for the targets.json metadata. At this point the device can
   see if a new Target is available for installation.

.. _mutual TLS:
   https://codeburst.io/mutual-tls-authentication-mtls-de-mystified-11fa2a52e9cf

.. _TUF:
   https://theupdateframework.com/
