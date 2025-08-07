.. _ref-static-deltas:

OSTree Static Deltas
====================

OSTree is implemented as a `Content Addressable Storage`_ system inspired by Git.
Both systems organize their objects in a tree-based hierarchy.
The client's job is to work through these trees of objects and apply the correct changes.
While Git has `smart protocol`_, OSTree `does not`_.
This can lead to certain types of OTAs being really inefficient — the client will be requesting a large number of files via HTTP requests.

OSTree has a solution for this problem called static deltas.
OSTree can produce static deltas that are good balance between number of files to download and the size of each file.
For instance, a 1.5G OTA might be split up into about 38 files that are each about 30Mb.

Generating Static Deltas
------------------------

Fioctl includes a command to help generate static deltas.
Since these deltas can sometimes require a bit of processing power and network bandwidth, the actual work is performed as CI Job in the Factory.

Understanding Why Static Deltas are Needed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An operator will be planning an update to a new Target.
This Target will have been produced by CI and already have a tag that was used by CI devices.
For example, the ``targets.json`` might include:

.. code-block::

  "raspberrypi4-64-lmp-9": {
    "custom" : {
      "version": "9",
      "tags" : ["main"],
   ...

In this example, Target #9 has passed CI and needs to be deployed to devices following the ``promoted`` tag.
The operator can determine what static deltas are needed by running:

.. code-block:: console

    $ fioctl targets static-deltas --dryrun --by-tag promoted 9
    Dry run: Would generated static deltas for target versions:
    7 -> 9
    5 -> 9

In this case, Fioctl has looked at all the devices configured to the ``promoted`` tag, and found the Target versions #5 and #7.
To produce the most efficient OTAs, two static deltas need to be created.

Creating Static Deltas
~~~~~~~~~~~~~~~~~~~~~~
Running the same command without ``--dryrun`` will produce the static deltas via a CI Job:

.. code-block:: console

   $ fioctl targets static-deltas --by-tag promoted 9

Once the static deltas are in place, Target #9 can be re-tagged so that "promoted" devices will apply the update:

.. code-block:: console

   $ fioctl targets tag --tags main,promoted --by-version 9

When the CI job completes, devices on the promoted tag will start performing OTA updates that will use the static deltas.

.. _Content Addressable Storage:
   https://en.wikipedia.org/wiki/Content-addressable_storage
.. _smart protocol:
   https://git-scm.com/book/en/v2/Git-Internals-Transfer-Protocols
.. _does not:
   https://ostreedev.github.io/ostree/formats/#on-the-topic-of-smart-servers
.. _static deltas:
   https://ostreedev.github.io/ostree/formats/#static-deltas
