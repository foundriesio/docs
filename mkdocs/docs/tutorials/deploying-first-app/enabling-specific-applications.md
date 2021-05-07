# Enabling Specific Applications

As you implement more applications in `containers.git`, you may not want
to run all of them on all of your devices. You can use `fioctl` to
specify what applications the device should run.

Instead of enabling the `shellhttpd`, which is already done as mentioned
before. Let's use `fioctl` to first disable and then enable the
`shellhttpd` application. Make sure to follow the `aktualizr-lite` logs
on your device with the following command:

bash device:~$

sudo journalctl --follow --unit aktualizr-lite

On your host machine, disable `shellhttpd` by replacing the list of apps
with a simple comma:

bash host:~$, auto

host:~$ fioctl devices config updates --compose-apps --apps ,
&lt;device-name&gt;

**Example Output**:

text

Changing apps from: \[shellhttpd\] -&gt; \[\] Changing packagemanager to
ostree+compose\_apps

In a maximum of 2 minutes, you should see `aktualizr-lite` remove the
application.

Once `aktualizr-lite` finishes its changes, use `docker ps` to see if
there are any containers running on the device:

bash device:~$, auto

device:~$ docker ps

**Example Output**:

text

CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES

On the device, open the `aktualizr-lite` log again and watch as you
re-enable `shellhttpd`:

bash device:~$

sudo journalctl --follow --unit aktualizr-lite

Enable the `shellhttpd` application on your device:

bash host:~$, auto

host:~$ fioctl devices config updates --compose-apps --apps shellhttpd
&lt;device-name&gt;

**Example Output**:

text

Changing apps from: \[\] -&gt; \[shellhttpd\] Changing packagemanager to
ostree+compose\_apps

Again in a maximum of 2 minutes, you should see `aktualizr-lite` add the
application.

On your device, test the container again by running the following
command:

bash device:~$, auto

device:~$ wget -qO- 127.0.0.1:8080

**Example Output**:

text

Hello world

Check the running containers:

bash device:~$, auto

device:~$ docker ps

**Example Output**:

text

CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES 72a3d00dbc1c
hub.foundries.io/&lt;factory&gt;/shellhttpd "/usr/local/bin/http…" 2
hours ago Up 2 hours 0.0.0.0:8080-&gt;8080/tcp shellhttpd\_httpd\_1
