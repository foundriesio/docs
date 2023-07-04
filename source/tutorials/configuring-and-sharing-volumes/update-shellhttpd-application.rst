Update Shellhttpd
^^^^^^^^^^^^^^^^^

The previous section, :ref:`tutorial-dynamic-configuration-file`, shows how to send configuration files using Fioctl®.
You also saw where the file is located on the device: ``/var/run/secrets/shellhttpd.conf``

However, ``shellhttpd`` is not yet using this file.

You will learn how to modify ``docker-compose.yml`` so that the app uses the host machine's ``/var/run/secrets/shellhttpd.conf``.

Start by removing ``shellhttpd.conf`` from the ``Dockerfile`` to simplify your app:

.. prompt:: bash host:~$, auto

    host:~$ gedit shellhttpd/Dockerfile

::

     FROM alpine
     
     COPY httpd.sh /usr/local/bin/
     
     CMD ["/usr/local/bin/httpd.sh"]

Edit ``docker-compose.yml`` and change the ``volumes`` stanza to share the ``/var/run/secrets`` folder.

.. prompt:: bash host:~$, auto

    host:~$ gedit shellhttpd/docker-compose.yml

::

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

Check your changes, add, commit, and push:

.. prompt:: bash host:~$, auto

    host:~$ git status
    host:~$ git add shellhttpd/Dockerfile
    host:~$ git add shellhttpd/docker-compose.yml
    host:~$ git commit -m "Updating shared folder path"
    host:~$ git push

Make sure you received your update by checking the latest **Target** on the :guilabel:`Devices` tab in your Factory.

Once you receive the update, the Docker log will show the new message configured with Fioctl in the previous section:

.. prompt:: bash device:~$, auto

    device:~$ docker logs -f shellhttpd_httpd_1

::

     PORT=8080
     MSG=Hello from fioctl

If you test the app with ``curl``, it will also display the new message:

.. prompt:: bash host:~$, auto

    host:~$ curl <device IP>:8080

::

     Hello from fioctl

Repeat the ``fioctl config`` command in the previous section to confirm everything is working.
Update the configuration file using Fioctl on your host machine:

.. prompt:: bash host:~$, auto

    host:~$ fioctl devices config set <device-name> shellhttpd.conf="MSG=\"New config file updated over-the-air\""

Wait, then test your app again:

.. prompt:: bash host:~$, auto

    host:~$ curl <device IP>:8080

::

     New config file updated over-the-air
