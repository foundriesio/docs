.. _tutorial-configuring-and-sharing-volumes-using-docker:

Copy the Configuration File with Dockerfile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create ``shellhttpd.conf`` in your local container repository in the ``shellhttpd`` folder, which holds your ``Dockerfile``:

.. code-block:: console

    $ echo -e 'PORT=8080\nMSG="Hello from the file copied in the Dockerfile"' > shellhttpd/shellhttpd.conf

Verify the ``shellhttpd.conf`` file:

.. code-block:: console

    $ cat shellhttpd/shellhttpd.conf

     PORT=8080
     MSG="Hello from the file copied in the Dockerfile"

Edit the ``Dockerfile`` to create the ``shellhttpd`` folder and copy ``shellhttpd.conf`` to it:

.. code-block:: docker

    FROM alpine
    
    RUN mkdir /home/shellhttpd/
     
    COPY shellhttpd.conf /home/shellhttpd/
    
    COPY httpd.sh /usr/local/bin/
    
    CMD ["/usr/local/bin/httpd.sh"]

Commit and push the changes.

.. code-block:: console

    $ git status
    $ git add shellhttpd/shellhttpd.conf
    $ git add shellhttpd/httpd.sh
    $ git add shellhttpd/Dockerfile
    $ git commit -m "Adding config file with Dockerfile"
    $ git push

Wait for the FoundriesFactory™ Platform's CI job to finish and for your device to receive the new target.

To check if your device is up-to-date, from your Factory page check :guilabel:`Devices`.
You should see a new number at the end of the **Target** name. For example, ``raspberrypi4-64-lmp-5``.

When the device is up-to-date, the **Status** icon will change to green.

.. figure:: /_static/tutorials/configuring-and-sharing-volumes/devices.png
   :width: 900
   :align: center

   Device list

Test the container from an external device connected to the same network, such as your computer:

.. code-block:: console

    $ curl <Device IP>:8080

     Hello from the file copied in the Dockerfile
