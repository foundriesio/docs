.. _ref-event-queues:

Event Queues
============

The FoundriesFactory® API_ exposes everything about a Factory.
In fact, ``app.foundries.io`` and Fioctl_ ® are both built on top of that API.
While this API is fully functional, it can be difficult to build custom tooling for a large numbers of devices if constantly polling the API.
Event queues were designed to solve this issue.

Event queues provide a way to receive messages about important events not easy polled for.
These include:

 * The first time a device connects to the :ref:`device gateway <ref-ota-architecture>`.
 * When a device applies a configuration change.
 * When an OTA update starts and completes.

Event queues are implemented using Google PubSub_ to provide a well understood and tested framework.
There are two types of event queues:

 * Push: Works as a webhook_ service.
   Events are sent to a managed URL where they can be processed.

 * Pull: Works like a typical message queue system where one can write their own client to receive and process events.

The PubSub documentation includes a very useful guide_ for deciding which approach will work best for you.
They also include a wide range of `client libraries`_ for consuming the Pull API.
PubSub subscriptions are created with default retention, expiration, and acknowledgement values_.

Implementation Details
----------------------

Each FoundriesFactory is given a single PubSub Topic.
Each Push and Pull queue created by a customer results in the creation of a PubSub subscription.
The FoundriesFactory API provides a thin, multi-tenant friendly wrapper to manage everything.

.. note::
   For performance reasons, new push queues can take up to five minutes before they start receiving events.

Creating a Pull Queue
---------------------
A pull queue can be created using Fioctl::

  fioctl event-queues mk-pull <name> <where to save creds-file>
  fioctl event-queues mk-pull docs-example $HOME/.fio-pull-queue.creds

Fioctl can also monitor this queue::

  fioctl event-queues listen docs-example $HOME/.fio-pull-queue.creds

This command also serves as a reference example_ on implementing a pull queue listener.

Creating a Push Queue
---------------------

A push queue requires a little up front work:

 * Having an internet facing server to run the webhook service.
 * Authenticating incoming requests.

Quick Start Example
~~~~~~~~~~~~~~~~~~~

A great way to prototype a push queue is by using ngrok_.
This tool allows a service running on your laptop to be exposed via an ngrok reverse proxy.
With ngrok installed, you can play with the :download:`example push queue <../../_static/push_queue_example.py>` code from your computer:

.. code-block:: bash

 # Start ngrok
 ngrok http 8080
 # make note of the "Forwarding https:..."
 # This URL is required for the JWT_AUDIENCE below

 # From another terminal:
 # Install required python dependencies:
 python3 -m venv /tmp/venv
 /tmp/venv/bin/pip3 install cryptography requests pyjwt
 JWT_AUDIENCE=<ngrok url> /tmp/venv/bin/python3 push_queue_example.py

Once the server is running, you can create a push queue with::

 fioctl event-queues mk-push docs-push <ngrok URL from above>

At this point events will start showing up in the example server.

Push Queue Payloads
~~~~~~~~~~~~~~~~~~~

Incoming HTTP requests will look similar to::

  {
   "message": {
     "attributes": {
       "event-type":"DEVICE_FIRST_SEEN"
     },
     "data":"aGVsbG9fd29ybGQ=",  # base64 encoded Event payload
     "messageId":"4292351872734735",
     "message_id":"4292351872734735",
     "publishTime":"2022-03-30T15:18:21.095Z",
     "publish_time":"2022-03-30T15:18:21.095Z"
   },
   "subscription":"projects/osf-prod/subscriptions/xxxxxxxx"
  }

Push Queue Security
~~~~~~~~~~~~~~~~~~~

Incoming requests will include a header, ``Authorization: Bearer <jwt>``.
This JWT is signed with one of Google's own private keys.
The `public keys`_ are published online so that users can validate the signatures.
The JWT audience header is set to the URL you specified when creating the push queue.
The :download:`example push queue<../../_static/push_queue_example.py>` includes logic for validating this header.

Event Types
-----------

DEVICE_FIRST_SEEN
~~~~~~~~~~~~~~~~~

::

 {
   "Uuid": <string: DEVICE_UUID>,
   "Time": <integer: unix seconds>
 }

DEVICE_CONFIG_APPLIED
~~~~~~~~~~~~~~~~~~~~~

::

 {
   "Uuid": <string: DEVICE_UUID>,
   "Time": <integer: unix seconds>
 }


DEVICE_OTA_STARTED
~~~~~~~~~~~~~~~~~~

::

 {
   "Uuid": <string: DEVICE_UUID>,
   "Time": <integer: unix seconds>,
   "Target": <string: target name>,
   "Id": <string: update correlation-id> # works with `fioctl devices updates show <id>`
 }

DEVICE_OTA_COMPLETED
~~~~~~~~~~~~~~~~~~~~

::

 {
   "Uuid": <string: DEVICE_UUID>,
   "Time": <integer: unix seconds>,
   "Target": <string: target name>,
   "Id": <string: update correlation-id>,
   "Success": <boolean>
 }

DEVICE_OTA_APPS_STATE_CHANGED
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

 {
   "Uuid": <string: DEVICE_UUID>,
   "Time": <integer: unix seconds>,
   "Ostree": <string: the device's OSTree commit hash>,
   "DeviceTime": <string: timestamp when an Apps state was captured on device, in RFC3339 format>,
   "Apps": {
        <app-name>: {
            "health": <string: `healthy` || `unhealthy`>,
            "uri": <string: a pinned App URI, optional>
            "services": [
                "name": <string: a service name as it is defined in an App's compose file>,
                "hash": <string: a service hash>,
                "state": <string: a service container state reported by Docker Engine>,
                "status": <string: a service container status reported by Docker Engine>,
                "health": <string: a service container health reported by Docker Engine or deduced from its state>,
                "image": <string: a pinned service image URI>,
                "logs": <string: last 5 lines of logs yielded by a service container, optional, present only if a container is unhealthy>
            ],
        }
        ...
   }
 }

DEVICE_PUBKEY_CHANGE
~~~~~~~~~~~~~~~~~~~~

::

 {
   "Uuid": <string: DEVICE_UUID>,
   "Time": <integer: unix seconds>,
   "NewPubKey": <string: New PEM encoded public key>,
   "OldPubKey": <string: Old PEM encoded public key>
 }

.. _API:
   https://api.foundries.io/ota/

.. _Fioctl:
   https://github.com/foundriesio/fioctl

.. _PubSub:
   https://cloud.google.com/pubsub/docs/overview

.. _webhook:
   https://en.wikipedia.org/wiki/Webhook

.. _guide:
   https://cloud.google.com/pubsub/docs/subscriber

.. _client libraries:
   https://cloud.google.com/pubsub/docs/publish-receive-messages-client-library

.. _example:
   https://github.com/foundriesio/fioctl/blob/main/subcommands/events/listen.go

.. _ngrok:
   https://ngrok.com/

.. _public keys:
   https://www.googleapis.com/oauth2/v1/certs

.. _values:
   https://cloud.google.com/pubsub/docs/create-topic#properties_of_a_topic
