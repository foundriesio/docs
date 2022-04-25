.. _ref-event-queues:

Event Queues
============

The FoundriesFactory API_ exposes everything about a Factory. In fact,
app.foundries.io and fioctl_ are both built on top of that API. While
this API is fully functional, it can be hard for certain operators to
build their custom tooling for large numbers of devices if they
must constantly poll the API for information. Event queues were
designed to solve this issue.

Event queues provide a way for customers to receive messages about
important events that are not easy to poll for. These include:

 * The first time a device connects to the :ref:`device gateway <ref-ota-architecture>`.
 * When a device applies a configuration change.
 * When an OTA update starts and completes.

Event queues are implemented using Google PubSub_ to provide
a well understood and tested framework. There are two types
of event queues that can be created:

 * Push - Works as a webhook_ service. Events are sent
   to a managed URL where they can be processed.

 * Pull - Works like a typical message queue system where one
   can write their own client to receive and process events.

PubSub documentation includes a very useful guide_ to help decide
which approach will work best for you. They also include a wide
range of `client libraries`_ for consuming the Pull API. PubSub
subscriptions are created with default retention, expiration,
and acknowledgement values_.

Implementation Details
----------------------

Each FoundriesFactory is given a single PubSub Topic. Each Push
and Pull queue created by a customer results in the creation of
a PubSub Subscription. The FoundriesFactory API just provides a
thin, multi-tenant friendly wrapper to manage everything.

Creating a Pull Queue
---------------------
A pull queue can be created using fioctl::

 # fioctl event-queues mk-pull <name> <where to save creds-file>
 $ fioctl event-queues mk-pull docs-example $HOME/.fio-pull-queue.creds

Fioctl can also monitor this queue::

 $ fioctl event-queues listen docs-example $HOME/.fio-pull-queue.creds

This command also serves as a reference example_ of how to implement
a pull queue listener.

Creating a Push Queue
---------------------

A push queue requires a little up front work:

 * Having an internet facing server to run the webhook service.
 * Authenticating incoming requests.

Quick Start Example
~~~~~~~~~~~~~~~~~~~
A great way to prototype a push queue by using ngrok_. This tool allows
a service running on your laptop to be exposed via an ngrok reverse
proxy. With ngrok installed, you can play with the `example push queue`_
code from your laptop::

 # Start ngrok
 $ ngrok http 8080
 # make note of the "Forwarding                    https:..."
 # This URL is required for the JWT_AUDIENCE below

 # From another terminal:
 # Install required python dependencies:
 $ python3 -m venv /tmp/venv
 $ /tmp/venv/bin/pip3 install cryptography requests pyjwt
 $ JWT_AUDIENCE=<ngrok url> /tmp/venv/bin/python3 push_queue_example.py

Once the server is running, you can create a push queue with::

 $ fioctl event-queues mk-push docs-push <ngrok URL from above>

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
This JWT is signed with one of Google's own private keys. The
`public keys`_ are published online so that users can validate the
signatures.
The JWT audience header is set to the URL you specified when creating
the push queue. The `example push queue`_ includes logic for validating
this header.

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

.. _API:
   https://api.foundries.io/ota/

.. _fioctl:
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

.. _example push queue:
   ../../_static/push_queue_example.py

.. _public keys:
   https://www.googleapis.com/oauth2/v1/certs

.. _values:
   https://cloud.google.com/pubsub/docs/admin#properties_of_a_topic
