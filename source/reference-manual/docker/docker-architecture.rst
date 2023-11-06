.. highlight:: sh

.. _ref-docker-architecture:

Architecture Overview
=====================

LmP—via aktualizr-lite—runs Docker Compose projects as defined in a device's active Target.
:ref:`ref-compose-apps` were created as a way for a Factory to distribute the contents of a compose project.
A good way to understand how things fit together is by starting with what a typical Target looks like:

.. code-block:: YAML

  "intel-corei7-64-lmp-101" : {
    "hashes" : {
      "sha256" : "cb681331941af5cf688b7bf5d362b67a2583fde3f844898fad9bad05c61a2b04"
    },
    "custom" : {
      "docker_compose_apps" : {
        "fiotest" : {
          "uri" : "hub.foundries.io/andy-corp/fiotest@sha256:deadbeef"
        },
        "shellhttpd" : {
          "uri" : "hub.foundries.io/andy-corp/shellhttpd@sha256:f00"
        }
      }
    ...

This Target includes two compose apps, ``fiotest`` and ``shellhttpd``. 
These apps are coming from the Factory's containers.git repository.
The apps have a "pinned" URL which includes the sha256 checksum of its content.

The container build process pins each to an immutable sha256 Docker reference.
This is done to guarantee that the compose definition can not change over time.
The app is then uploaded to the ``hub.foundries.io`` Docker registry as an immutable tarball.

During the installation of a Target, aktualizr-lite extracts each tarball into its own directory, ``/var/sota/compose-apps/<app>``.
Running the compose app is then a matter of aktualizr-lite launching the compose app.
