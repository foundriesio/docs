Update shellhttpd Application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The previous section, :ref:`tutorial-dynamic-configuration-file`, shows how to 
send configuration files using ``fioctl``. The section also shows where the file 
is located on the device: ``/var/run/secrets/shellhttpd.conf``

The ``shellhttpd`` application is not using this file yet.

This section shows how to modify the ``docker-compose.yml`` file so that the application will
use the host machine's ``/var/run/secrets/shellhttpd.conf`` file instead of a configuration file built
into the container.

Let’s start by changing the ``Dockerfile``.  Remove the addition of the 
``shellhttpd.conf`` file to simplify your application:

.. prompt:: bash host:~$, auto

    host:~$ gedit shellhttpd/Dockerfile

**shellhttpd/Dockerfile**:

.. prompt:: text

     FROM alpine
     
     COPY httpd.sh /usr/local/bin/
     
     CMD ["/usr/local/bin/httpd.sh"]

Edit ``docker-compose.yml`` and change the ``volumes`` stanza to share the ``/var/run/secrets`` folder.

.. prompt:: bash host:~$, auto

    host:~$ gedit shellhttpd/docker-compose.yml

**shellhttpd/docker-compose.yml**:

.. prompt:: text

     version: '3.2'
     
     services:
       httpd:
         image: hub.foundries.io/<factory>/shellhttpd:latest
     #    image: shellhttpd:1.0
         restart: always
         volumes:
           - /var/run/secrets:/home/shellhttpd/
         ports:
           - 8080:${PORT-8080}
         environment:
           MSG: "${MSG-Hello world}"

Check your changes, add, commit and push to the server:

.. prompt:: bash host:~$, auto

    host:~$ git status
    host:~$ git add shellhttpd/Dockerfile
    host:~$ git add shellhttpd/docker-compose.yml
    host:~$ git commit -m "Updating shared folder path"
    host:~$ git push

Make sure you received your update by checking the latest **Target** on the :guilabel:`Devices` tab in your Factory.

Once you receive the update, the docker log should show the new message configured with ``fioctl`` in the previous section:

.. prompt:: bash device:~$, auto

    device:~$ docker logs -f shellhttpd_httpd_1

**Example Output**:

.. prompt:: text

     PORT=8080
     MSG=Hello from fioctl

If you test the application with ``curl``, it will also display the new message:

.. prompt:: bash host:~$, auto

    host:~$ curl <device IP>:8080

**Example Output**:

.. prompt:: text

     Hello from fioctl

Let's repeat the ``fioctl config`` command used in the previous section, and confirm
that everything is working.

Update the configuration file using ``fioctl`` in your host machine:

.. prompt:: bash host:~$, auto

    host:~$ fioctl devices config set raspberrypi3-64 shellhttpd.conf="MSG=\"New config file updated over-the-air\""

Wait and test your application again:

.. prompt:: bash host:~$, auto

    host:~$ curl <device IP>:8080

**Example Output**:

.. prompt:: text

     New config file updated over-the-air