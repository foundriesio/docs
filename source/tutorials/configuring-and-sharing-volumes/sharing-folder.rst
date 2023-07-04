Sharing a Folder
^^^^^^^^^^^^^^^^

When you share a folder, the operating system and running containers can see and consume its files.
This is one way in which they can interact.

.. caution::
   When you bind mount a file into a container, you will usually want to bind mount the parent directory/folder.
   If a bind mount destination does not exist, Docker will create the endpoint as an empty directory rather than a file.

In, :ref:`tutorial-configuring-and-sharing-volumes-using-docker`, you created and copied the configuration file to ``/home/shellhttpd/``.
Keep the changes because you will share the same folder to see what happens.
Edit ``docker-compose.yml``, adding the ``volumes`` stanza:

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
           - /var/rootdirs/home/fio/shellhttpd:/home/shellhttpd/
         ports:
           - 8080:${PORT-8080}
         environment:
           MSG: "${MSG-Hello world}"

Above, ``volumes:`` is added with the value ``/var/rootdirs/home/fio/shellhttpd:/home/shellhttpd/``.
This means that ``/var/rootdirs/home/fio/shellhttpd`` from your host machine will be mounted over the container's ``/home/shellhttpd`` folder.
The container folder content will be **overwritten** by the host machine's. 
Thus, as the host machine folder is empty, the ``shellhttpd.conf`` you copied in the ``Dockerfile`` will **disappear**.

Check your changes, add, commit, and push:

.. prompt:: bash host:~$, auto

    host:~$ git status
    host:~$ git add shellhttpd/docker-compose.yml
    host:~$ git commit -m "Adding shared folder"
    host:~$ git push

Make sure you received your update by checking the latest **Target** on the :guilabel:`Devices` tab in your Factory.

Open a terminal connected to your device and check the running containers:

.. prompt:: bash device:~$, auto

    device:~$ docker ps

::

     CONTAINER ID   IMAGE                               COMMAND                  CREATED          STATUS          PORTS                    NAMES
     a2d425490201   hub.foundries.io/<factory>/shellhttpd   "/usr/local/bin/http…"   20 minutes ago   Up 20 minutes   0.0.0.0:8080->8080/tcp   shellhttpd_httpd_1

Monitor the docker logs:

.. prompt:: bash device:~$, auto

    device:~$ docker logs --follow shellhttpd_httpd_1

::

     PORT=8080
     MSG=Hello world

Open a second terminal connected to your device and check for ``/var/rootdirs/home/fio/shellhttpd``:

.. prompt:: bash device:~$, auto

    device:~$ ls /var/rootdirs/home/fio/shellhttpd/

The folder is empty and was automatically created when the Docker image was launched. 
Create a new configuration file inside that folder and follow the logs from the first terminal:

.. prompt:: bash device:~$, auto

    device:~$ sudo bash -c 'echo -e "MSG=\"Hello from shared folder\"" > /var/rootdirs/home/fio/shellhttpd/shellhttpd.conf'
              
In the first terminal you should see the new ``MSG`` value:

::

     PORT=8080
     MSG=Hello from shared folder

To confirm the change, test the container from an external device connected to the same network, such as your computer.

.. prompt:: bash host:~$, auto

    host:~$ curl <device IP>:8080

::

     Hello from shared folder

You have now seen how to share a folder with the container and how to manually update the configuration while the container is running.
