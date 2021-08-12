.. _tutorial-dynamic-configuration-file:

Dynamic Configuration File
^^^^^^^^^^^^^^^^^^^^^^^^^^
In a production environment, you might have a large fleet of devices. 
Configuring each device for your applications would be frustrating. 

FoundriesFactory adds management capabilities to your product configuration: 
by using ``fioctl`` the tool encrypts the configuration file with the devices’ public key.

When the device receives the encrypted file, ``fioconfig`` stores it to a 
persistent volume at ``/var/sota/config.encrypted``. At boot, ``fioconfig`` 
extracts all your configuration files to ``/var/run/secrets/<filename>``. 
This is a tmpfs and is only available when the device is running.
This means only the ``fioctl`` user and the device will know the configuration content and Foundries.io won't.

The following example will configure a single device; however, keep in mind that 
it could be used to affect a larger group of devices if associated with ``devices-groups``. 
This topic will be discussed further in later tutorials.

Use ``fioctl`` on your host machine to remember your device name:

.. prompt:: bash host:~$, auto

    host:~$ fioctl devices list

**Example Output**:

.. prompt:: text

     NAME             FACTORY   TARGET                 STATUS   APPS        UP-TO-DATE
     ----             -------   ------                 ------   ----        ----------
     <device-name>  <factory>  raspberrypi3-64-lmp-8  ONLINE   shellhttpd  true

Run ``fioctl`` to set a configuration file:

.. prompt:: bash host:~$, auto

    host:~$ fioctl devices config set <device-name> shellhttpd.conf="MSG=\"Hello from fioctl\""

On your device, check the folder ``/var/run/secrets``. It could take up to 
5 minute to receive the configuration file. If you changed the ``fioconfig`` 
interval as suggested in the previous tutorial :ref:`tutorial-deploying-first-app`
it could take up to a minute.

.. prompt:: bash device:~$, auto

    device:~$ sudo ls /var/run/secrets/

**Example Output**:

.. prompt:: text

     shellhttpd.conf  wireguard-client

Read the file content:

.. prompt:: bash device:~$, auto

    device:~$ sudo cat /var/run/secrets/shellhttpd.conf

**Example Output**:

.. prompt:: text

     MSG="Hello from fioctl"
