Testing Applications
^^^^^^^^^^^^^^^^^^^^

If your build is already successful, wait until your device reboots.

On your device, use the following command to list the ``shellhttpd`` service:

.. prompt:: bash device:~$, auto

    device:~$ systemctl list-unit-files | grep enabled | grep shellhttpd

**Example Output**:

.. prompt:: text

    shellhttpd.service                         enabled         enabled

Verify the ``shellhttpd`` application status:

.. prompt:: bash device:~$, auto

    device:~$ systemctl status shellhttpd

**Example Output**:

.. prompt:: text

      shellhttpd.service - Start up Shellhttpd Application
         Loaded: loaded (/usr/lib/systemd/system/shellhttpd.service; enabled; vendor preset: enabled)
         Active: active (running) since
       Main PID: 404 (sh)
          Tasks: 2 (limit: 777)
         Memory: 2.1M
         CGroup: /system.slice/shellhttpd.service
                 ├─404 /bin/sh /usr/share/shellhttpd/httpd.sh
                 └─413 nc -c -l -p 8090

Using a second terminal, test your application using ``curl`` in any external 
device connected to the same network (e.g. your host machine: the same computer 
you use to access your device with ssh).

.. prompt:: bash host:~$, auto

    host:~$ #Example curl 192.168.15.11:8090
    host:~$ curl <device IP>:8090

**Example Output**:

.. prompt:: text

     Hello from Shellhttpd Recipe

Finally, in the same device, try to use ``curl`` instead of ``wget``:

.. prompt:: bash device:~$, auto

    device:~$ curl localhost:8090

**Example Output**:

.. prompt:: text

     Hello from Shellhttpd Recipe