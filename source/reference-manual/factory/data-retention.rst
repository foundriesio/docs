.. _ref-data-retention:

Data Retention Policies
=======================

Users often need to understand data retention policies within a FoundriesFactory so that they can work through compliance processes for their product.
This page explains how data is managed within a Factory.
FoundriesFactory consists of several free-standing projects that are tightly integrated with each other:

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

These services can be grouped into two areas of concern: customer data and device data.

Customer Data
-------------

source.foundries.io
~~~~~~~~~~~~~~~~~~~
User source code like ``containers.git`` lives in Digital Ocean's SFO2 data center.
This data is periodically backed up within this data center.
Backups over 6 months old are pruned.
All customer source code is deleted when a Factory is deleted.

ci.foundries.io
~~~~~~~~~~~~~~~
ci.foundries.io runs inside Google's GCP us-central1-a region.
It stores data in two places:

 * Galera Cluster Database
 * Google Storage Bucket

The storage bucket is multi-regional in the United States.
The database is periodically backed up to Google Storage.
Backups over 6 months old are pruned.

CI Workers
~~~~~~~~~~
CI work takes place in ephemeral instances (Docker containers) that are removed upon the completion of a CI Run.
The exception to this is the `sstate cache`_ for LmP builds.
This is kept on an NFS drive in the customer's CI region.
This data is periodically pruned to remove old data and completely deleted when a Factory is deleted.

.. _sstate cache:
   https://wiki.yoctoproject.org/wiki/Enable_sstate_cache

api.foundries.io
~~~~~~~~~~~~~~~~
This service is a reverse proxy to other services and stores no data.

app.foundries.io
~~~~~~~~~~~~~~~~
This service has two components:

 * A web view to api.foundries.io
 * Factory user and subscription management

The service runs inside Google's GCP us-central1-a region.
The user and subscription database is backed up nightly to Google Storage.
Backups over 6 months old are pruned.

Device Data
-----------
Foundries.io does not store any other device application data beyond what is listed in this section.

hub.foundries.io
~~~~~~~~~~~~~~~~
User container images are managed by this service.
Devices pull container updates from this service.
All data is stored in a multi-regional Google Storage Bucket in the United States.
It is deleted when a Factory is deleted.

ota-lite.foundries.io
~~~~~~~~~~~~~~~~~~~~~
This service manages two pieces of data:

 * The Factory's TUF Metadata
 * Device data

Device data includes things such as:

 * Hardware information from the lshw_ tool.
 * Details of the last 10 OTAs (``fioctl updates show``)
 * When the device was created
 * The Factory user that created the device
 * The device's local IPv4 address. *Depends on deployment details, this is normally a class C IP Address and not the public IPv4 address it accesses the Internet from*
 * The device's MAC address

The service and data is inside Google's GCP us-central1-a region.
The data is periodically backed up to Google Storage.
Backups over 6 months old are pruned.

.. _lshw:
   https://ezix.org/project/wiki/HardwareLiSter

ostree.foundries.io
~~~~~~~~~~~~~~~~~~~
Devices pull LmP updates down from this service.
It is managed in a similar way to hub.foundries.io.
