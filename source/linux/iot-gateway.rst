.. highlight:: sh

.. _iot-gateway:

IoT Gateway Containers
======================

This page describes how to use containerized reference applications to
enable IoT gateway functionality using the Linux microPlatform.

.. note::

   This page is a generic reference on what's available. For
   step-by-step instructions to set up complete systems, check out
   :ref:`iotfoundry-top`.

All you need to get started is a gateway device supported by the Linux
microPlatform, a computer, and an Internet connection.

Install the Linux microPlatform
-------------------------------

Follow the instructions in the Linux microPlatform
:ref:`linux-getting-started` guide to set up your target hardware.

Install Ansible
---------------

The easiest way to get started with containers on your device is by
installing Ansible on your workstation, and using Ansible playbooks
provided by Open Source Foundries.

Linux and macOS
~~~~~~~~~~~~~~~

`Install the latest Ansible release`_. (Our playbooks require more
recent versions of Ansible than some Linux distribution package
managers provide).

Windows
~~~~~~~

While Ansible isn't supported on Windows, you can run `Ubuntu in a
Docker container`_ and install Ansible on Ubuntu. Another alternative
(though not officially supported by Microsoft or Ansible) is to
install `Ansible in the Windows Subsystem for Linux`_.

Load Gateway Containers
-----------------------

Now to deploy some key containerized applications to your device.

Subscribers
~~~~~~~~~~~

Subscribers have access to the latest gateway-containers repository
via their namespace (``YOUR_NAMESPACE``) on `git.foundries.io`_:

.. code-block:: none

   https://git.foundries.io/subscriber/YOUR_NAMESPACE/microplatforms/linux/gateway-containers

Start with the top-level ``README.md`` file in that repository, and
move on to the containers which interest you.

Prebuilt container images are available in the gateway-containers
Container Registry:

.. code-block:: none

   https://git.foundries.io/subscriber/YOUR_NAMESPACE/microplatforms/linux/gateway-containers/container_registry

Open Source Foundries provides Ansible playbooks to deploy these
containers to your board; these are available in each subscriber's
gateway-ansible repository:

.. code-block:: none

   https://git.foundries.io/subscriber/YOUR_NAMESPACE/microplatforms/linux/gateway-ansible

.. warning::

   The playbooks refer by default to container images in the public
   `Open Source Foundries Docker Hub`_ repository, which are **up to
   six months older** than the subscriber versions.

   For instructions on how to use the latest subscriber images from
   your Container Registry, refer to the ``registry``,
   ``registry_user``, etc. variables and nearby comments in the
   playbook YAML files.

Public
~~~~~~

Check out the `gateway-containers GitHub repository`_, which contains
the latest public container build files, along with instructions for
how to get them running on your board. Prebuilt container images are
available from the `Open Source Foundries Docker Hub`_ organization.

Start with the top-level `README.md
<https://github.com/OpenSourceFoundries/gateway-containers/blob/master/README.md>`_,
and move on to the containers which interest you.

Open Source Foundries provides Ansible playbooks to deploy these
containers to your board; these are available in the `gateway-ansible
GitHub repository`_.

.. _iot-gateway-whitelist:

Whitelist Setup for IoT Gateway
-------------------------------

Instructions follow setting up a 6LoWPAN Bluetooth device whitelist.

.. note::

   Prior to starting this walk through, please power off any IoT
   devices in your area.

Enable the whitelist feature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable the whitelist, simply enable the whitelist function by modifying
the bluetooth_6lowpand.conf.  You'll want to set USE_WL to 1 and add a
WL=MAC_ADDRESS line for each device you wish to whitelist.

How to Find Devices for the Whitelist
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that the whitelist is enabled, you can find the beaconing devices
using the following command::

    sudo hcitool lescan

While leaving this command running, power on the IoT device
you wish to add to the whitelist. You should see an additional line
appear as each device is powered on.

The following is an example of the output from this command (``XXX``
may vary)::

  LE Scan ...
  D6:E7:D2:E8:6C:9F (unknown)
  D6:E7:D2:E8:6C:9F XXX IPSP node

Make a note of the "XXX IPSP node" Bluetooth addresses.

Disable the whitelist feature
+++++++++++++++++++++++++++++

To turn off the whitelist feature, set USE_WL to '0' in bluetooth_6lowpand.conf

.. _Ansible: https://www.ansible.com/

.. _Install the latest Ansible release: http://docs.ansible.com/ansible/latest/intro_installation.html

.. _Ubuntu in a Docker container: https://docs.docker.com/docker-for-windows/

.. _Ansible in the Windows Subsystem for Linux: http://docs.ansible.com/ansible/latest/intro_windows.html

.. _git.foundries.io: https://git.foundries.io

.. _gateway-containers GitHub repository: https://github.com/OpenSourceFoundries/gateway-containers

.. _Open Source Foundries Docker Hub: https://hub.docker.com/u/opensourcefoundries/dashboard/

.. _gateway-ansible GitHub repository: https://github.com/OpenSourceFoundries/gateway-ansible
