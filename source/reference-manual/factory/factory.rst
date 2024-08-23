.. _ref-factory:

FoundriesFactory
================

**FoundriesFactory™ Platform**: The set of tools, services, and support that enable a :term:`Factory` and assist it throughout the device lifecycle.
This section provides support for working with and customizing FoundriesFactory and the LmP.

* Topics that deal with how CI functions include :ref:`ref-factory-definition` and :ref:`ref-ci-webhooks`.

* :ref:`ref-fioctl` provides a helpful CLI tool for :ref:`ref-api-access`,
  while using :ref:`event queues<ref-event-queues>` helps with managing a large number of devices.

Each Factory has a set of git repositories used for customizing the LmP platform, defining container and Docker Compose apps, and managing CI build jobs.
These repositories are explored under :ref:`ref-factory-sources`.

For compliance concerns, there is an overview of the FoundriesFactory :ref:`ref-data-retention` policies, which covers customer (Factory) data and device data.
The FoundriesFactory :ref:`sbom` (SBOM) feature can assist with for license compliance.

.. toctree::
   :maxdepth: 1

   Factory Sources <factory-sources.rst>
   factory-definition
   Fioctl <fioctl/index.rst>
   sboms
   api-access
   ci-webhooks
   event-queues
   data-retention

.. seealso::
   :ref:`account-management` covers managing a FoundriesFactory subscription and access control settings.
   
   :ref:`lmp-customization` explores ways of customizing the LmP platform.
