.. _ref-ci-targets:

CI Targets
==========

The point of a Factory is to create Targets.
A ``git push`` is all that is required to trigger a Target to be built.

There is another type of Target, :ref:`Production Targets <ref-production-targets>`, that are intended to be used for production devices.
However, it is almost always originally created by the CI when:

 * A change is pushed to ``source.foundries.io``
 * A CI job is triggered in ``ci.foundries.io``
 * The CI job signs the resulting TUF ``targets.json`` with the Factory's "online" Targets signing key.

The online Targets signing key ID can be seen in the TUF root metadata:

.. code-block:: bash

  $ fioctl get https://api.foundries.io/ota/repo/<FACTORY>/api/v1/user_repo/root.json \
  | jq '.signed.roles.targets.keyids[0]'

Due to all the changes and branches you may have, the TUF Targets metadata can grow to include a large number of Targets.
There are two ways this can be dealt with:

 * Condensed Targets
 * Target Pruning

.. _ref-condensed-targets:

Condensed Targets
-----------------

Each device is configured to take updates for Targets that include a specific tag.
Because of this, most of the Targets in ``targets.json`` are not relevant for any given device and can be ignored by it.
In order to provide smaller TUF metadata payloads, the backend employs what is referred to as "condensed Targets".

Condensed Targets are produced by taking the raw CI version, and then producing condensed versions for each unique tag.
For example, a raw ``targets.json`` might include::

  version=1, tag=master
  version=2, tag=devel
  version=3, tag=devel
  version=4, tag=devel,experimental

The back-end will actually produce three different condensed versions.
Each one is signed with the Factory's online Targets signing key::

  # targets-master.json
  version=1, tag=master

  # targets-devel.json
  version=2, tag=devel
  version=3, tag=devel

  # targets-experimental.json
  version=3, tag=experimental
  version=4, tag=experimental

The :ref:`device gateway <ref-ota-architecture>` is then able to serve an optimized ``targets.json`` to each CI device.

Target Pruning
--------------

Each successful build appends a Target to ``targets.json``.
Eventually it can grow too large, and you would see an error in CI::

  Publishing local TUF targets to the remote TUF repository
  == 2022-03-24 00:44:18 Running: garage-sign targets push --repo /root/tmp.gkfCEF
  |  An error occurred
  |  com.advancedtelematic.libtuf.http.CliHttpClient$CliHttpClientError: ReposerverHttpClient|PUT|http/413|https://api.foundries.io/ota/repo/andy-corp/api/v1/user_repo/targets%7C<html>
  |  <head><title>413 Request Entity Too Large</title></head>

When this happens, it is time to :ref:`prune targets <ref-troubleshooting_request-entity-too-large>`.
