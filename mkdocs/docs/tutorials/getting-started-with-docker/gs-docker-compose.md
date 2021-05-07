# docker-compose.yml

This is a YAML file defining services, networks, and volumes for
multi-container Docker applications. In other words, all the parameters
you have used with `docker run` you could specify in a
`docker-compose.yml` file. Then, with a single command, create and start
all the services with your configurations.

In this example, we will launch just one image, but keep in mind that a
`docker-compose.yml` file could specify more than one image at the same
time.

Tip

For more information, see the [Compose File Version 3
Reference](https://docs.docker.com/compose/compose-file/compose-file-v3/)

Move the default `docker-compose.yml` from `shellhttpd.disabled` to your
folder:

bash host:~$, auto

host:~$ mv ../shellhttpd.disabled/docker-compose.yml .

Read the `docker-compose.yml` file:

bash host:~$, auto

host:~$ cat docker-compose.yml

**docker-compose.yml**:

text

version: '3.2'

services:  
httpd:  
image: hub.foundries.io/&lt;factory&gt;/shellhttpd:latest restart:
always ports: - 8080:${PORT-8080} environment: MSG: "${MSG-Hello world}"

Most of the parameters were already used in the previous commands. The
only thing you need to change is the image parameter.

In the next tutorial, you will build and deploy the image with
FoundriesFactory and there the image with `hub.foundries.io` will be
necessary.

For now, because you are still developing locally, you need to edit the
image parameter to use the image you have built in the previous steps.

Change the image parameter to the name and tag we built locally
`shellhttpd:1.0`:

bash host:~$, auto

host:~$ gedit docker-compose.yml

**docker-compose.yml**:

text

version: '3.2'

services:  
httpd:

\# image: hub.foundries.io/&lt;factory&gt;/shellhttpd:latest  
image: shellhttpd:1.0 restart: always ports: - 8080:${PORT-8080}
environment: MSG: "${MSG-Hello world}"

Notice that the MSG variable is configured to use `Hello world` as
default.

To run your `docker-compose` application, execute the
`docker-compose up --detach` command.

bash host:~$, auto

host:~$ docker-compose up --detach

Where:  
-   `--detach` or `-d` - Run containers in the background.

To verify the running containers:

bash host:~$, auto

host:~$ docker ps

**Example Output**:

text

CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES dbc969a5487d
shellhttpd:1.0 "/usr/local/bin/http…" 3 minutes ago Up 3 minutes
0.0.0.0:8080-&gt;8080/tcp shellhttpd\_httpd\_1

Test the container with `curl`:

bash host:~$, auto

host:~$ curl 127.0.0.1:8080

**Example Output**:

text

Hello world
