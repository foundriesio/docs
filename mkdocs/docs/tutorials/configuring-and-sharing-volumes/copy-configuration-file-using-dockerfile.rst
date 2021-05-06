.. _tutorial-configuring-and-sharing-volumes-using-docker:

Copy the Configuration File using Dockerfile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create the ``shellhttpd.conf`` file in your local container repository in the
``shellhttpd`` folder, which holds your ``Dockerfile``:

.. prompt:: bash host:~$, auto

    host:~$ echo -e 'PORT=8080\nMSG="Hello from the file copied in the Dockerfile"' > shellhttpd/shellhttpd.conf

Verify the ``shellhttpd.conf`` file:

.. prompt:: bash host:~$, auto

    host:~$ cat shellhttpd/shellhttpd.conf

**Example Output**:

.. prompt:: text

     PORT=8080
     MSG="Hello from the file copied in the Dockerfile"

Edit the ``Dockerfile`` to create the ``shellhttpd`` folder and copy ``shellhttpd.conf`` to it:

.. prompt:: bash host:~$, auto

    host:~$ gedit shellhttpd/Dockerfile

**shellhttpd/Dockerfile**:

.. prompt:: text

    FROM alpine
    
    RUN mkdir /home/shellhttpd/
     
    COPY shellhttpd.conf /home/shellhttpd/
    
    COPY httpd.sh /usr/local/bin/
    
    CMD ["/usr/local/bin/httpd.sh"]

Commit and push all changes done in the ``containers`` folder

.. prompt:: bash host:~$, auto

    host:~$ git status
    host:~$ git add shellhttpd/shellhttpd.conf
    host:~$ git add shellhttpd/httpd.sh
    host:~$ git add shellhttpd/Dockerfile
    host:~$ git commit -m "Adding config file with Dockerfile"
    host:~$ git push

Wait for your FoundriesFactory CI job to finish and for your device to receive 
the new target as an over-the-air update:

.. figure:: /_static/tutorials/configuring-and-sharing-volumes/building.png
   :width: 900
   :align: center

   FoundriesFactory CI Job running

In this example, the build version is ``5``. To check if your device is already 
up-to-date, check :guilabel:`Devices` until you see ``-5`` at the end of the **Target** name. For example ``raspberrypi3-64-lmp-5``.

When the device is up-to-date, the **Status** icon will change to green.

.. figure:: /_static/tutorials/configuring-and-sharing-volumes/devices.png
   :width: 900
   :align: center

   Device list

Test the container from an external device connected to the same network 
(e.g. your host machine: the same computer you use to access your device with ssh).

.. prompt:: bash host:~$, auto

    host:~$ curl <Device IP>:8080

**Example Output**:

.. prompt:: text

     Hello from the file copied in the Dockerfile