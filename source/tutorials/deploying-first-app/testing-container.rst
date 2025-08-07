Testing the Container
^^^^^^^^^^^^^^^^^^^^^

``curl`` is not available on your device, instead run ``wget`` on your device to test the container:

.. code-block:: console

    device:~$ wget -qO- 127.0.0.1:8080

     Hello world

You can also test the container from an **external device** connected to the same network, such as your computer.

.. code-block:: console

    $ #Example curl 192.168.15.11:8080
    $ curl <device IP>:8080

     Hello world
