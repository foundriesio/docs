.. _tutorial-deploying-first-app-testing:

Testing the Container
^^^^^^^^^^^^^^^^^^^^^

``curl`` is not available on your device, instead run ``wget`` to test the container like so:

.. prompt:: bash device:~$, auto

    device:~$ wget -qO- 127.0.0.1:8080

**Example Output**:

.. prompt:: text

     Hello world

You can also test the container from an external device connected to the same 
network (e.g. your host machine: the same computer you use to access your device with ssh).

.. prompt:: bash host:~$, auto

    host:~$ #Example curl 192.168.15.11:8080
    host:~$ curl <device IP>:8080

**Example Output**:

.. prompt:: text

     Hello world