.. highlight:: sh

.. _ref-docker-architecture:

Architecture Overview
=====================

The LmP/aktualizr-lite is capable of running Docker Compose projects
that are defined in a device's active Target. The Factory needs a way
to distribute the contents of a compose project, so :ref:`ref-compose-apps`
were created. A good way to visualize how things fit together is
by starting with what a typical Target looks like::

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

This Target includes 2 compose apps, ``fiotest`` and ``shellhttpd`` that
will come from a Factory's containers.git repository. The apps have
a "pinned" URL that includes the sha256 checksum of its content.

The container build process will pin each container defined in the
compose file to an immutable sha256 Docker reference to make sure
the compose definition can't change over time. The app is then
uploaded to the hub.foundries.io Docker registry as a immutable
tarball.

Aktualizr-lite extracts each compose app's tarball into its own
directory, ``/var/sota/compose-apps/<app>``, during the installation
of a Target. Running the compose app is then a simple matter of
aktualizr-lite launching the compose app.
