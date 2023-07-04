.. _tutorial-dynamic-configuration-file:

Dynamic Configuration File
^^^^^^^^^^^^^^^^^^^^^^^^^^
In a production environment, you may have a fleet of devices. 
Configuring each device would be frustrating. 
FoundriesFactory® adds management capabilities to your product configuration. 
With Fioctl®, the configuration file is encrypted with the devices’ public key.

When the device receives the encrypted file, ``fioconfig`` stores it to a persistent volume at ``/var/sota/config.encrypted``.
At boot, ``fioconfig`` extracts all your configuration files to ``/var/run/secrets/<filename>``. 
This is a temporary file system only available while the device is running.
This means only the ``fioctl`` user—you—and the device will know the configuration content; Foundries.io™ will not.

.. hint::
   While the following configures a single device, it can also be used to affect a group of devices if associated with ``devices-groups``. 
   This topic will be discussed further in later tutorials.

Use Fioctl on your host machine to remember your device name:

.. prompt:: bash host:~$, auto

    host:~$ fioctl devices list

::

     NAME             FACTORY   TARGET                 STATUS   APPS        UP-TO-DATE
     ----             -------   ------                 ------   ----        ----------
     <device-name>  <factory>  raspberrypi3-64-lmp-8  ONLINE   shellhttpd  true

Now use Fioctl to set a configuration file:

.. prompt:: bash host:~$, auto

    host:~$ fioctl devices config set <device-name> shellhttpd.conf="MSG=\"Hello from fioctl\""

On your device, check the folder ``/var/run/secrets``.
It may take a few minutes to receive the configuration file.
If you changed the ``fioconfig`` interval as suggested in :ref:`tutorial-deploying-first-app`,
it could take up to a minute.

.. prompt:: bash device:~$, auto

    device:~$ sudo ls /var/run/secrets/

::

     shellhttpd.conf  wireguard-client

Read the file content:

.. prompt:: bash device:~$, auto

    device:~$ sudo cat /var/run/secrets/shellhttpd.conf

::

     MSG="Hello from fioctl"
