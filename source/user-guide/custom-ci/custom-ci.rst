.. _ug-custom-ci:

Custom CI
=========

FoundriesFactory® is a Swiss Army knife.
It includes everything you need to manage the lifecycle of a Linux®-based OS with containerized applications running on it:

   - Git repositories for your operating system (OE layers/recipes) and containerized applications.
   - The CI service to build your operating system and containerized applications.
   - The TUF compliant OTA service to securely update the OS and the Apps on your devices.
   - Utilities to configure and manage the aforementioned services.

While it all works together like a charm, in some cases you may want to use only a subset of the services.
In particular, you may want to build the OS and applications yourself, while still using the FoundriesFactory OTA service.
The following guides walk you through the steps to accomplish this.

:ref:`ug-custom-ci-for-rootfs` outlines building an LmP image outside of the FoundriesFactory CI service,
and how to use the OTA service to update the OS.

:ref:`ug-custom-ci-for-apps` provides an example of building containerized Apps in a GitHub workflow,
along with the OTA service usage to update Apps on devices.

.. toctree::
   :maxdepth: 1

   custom-ci-for-rootfs
   custom-ci-for-apps

