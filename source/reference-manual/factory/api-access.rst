.. _ref-api-access:

API Access
==========

FoundriesFactory APIs can be accessed with two different methods:

 #. OAuth2_ tokens managed in the `Application Credentials`_ interface.
 #. API Tokens managed in the `API tokens`_ interface.

These credentials allow users to access:

 * `REST APIs`_

   * Using the HTTP header ``OSF-TOKEN: <token>``.
   * Using an OAuth2 bearer token ``Authorization: Bearer <access-token>``
 * `Git repositories`_. Access is granted by passing an API token as the
   password to Git clone and fetch operations.
 * `Factory containers`_. Access is granted by passing an API token as the
   password to ``docker login hub.foundries.io``.
 * Fioctl uses OAuth2 by default, but can also use API Tokens.

All tokens are created with scopes to help limit what they can do.

Common scopes
-------------

Some common scopes users may find handy include:

 * ``source:read-update`` - Useful for Git.
 * ``targets:read, devices:read, ci:read`` - read-only access
   for fioctl or REST API
 * ``targets:read-update, devices:read-update, ci:read`` - read-update
   access for fioctl.
 * ``containers:read`` - Useful for running docker commands on
   factory containers.

.. _ref-scopes:

Token Scopes
------------

Scopes define what resources a given token may perform operations on. The
following scopes are supported:

source:read
 Can perform git clone/fetch/pull operations.
source:read-update
 Can perform git push operations.
source:delete
 Can delete a reference (git push --delete ...) and force-push (git push -f).
source:create
 Can create a new references (tags and branches).

containers:read
  Can docker pull.
containers:read-update
 Can docker push.

ci:read
 Can access CI builds `https://api.foundries.io/projects/<factory>/lmp/`.
ci:read-update
 This isn’t needed normally because ``source:read-update`` triggers CI.
 However, certain custom use-cases that trigger CI builds via
 `https://api.foundries.io/projects/<factory>/lmp/builds/` can use this.

devices:read
 Can view device(s) `https://api.foundries.io/ota/devices/`.
devices:read-update
 Can update configuration on a device
 `https://api.foundries.io/ota/devices/<device>/config/`
devices:create
 Can create a device (lmp-device-register with an API token).
devices:delete
 Can delete a device `https://api.foundries.io/ota/devices/<device>/`

targets:read
  Can view targets.json `https://api.foundries.io/ota/factories/<factory>/targets/`.
targets:read-update
  Can update targets.json `https://api.foundries.io/ota/factories/<factory>/targets/`.

.. _API Tokens:
   https://app.foundries.io/settings/tokens/

.. _Application credentials:
   https://app.foundries.io/settings/credentials/

.. _REST APIs:
   https://api.foundries.io/ota/

.. _Git repositories:
   https://source.foundries.io/

.. _Factory containers:
   https://hub.foundries.io/

.. _OAuth2:
   https://oauth.net/2/
