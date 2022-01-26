.. _ref-factory-registration-ref:

Manufacturing Process for Device Registration
=============================================

lmp-device-auto-register works great when run manually and can be configured
to auto register devices in **CI**
:ref:`builds <ug-lmp-device-auto-register>`. However,
a different process is required for provisioning production devices.
The key to production provisioning lies in owning the
:ref:`device gateway PKI <ref-device-gateway>`. Once a customer has
control of their PKI, they can create client TLS certificates for
devices that will be trusted by the Foundries.io device gateway.

Customers all have unique requirements, so Foundries.io created a
`reference implementation`_ that customers can fork and modify to
their liking. Here are some common ways to use this reference.

Fully detached
--------------
In this scenario devices connect to a reference server instance on
a private network. This network is isolated from the internet
(api.foundries.io). Devices get a valid signed client certificate from
the reference server. Each device will be created via api.foundries.io
**on-the-fly** the first time they connect.

This scenario is handy for certain security constrained setups. However,
it does have a couple of potential drawbacks:

 * Devices don't show up on Foundries.io until the first time
   they connect.

 * Devices won't have Foundries.io managed configuration data available
   until this first connection.

Registering Production Device by Default
----------------------------------------

After the development cycle is over, and it is expected that every new
device to be registered is a production device, it might be good to enable this
by default in LmP.

Create or modify the ``lmp-device-register_%.bbappend`` file in the factory's
``meta-subscriber-overrides``:

.. prompt:: bash host:~$

   mkdir -p meta-subscriber-overrides/recipes-sota/lmp-device-register/
   echo 'PACKAGECONFIG += "production"' >> meta-subscriber-overrides/recipes-sota/lmp-device-register/lmp-device-register_%.bbappend

The images created with this configuration includes ``PRODUCTION=on`` by default
on the command ``lmp-device-register``.

This is very usefully when the update plan is to use
:ref:`ref-production-targets`.

lmp-device-auto-register configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Devices can also have :ref:`ug-lmp-device-auto-register` enabled. 
In order to have the device run ``lmp-device-register`` automatically
on boot.

After following those steps a FoundriesFactory can copy `lmp-device-auto-register`_ into their
meta-subscriber-overrides.git production branch as
``recipes-support/lmp-device-auto-register/lmp-device-auto-register/lmp-device-auto-register``
and add the following two environment variables to that specific file at
the top for example::

  #!/bin/sh -e

  TOKEN_FILE=${TOKEN_FILE-/etc/lmp-device-register-token}

  DEVICE_API=http://<IP of reference server>/sign
  PRODUCTION=1

  ... 

Then it will use the reference server as the one where to register instead
of using https://api.foundries.io. 

Registration reference configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The registration reference should work out-of-the box for this scenario.
The operator simply needs to copy their PKI keys as described in the
reference server's `README.md`_.

Partially detached
------------------
In this scenario devices connect to a reference server instance on
a private network, but the reference server has access to
api.foundries.io. The reference server can create device entries via
api.foundries.io as devices are registered.

Additionally, if devices have access to ota-lite.foundries.io:8443,
they can download their initial fioconfig configuration data.

lmp-device-auto-register configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A factory can also customize the ``lmp-device-auto-register`` as is
explained in :ref:`ug-lmp-device-auto-register`.

For example::

 #!/bin/sh -e

 if [ -f /var/sota/sql.db ] ; then
 	echo "$0: ERROR: Device appears to already be registered"
 	exit 1
 fi

 # Done in 2 parts. This first part will remove trailing \n's and make
 # the output all space separated. The 2nd part makes it comma separated.
 [ -d /var/sota/compose-apps ] && APPS=$(ls /var/sota/compose-apps)
 APPS=$(echo ${APPS} | tr ' ' ',')
 if [ -n "${APPS}" ] ; then
 	echo "$0: Registering with default apps = ${APPS}"
 	APPS="-a ${APPS}"
 else
 	echo "$0: Registering with all available apps"
 fi

 # Register the device but don't start the daemon:
 DEVICE_API="http://example.com/sign" \
 PRODUCTION=1 \
 	/usr/bin/lmp-device-register --start-daemon=0 -T na ${APPS}

 # Pull down the device's initial configuration
 fioconfig check-in

 # Optionally start services, or maybe just power off the device
 #systemctl start aktualizr-lite
 #systemctl start fioconfig

Registration reference configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The registration reference should work out-of-the box for this scenario.
The operator will need to create a Foundries.io API token with scope
``devices:create``. They can take this token and configure the
reference server as per the README.md.

.. _reference implementation:
   https://github.com/foundriesio/factory-registration-ref
.. _README.md:
   https://github.com/foundriesio/factory-registration-ref/blob/main/README.md
.. _lmp-device-auto-register:
   https://github.com/foundriesio/meta-lmp/blob/master/meta-lmp-base/recipes-support/lmp-device-auto-register/lmp-device-auto-register/lmp-device-auto-register
