Configure your device
^^^^^^^^^^^^^^^^^^^^^

At this point, your device should be registered to your Factory according to 
the :ref:`Getting Started guide <gs-register>`. Once your device is registered, two applications start to 
communicate with your Factory: ``aktualizr-lite`` and ``fioconfig``.

**aktualizr-lite**:

This is the daemon responsible for the updates. It checks for new updates and 
implements `The Update Protocol (TUF) <TUF_>`_ to guarantee the integrity of the platform 
and the container updates. 

**fioconfig**:

This is the daemon responsible for managing configuration data for your device. 
The data content used by ``fioconfig`` is encrypted with the device’s public key. 
The device can then get the configuration and use its private key to decrypt. 
``fioconfig`` also stores the encrypted file and extracts it to the userspace.

Both applications are configured to communicate with your Factory every 5 minutes. 
That being said, an update could take from 5 minutes to 10 minutes to be triggered. 
This can be configured according to your product needs.

To improve your experience during this tutorial, you will configure both 
``aktualizr-lite`` and ``fioconfig`` to check every minute.

This configuration will apply just to the device you run the commands below. 
To change it to your entire fleet permanently you have to customize your image.

In your device, create the folder and the file to configure ``aktualizr-lite``:

.. prompt:: bash device:~$

    sudo mkdir -p /etc/sota/conf.d/
    sudo bash -c 'printf "[uptane]\npolling_sec = 60" > /etc/sota/conf.d/z-01-polling.toml'

Create the file to configure ``fioconfig``:

.. prompt:: bash device:~$

    sudo bash -c 'printf "DAEMON_INTERVAL=60" > /etc/default/fioconfig'

Restart both services:

.. prompt:: bash device:~$

    sudo systemctl restart aktualizr-lite
    sudo systemctl restart fioconfig

.. tip::

   In the following instruction, you will disable and enable applications. 
   It will trigger ``aktualizr-lite`` tasks that might be interesting to follow.

   To watch the ``aktualizr-lite`` logs and see the updates, leave a device 
   terminal running the command:

   .. prompt:: bash device:~$

       sudo journalctl -f -u aktualizr-lite

.. _TUF: https://theupdateframework.com/