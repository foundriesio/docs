Creating Your Factory
=====================
The Community Factory is provided by Foundries.io, and we define and maintain the content of the securable bootloader, Linux microPlatform image, and the Docker App Store. It allows you to download the public images and artifacts for a variety of common target boards, and will automatically update your device with updates to any of the components. However, if you would like to change any of these components, you will need to create a factory of your own.

A factory will allow you to tailor the software to a specific device, use-case, or product. They are privately hosted, so only members of your factory can access the source code, Docker registry, and CI system.

Below is a list of features a factory provides you.

Define your own Docker App Store
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Create your own containers, and :ref:`ref-docker-apps`. A build system is provided to build and publish your images for multiple architectures, and allows you to deliver them incrementally to any devices registered with your factory.

Customize the Linux microPlatform
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You are in control the of Linux microPlatform in your factory. Choose a different Linux kernel version, add drivers, packages, or even create a new target. Any builds produced from your factory will be presented to registered devices, allowing you to manage these deployments using :ref:`ref-device-tags` at scale. 

Hardware Testing (Enterprise Edition Only)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Test images on your hardware before deploying them to a production environment. 

Get Started
~~~~~~~~~~~
Click the ``Next`` button below to read how to start a subscription and create your first factory.
