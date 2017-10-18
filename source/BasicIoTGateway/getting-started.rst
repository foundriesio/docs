.. highlight:: sh

.. _big-getting-started:

Getting Started
===============

All you need to get started is a gateway device supported by the LTD Basic
IoT Gateway, a computer, and an Internet connection.

Start with a base Linux microPlatform
-------------------------------------

follow the instructions to setup your target hardware with the Linux
microPlatform software following the instructions at
:ref:`linux-getting-started`.

Boot the Board
--------------

#. Connect the UART Serial Adapter to your host PC via USB.

#. Apply power to the HiKey via the barrel jack connector.

Your board should look like this:

.. figure:: /_static/linux/hikey-boot.jpg
   :align: center
   :alt: HiKey when booting

.. highlight:: none

At the serial console, the following login prompt should appear after
the board finishes booting::

  Reference-Platform-Build-X11 2.0+linaro hikey ttyAMA3

  hikey login:

Enter ``osf`` for the username, and ``osf`` for the
password. You will be dropped into a normal user shell, and should now
change the password. The ``osf`` user may use ``sudo`` to obtain
root access on the device.

Load Gateway Containers
-----------------------

Now to deploy some key containerized applications to your device.

One of the greatest advantages of using the Linux microPlatform is that it
makes it easier to deploy and manage container-based applications. What's more,
unlike other container-based embedded device platforms, the Linux microPlatform
allows you to deploy **multiple applications to the same gateway, each
running at the same time in its own container**. This is called
**multitenancy**.

Check out the Linaro Technologies Division `Gateway Containers
<https://github.com/linaro-technologies/gateway-containers>`_
repository for example Docker containers, along with instructions for
how to get them running on your board. Start with the top-level
`gateway-containers README.md`_, and move on to the subdirectories for
containers which interest you.

If you installed Ansible earlier, you can also use Ansible playbooks
to deploy the containers; these are available in the `gateway-ansible
<https://github.com/linaro-technologies/gateway-ansible>`_
repository. (While Ansible isn't supported on Windows, you can run
`Ubuntu in a Docker container <https://hub.docker.com/_/ubuntu/>`_ and
run Ansible from Ubuntu.)

.. _big-whitelist:

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

The following is an example of the output from this command::

  LE Scan ...
  D6:E7:D2:E8:6C:9F (unknown)
  D6:E7:D2:E8:6C:9F Linaro IPSP node

Write down all of the "Linaro IPSP node" Bluetooth addresses, as you
will need these for the next steps.

Disable the whitelist feature
+++++++++++++++++++++++++++++

To turn off the whitelist feature, set USE_WL to '0' in bluetooth_6lowpand.conf

.. _gateway-containers README.md:
   https://github.com/linaro-technologies/gateway-containers/blob/master/README.md
