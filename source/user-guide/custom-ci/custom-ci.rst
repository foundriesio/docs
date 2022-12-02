.. _ug-custom-ci:

Custom CI
=========

FoundriesFactory is like a Swiss Army knife that includes everything you need to manage the lifecycle of
a Linux-based operating system and the containerized applications running on it. In particular, it includes:

1. Git repositories for your operating system (OE layers/recipes) and containerized applications.
2. The CI service to build your operating system and containerized applications.
3. The TUF compliant OTA service to securely update the OS and the Apps on your devices.
4. Utilities to configure and manage the aforementioned services.

While it all works together like a charm, in some cases you may wanna use just some subsets of the provided services.
In particular, you may want to build OS and applications by yourself and still use the FoundriesFactory OTA service.
The following two guides walk you through the steps to accomplish it.

The :ref:`ug-custom-ci-for-rootfs` guide outlines steps to build an LmP-based OS image outside of the FoundriesFactory CI service
and how to use the OTA service to update the OS on devices.

The :ref:`ug-custom-ci-for-apps` guide provides an example of building containerized applications in a GitHub workflow along with
the OTA service usage to update applications on devices.

.. toctree::
   :maxdepth: 1

   custom-ci-for-rootfs
   custom-ci-for-apps
