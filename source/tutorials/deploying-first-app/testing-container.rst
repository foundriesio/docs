Testing the Container
^^^^^^^^^^^^^^^^^^^^^

``curl`` is not available on your device, instead run ``wget`` to test the container like so:

.. prompt:: bash device:~$, auto

    device:~$ wget -qO- 127.0.0.1:8080

::

     Hello world

You can also test the container from an external device connected to the same network, such as your computer.

.. prompt:: bash host:~$, auto

    host:~$ #Example curl 192.168.15.11:8080
    host:~$ curl <device IP>:8080

::

     Hello world
