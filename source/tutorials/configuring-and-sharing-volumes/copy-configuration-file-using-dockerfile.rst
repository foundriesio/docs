.. _tutorial-configuring-and-sharing-volumes-using-docker:

Copy the Configuration File with Dockerfile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create ``shellhttpd.conf`` in your local container repository in the ``shellhttpd`` folder, which holds your ``Dockerfile``:

.. prompt:: bash host:~$, auto

    host:~$ echo -e 'PORT=8080\nMSG="Hello from the file copied in the Dockerfile"' > shellhttpd/shellhttpd.conf

Verify the ``shellhttpd.conf`` file:

.. prompt:: bash host:~$, auto

    host:~$ cat shellhttpd/shellhttpd.conf

::

     PORT=8080
     MSG="Hello from the file copied in the Dockerfile"

Edit the ``Dockerfile`` to create the ``shellhttpd`` folder and copy ``shellhttpd.conf`` to it:

.. prompt:: bash host:~$, auto

    host:~$ vi shellhttpd/Dockerfile

::

    FROM alpine
    
    RUN mkdir /home/shellhttpd/
     
    COPY shellhttpd.conf /home/shellhttpd/
    
    COPY httpd.sh /usr/local/bin/
    
    CMD ["/usr/local/bin/httpd.sh"]

Commit and push the changes.

.. prompt:: bash host:~$, auto

    host:~$ git status
    host:~$ git add shellhttpd/shellhttpd.conf
    host:~$ git add shellhttpd/httpd.sh
    host:~$ git add shellhttpd/Dockerfile
    host:~$ git commit -m "Adding config file with Dockerfile"
    host:~$ git push

Wait for the FoundriesFactory™ Platform's CI job to finish and for your device to receive the new target.

To check if your device is up-to-date, from your Factory page check :guilabel:`Devices`.
You should see a new number at the end of the **Target** name. For example, ``raspberrypi4-64-lmp-5``.

When the device is up-to-date, the **Status** icon will change to green.

.. figure:: /_static/tutorials/configuring-and-sharing-volumes/devices.png
   :width: 900
   :align: center

   Device list

Test the container from an external device connected to the same network, such as your computer:

.. prompt:: bash host:~$, auto

    host:~$ curl <Device IP>:8080

::

     Hello from the file copied in the Dockerfile
