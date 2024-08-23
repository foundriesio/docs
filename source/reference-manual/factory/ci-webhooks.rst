.. _ref-ci-webhooks:

CI Webhooks
===========

By default, each Factory is configured to send :ref:`email notifications <def-notify>` when CI builds complete.
You also have the option of receiving *webhooks* when builds complete.
Webhooks provide a way to do things such as launching internal workflows.

Webhook data sent by the CI looks like::

  {
    "build_id": 67,
    "url": "https://api.foundries.io/projects/andy-corp/lmp/builds/67/",
    "status": "PASSED",
    "runs": [
    {
    "name": "build-amd64-partner",
    "url": "https://api.foundries.io/projects/andy-corp/lmp/builds/67/runs/build-amd64-partner/",
    "status": "PASSED",
    "log_url": "https://api.foundries.io/projects/andy-corp/lmp/builds/67/runs/build-amd64-partner/console.log",
    "web_url": "https://ci.foundries.io/projects/andy-corp/lmp/builds/67/build-amd64-partner/",
    "created": "2021-07-26T18:10:37+00:00",
    "completed": "2021-07-26T18:11:42+00:00",
    "host_tag": "amd64-partner",
    "tests": "https://api.foundries.io/projects/andy-corp/lmp/builds/67/runs/build-amd64-partner/tests/"
    },
    {
    "name": "build-aarch64",
    "url": "https://api.foundries.io/projects/andy-corp/lmp/builds/67/runs/build-aarch64/",
    "status": "PASSED",
    "log_url": "https://api.foundries.io/projects/andy-corp/lmp/builds/67/runs/build-aarch64/console.log",
    "web_url": "https://ci.foundries.io/projects/andy-corp/lmp/builds/67/build-aarch64/",
    "created": "2021-07-26T18:10:35+00:00",
    "completed": "2021-07-26T18:11:02+00:00",
    "host_tag": "aarch64",
    "tests": "https://api.foundries.io/projects/andy-corp/lmp/builds/67/runs/build-aarch64/tests/"
    },
    {
    "name": "publish-compose-apps",
    "url": "https://api.foundries.io/projects/andy-corp/lmp/builds/67/runs/publish-compose-apps/",
    "status": "PASSED",
    "log_url": "https://api.foundries.io/projects/andy-corp/lmp/builds/67/runs/publish-compose-apps/console.log",
    "web_url": "https://ci.foundries.io/projects/andy-corp/lmp/builds/67/publish-compose-apps/",
    "created": "2021-07-26T18:11:49+00:00",
    "completed": "2021-07-26T18:19:24+00:00",
    "host_tag": "amd64-partner"
    }
    ],
    "web_url": "https://ci.foundries.io/projects/andy-corp/lmp/builds/67",
    "trigger_name": "containers-devel",
    "created": "2021-07-26T18:10:33+00:00",
    "completed": "2021-07-26T18:19:24+00:00"
  }

This message includes an `HMAC-SHA256`_ HTTP header from the FoundriesFactory™ Platform `CI engine`_, ``X-JobServ-Sig`` to help authenticate the sender.

.. _HMAC-SHA256:
   https://en.wikipedia.org/wiki/HMAC
.. _CI engine:
   https://github.com/foundriesio/jobserv/blob/72935348e902cdf318cfee6ab00acccee1438a7c/jobserv/notify.py#L141-L146

Prerequisites
-------------

You will need a server with an HTTP(S) port exposed to the internet.
HTTPS is recommended, but the HMAC signing also helps prevent malicious 3rd parties from tampering with the message body.

.. note::
   `Ngrok`_ can be a useful tool for prototype work.

.. _Ngrok:
   https://ngrok.com/

Configuring Webhooks
--------------------

Define a webhook secret for HMAC signing::

  $ fioctl secrets update webhook-docs-example=UseSomethingGoodHere

This informs the FoundriesFactory backend about a new CI related secret.

Configuring the Factory
-----------------------

``factory-config.yml`` from ``ci-scripts.git`` will need something like:

.. code-block:: YAML

 notify:
   webhooks:
    - url: https://29171f519f0a.ngrok.io/webhook
      secret_name: webhook-docs-example

``secret_name`` ties things together so that the backend will use the correct key when signing the HTTP message.

Once this change is pushed, all builds will send webhooks to the configured server.

Example
-------

A Docker-compose based project has been written to help prototype.
This example uses Ngrok_ so that it can be tested behind firewalls.

.. note:: Ngrok changes URLs every time it restarts.
   This requires the ``factory-config.yml`` file to change as well.

Prepare the App
~~~~~~~~~~~~~~~

::

 $ git clone https://github.com/foundriesio/jobserv-webhook-example
 $ cd jobserv-webhook-example
 $ docker-compose build

Create the Secret
~~~~~~~~~~~~~~~~~

::

  # Set secret in backend:
  $ fioctl secrets update webhook-docs-example=UseSomethingGoodHere
  # Set secret for compose app:
  $ echo UseSomethingGoodHere > webhook-secret

Launch the App
~~~~~~~~~~~~~~

::

  $ docker-compose up

At this point, pay attention to the Docker-compose logs.
Ngrok will print a message like::

  ngrok-proxy_1  | t=2021-07-26T17:51:15+0000 lvl=info msg="started tunnel" obj=tunnels name=command_line addr=http://webhook:5000 url=https://29171f519f0a.ngrok.io

That tells the URL its proxying with. Take this URL and configure
the factory-config.yml's ``notify.webhooks[0].url`` value.

Push a Change
~~~~~~~~~~~~~

Go to a branch in ``containers.git``  such as ``devel`` if you have it, and push an empty change with::

  $ git commit --allow-empty -m "bump to test webhooks"

Wait for it to complete and the webhook to be delivered to the webhook app.
It will print the contents of the webhook data.
