# Copy the Configuration File using Dockerfile

Create the `shellhttpd.conf` file in your local container repository in
the `shellhttpd` folder, which holds your `Dockerfile`:

bash host:~$, auto

host:~$ echo -e 'PORT=8080nMSG="Hello from the file copied in the
Dockerfile"' &gt; shellhttpd/shellhttpd.conf

Verify the `shellhttpd.conf` file:

bash host:~$, auto

host:~$ cat shellhttpd/shellhttpd.conf

**Example Output**:

text

PORT=8080 MSG="Hello from the file copied in the Dockerfile"

Edit the `Dockerfile` to create the `shellhttpd` folder and copy
`shellhttpd.conf` to it:

bash host:~$, auto

host:~$ gedit shellhttpd/Dockerfile

**shellhttpd/Dockerfile**:

text

FROM alpine

RUN mkdir /home/shellhttpd/

COPY shellhttpd.conf /home/shellhttpd/

COPY httpd.sh /usr/local/bin/

CMD \["/usr/local/bin/httpd.sh"\]

Commit and push all changes done in the `containers` folder

bash host:~$, auto

host:~$ git status host:~$ git add shellhttpd/shellhttpd.conf host:~$
git add shellhttpd/httpd.sh host:~$ git add shellhttpd/Dockerfile
host:~$ git commit -m "Adding config file with Dockerfile" host:~$ git
push

Wait for your FoundriesFactory CI job to finish and for your device to
receive the new target as an over-the-air update:

<figure>
<img src="/_static/tutorials/configuring-and-sharing-volumes/building.png" class="align-center" width="900" alt="FoundriesFactory CI Job running" /><figcaption aria-hidden="true">FoundriesFactory CI Job running</figcaption>
</figure>

In this example, the build version is `5`. To check if your device is
already up-to-date, check `Devices` until you see `-5` at the end of the
**Target** name. For example `raspberrypi3-64-lmp-5`.

When the device is up-to-date, the **Status** icon will change to green.

<figure>
<img src="/_static/tutorials/configuring-and-sharing-volumes/devices.png" class="align-center" width="900" alt="Device list" /><figcaption aria-hidden="true">Device list</figcaption>
</figure>

Test the container from an external device connected to the same network
(e.g. your host machine: the same computer you use to access your device
with ssh).

bash host:~$, auto

host:~$ curl &lt;Device IP&gt;:8080

**Example Output**:

text

Hello from the file copied in the Dockerfile
