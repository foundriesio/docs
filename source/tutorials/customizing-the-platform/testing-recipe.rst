Testing Applications
^^^^^^^^^^^^^^^^^^^^

Once your build is successful, wait until your device reboots.

**On your device**, use the following command to list the ``shellhttpd`` service:

.. code-block:: console

    device:~$ systemctl list-unit-files | grep enabled | grep shellhttpd

    shellhttpd.service                         enabled         enabled

Verify the status of ``shellhttpd``:

.. code-block:: console

    device:~$ systemctl status shellhttpd

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

.. code-block:: console

    $ #Example curl 192.168.15.11:8090
    $ curl <device IP>:8090
      Hello from Shellhttpd Recipe

Finally, from your device, try to use ``curl`` instead of ``wget``:

.. code-block:: console

    device:~$ curl localhost:8090
    Hello from Shellhttpd Recipe
