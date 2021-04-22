Testing Container
^^^^^^^^^^^^^^^^^
On your device, ``curl`` is not available, instead run ``wget`` as following to 
test the container:

.. prompt:: bash device:~$, auto

    device:~$ wget -qO- 127.0.0.1:8080

**Example Output**:

.. prompt:: text

     Hello world

You can also test the container from an external device connected to the same 
network. For example, your host machine, the same computer you access your device over ssh.
Run the curl command with the device IP address:

.. prompt:: bash host:~$, auto

    host:~$ #Example curl 192.168.15.11:8080
    host:~$ curl <device IP>:8080

**Example Output**:

.. prompt:: text

     Hello world