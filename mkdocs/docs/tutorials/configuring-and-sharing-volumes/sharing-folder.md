# Sharing a Folder

When you share a folder the base operating system and the running
containers will be able to see and consume the files inside it. This is
one option for the host machine and the container to interact.

In the section,
"`tutorial-configuring-and-sharing-volumes-using-docker`", you created
and copied the configuration file to the `/home/shellhttpd/` folder.
Purposefully leave the changes you just did because you will share the
same folder to see what happens.

Edit the `docker-compose.yml` file adding the `volumes` stanza:

bash host:~$, auto

host:~$ gedit shellhttpd/docker-compose.yml

**shellhttpd/docker-compose.yml**:

text

version: '3.2'

services:  
httpd:  
image: hub.foundries.io/&lt;factory&gt;/shellhttpd:latest

\# image: shellhttpd:1.0  
restart: always volumes: -
/var/rootdirs/home/fio/shellhttpd:/home/shellhttpd/ ports: -
8080:${PORT-8080} environment: MSG: "${MSG-Hello world}"

Above, you add the `volumes:` stanza with the value
`/var/rootdirs/home/fio/shellhttpd:/home/shellhttpd/`. This means that
the `/var/rootdirs/home/fio/shellhttpd` folder from your host machine
will be mounted over the container's `/home/shellhttpd` folder. The
container folder content will be **overwritten** by the host machine
folder content. Thus, as the host machine folder is empty, the
`shellhttpd.conf` you copied in the `Dockerfile` will **disappear** in
this new setup.

Check your changes, add, commit and push to the server:

bash host:~$, auto

host:~$ git status host:~$ git add shellhttpd/docker-compose.yml host:~$
git commit -m "Adding shared folder" host:~$ git push

Make sure you received your update by checking the latest **Target** on
the `Devices` tab in your Factory.

Open one terminal connected to your device and check the running
containers:

bash device:~$, auto

device:~$ docker ps

**Example Output**:

text

CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES a2d425490201
hub.foundries.io/&lt;factory&gt;/shellhttpd "/usr/local/bin/http…" 20
minutes ago Up 20 minutes 0.0.0.0:8080-&gt;8080/tcp shellhttpd\_httpd\_1

Monitor the docker logs:

bash device:~$, auto

device:~$ docker logs --follow shellhttpd\_httpd\_1

**Example Output**:

text

PORT=8080 MSG=Hello world

Open a second terminal connected to your device and check for the
`/var/rootdirs/home/fio/shellhttpd` folder:

bash device:~$, auto

device:~$ ls /var/rootdirs/home/fio/shellhttpd/

The folder is empty and was automatically created when the Docker image
was launched. Let’s create a new configuration file inside that folder
and follow the logs from the first terminal:

bash device:~$, auto

device:~$ sudo bash -c 'echo -e "MSG="Hello from shared folder"" &gt;
/var/rootdirs/home/fio/shellhttpd/shellhttpd.conf'

And in the first terminal you should see the new `MSG` value:

**Example Output**:

text

PORT=8080 MSG=Hello from shared folder

Just to confirm the change, test the container from an external device
connected to the same network (e.g. your host machine: the same computer
you use to access your device with ssh).

bash host:~$, auto

host:~$ curl &lt;device IP&gt;:8080

**Example Output**:

text

Hello from shared folder

At this point, you learned how to share a folder with the Docker
container and how to manually update the configuration while the
container is running.
