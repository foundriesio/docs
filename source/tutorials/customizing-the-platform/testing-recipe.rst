Testing Applications
^^^^^^^^^^^^^^^^^^^^

Once your build is successful, wait until your device reboots.

On your device, use the following command to list the ``shellhttpd`` service:

.. prompt:: bash device:~$, auto

    device:~$ systemctl list-unit-files | grep enabled | grep shellhttpd


::

    shellhttpd.service                         enabled         enabled

Verify the status of ``shellhttpd``:

.. prompt:: bash device:~$, auto

    device:~$ systemctl status shellhttpd

::

      shellhttpd.service - Start up Shellhttpd Application
         Loaded: loaded (/usr/lib/systemd/system/shellhttpd.service; enabled; vendor preset: enabled)
         Active: active (running) since
       Main PID: 404 (sh)
          Tasks: 2 (limit: 777)
         Memory: 2.1M
         CGroup: /system.slice/shellhttpd.service
                 ├─404 /bin/sh /usr/share/shellhttpd/httpd.sh
                 └─413 nc -c -l -p 8090

Using a second terminal, test your application using ``curl`` from any external device connected to the same network,
such as your computer.

.. prompt:: bash host:~$, auto

    host:~$ #Example curl 192.168.15.11:8090
    host:~$ curl <device IP>:8090


::

     Hello from Shellhttpd Recipe

Finally, from the same device, try to use ``curl`` instead of ``wget``:

.. prompt:: bash device:~$, auto

    device:~$ curl localhost:8090

::

     Hello from Shellhttpd Recipe
