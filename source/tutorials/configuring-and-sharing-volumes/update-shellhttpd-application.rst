Update Shellhttpd
^^^^^^^^^^^^^^^^^

The previous section, :ref:`tutorial-dynamic-configuration-file`, shows how to send configuration files using :term:`fioctl`.
You also saw where the file is located on the device: ``/var/run/secrets/shellhttpd.conf``

However, ``shellhttpd`` is not yet using this file.

You will learn how to modify ``docker-compose.yml`` so that the app uses the host machine's ``/var/run/secrets/shellhttpd.conf``.

Start by removing ``shellhttpd.conf`` from the ``Dockerfile`` to simplify your app:

.. code-block:: console

    $ vi shellhttpd/Dockerfile

.. code-block:: docker

     FROM alpine
     
     COPY httpd.sh /usr/local/bin/
     
     CMD ["/usr/local/bin/httpd.sh"]

Edit ``docker-compose.yml`` and change the ``volumes`` stanza to share the ``/var/run/secrets`` folder.

.. code-block:: console

    $ vi shellhttpd/docker-compose.yml

.. code-block:: yaml

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

.. code-block:: console

    $ git status
    $ git add shellhttpd/Dockerfile
    $ git add shellhttpd/docker-compose.yml
    $ git commit -m "Updating shared folder path"
    $ git push

Make sure you received your update by checking the latest **Target** on the :guilabel:`Devices` tab in your Factory.

Once you receive the update, the Docker log will show the new message configured with Fioctl in the previous section:

.. code-block:: console

    $ docker logs -f shellhttpd_httpd_1

     PORT=8080
     MSG=Hello from fioctl

If you test the app with ``curl``, it will also display the new message:

.. code-block:: console

    $ curl <device IP>:8080

     Hello from fioctl

Repeat the ``fioctl config`` command in the previous section to confirm everything is working.
Update the configuration file using Fioctl on your host machine:

.. code-block:: console

    $ fioctl devices config set <device-name> shellhttpd.conf="MSG=\"New config file updated over-the-air\""

Wait, then test your app again:

.. code-block:: console

   $ curl <device IP>:8080

   New config file updated over-the-air
