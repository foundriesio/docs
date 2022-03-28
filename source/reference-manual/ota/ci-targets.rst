.. _ref-ci-targets:

CI Targets
==========

The point of the Factory is to create Targets. The magic of the
Factory is how a ``git push`` can make this all happen. Because
of how easy these are to create, there is another type of Target,
:ref:`Production Targets <ref-production-targets>`, that are intended
to be used for production devices. However, it's almost always
originally created by CI when:

 * A change is pushed to source.foundries.io
 * A CI job is triggered in ci.foundries.io
 * The CI job signs the resulting TUF ``targets.json`` with the Factory's
   "online" targets signing key.

The online targets signing key ID can be seen in the TUF root
metadata:

.. code-block:: bash

  $ fioctl get https://api.foundries.io/ota/repo/<FACTORY>/api/v1/user_repo/root.json \
  | jq '.signed.roles.targets.keyids[0]'

Due to the number of changes and development branches a typical
customer may have, the TUF targets metadata can grow to include large
numbers of Targets. There are two ways these are dealt with:

 * Condensed Targets
 * Target Pruning

Condensed Targets
-----------------

Each device is configured to take updates for Targets that include
a specific tag. Because of this, the most of the Targets in the
CI ``targets.json`` aren't relevant and can be ignored by the device.
In order to provide smaller TUF metadata payloads, the Foundries
back-end employs a trick referred to as "condensed targets".

Condensed Targets are produced by taking the raw CI version and then
producing condensed versions for each unique tag. For example, the
raw targets.json might include::

  version=1, tag=master
  version=2, tag=devel
  version=3, tag=devel
  version=4, tag=devel,experimental

The back-end will actually produce three different condensed versions
that are each signed with the Factory's online targets signing key::

  # targets-master.json
  version=1, tag=master

  # targets-devel.json
  version=2, tag=devel
  version=3, tag=devel

  # targets-experimental.json
  version=3, tag=experimexperimental
  version=4, tag=experimental

The :ref:`device gateway <ref-ota-architecture>` is then able to serve
an optimized targets.json to each CI device.

Target Pruning
--------------

Each successful build appends a Target to targets.json. Eventually
it grows too large and users will see an error in CI::

  Publishing local TUF targets to the remote TUF repository
  == 2022-03-24 00:44:18 Running: garage-sign targets push --repo /root/tmp.gkfCEF
  |  An error occurred
  |  com.advancedtelematic.libtuf.http.CliHttpClient$CliHttpClientError: ReposerverHttpClient|PUT|http/413|https://api.foundries.io/ota/repo/andy-corp/api/v1/user_repo/targets%7C<html>
  |  <head><title>413 Request Entity Too Large</title></head>

When this happens, it's time to :ref:`prune targets <ref-troubleshooting_request-entity-too-large>`.
