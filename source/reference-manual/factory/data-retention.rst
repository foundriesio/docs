.. _ref-data-retention:

Data Retention Policies
=======================

Understanding data retention policies within a FoundriesFactory can help with the compliance processes for a product.
This page explains how data is managed within a Factory.
FoundriesFactory consists of several tightly integrated projects:

======================   ================== =================================
**Service**              **Description**     **Location**
----------------------   ------------------ ---------------------------------
source.foundries.io      Git                 Digital - Ocean SFO2 DC
ci.foundries.io          CI server           GCP - us-central1-a
Ephemeral CI workers     CI                  AWS us-east-2, online.net France
api.foundries.io         User-facing APIs    GCP - us-central1-a
app.foundries.io         Web UI              GCP - us-central1-a
hub.foundries.io         Docker registry     GCP - us-central1-a
ota-lite.foundries.io    Device gateway      GCP - us-central1-a
ostree.foundries.io      OSTree for devices  GCP - us-central1-a
======================   ================== =================================

These services fall under two areas of concern: customer data and device data.

Customer Data
-------------

source.foundries.io
~~~~~~~~~~~~~~~~~~~
Source code like ``containers.git`` lives in Digital Ocean's SFO2 data center where it is periodically backed up.
Backups —but not the source itself— older than 6 months get pruned.
Source code gets deleted when a Factory is deleted.

ci.foundries.io
~~~~~~~~~~~~~~~
``ci.foundries.io`` runs inside Google's GCP us-central1-a region.
It stores data in two places:

 * Galera Cluster Database
 * Google Storage Bucket

The storage bucket is multi-regional and is within the United States.
The database gets periodically backed up to Google Storage.
Backups over 6 months old get pruned.

CI Workers
~~~~~~~~~~
CI work takes place in ephemeral instances (Docker containers) that are removed upon the completion of a CI Run.
The exception being `sstate cache`_ for LmP builds.
This is kept on an NFS drive in the customer's CI region.
This data get pruned periodically, and gets deleted when a Factory is deleted.

.. _sstate cache:
   https://wiki.yoctoproject.org/wiki/Enable_sstate_cache

api.foundries.io
~~~~~~~~~~~~~~~~
A reverse proxy to other services, and stores no data.

app.foundries.io
~~~~~~~~~~~~~~~~
This service has two components:

 * A web view to ``api.foundries.io``
 * Factory user and subscription management

Both run inside Google's GCP us-central1-a region.
The user and subscription database is backed up nightly to Google Storage.
Backups over 6 months old get pruned.

Device Data
-----------
Foundries.io does not store any other device application data beyond what is listed in this section.

hub.foundries.io
~~~~~~~~~~~~~~~~
Container images are managed by this service.
Devices pull container updates from this service.
Data gets stored in a multi-regional Google Storage Bucket within the United States and gets deleted when a Factory gets deleted.

ota-lite.foundries.io
~~~~~~~~~~~~~~~~~~~~~
This service manages two pieces of data:

 * A Factory's TUF Metadata
 * Device data

Device data covers:

 * Hardware information from the lshw_ tool.
 * Details of the last 10 OTAs (``fioctl updates show``)
 * The date when device was added
 * The Factory member that added the device
 * The device's MAC address
 * The device's local IPv4 address.

.. note::
 The  device's address depends on deployment details.
 This normally a class C IP Address, not the public IPv4 address it accesses the Internet from

Both service and data gets kept inside Google's GCP us-central1-a region.
The data is periodically backed up to Google Storage.
Backups over 6 months old get pruned.

.. _lshw:
   https://ezix.org/project/wiki/HardwareLiSter

ostree.foundries.io
~~~~~~~~~~~~~~~~~~~
Devices pull LmP updates down from this service.
It is managed in a similar way to hub.foundries.io.
