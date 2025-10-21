Choosing Your CI Solution
=========================

FoundriesFactories supports two different modes for building Targets.

FoundriesFactory Managed
------------------------

Every Factory includes a ``containers.git`` hosted at ``source.foundries.io``.
This works out of the box and changes pushed here will be built automatically by our CI system and produce Targets that can be deployed to your device(s).

To get started with the Foundries.io managed solution you will need to:

- :ref:`Install Fioctl <gs-install-fioctl>` in order to work with ``source.foundries.io``.
- :ref:`Build and deploy <gs-building-deploying-app>` your first application.

Self-Hosted
-----------

The self-hosted option works well for people wanting more control of their workflows.
It works great with products like GitHub.
There is a one-time setup that takes about 30 minutes.

To get started with the self-hosted option, follow the steps outlined in the :ref:`Custom CI <ug-custom-ci-for-apps>` guide.
