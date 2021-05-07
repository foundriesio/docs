# Extra commands

Here is a list of useful commands when working with Docker containers.

## docker ps

The first command is: `docker ps`. It displays the running containers on
the device. Add the `--all` parameter to see all containers on the
device (even if they aren't running).

bash host:~$, auto

host:~$ docker ps

**Example Output**:

text

CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES 244a84742697
shellhttpd:1.0 "/usr/local/bin/http…" 6 minutes ago Up 6 minutes
0.0.0.0:8080-&gt;8080/tcp shellhttpd

## docker logs

Often, it is useful to watch Docker container logs. Use
`docker logs <container name>` to see the logs of a specific container.
If you want the command to keep following the log, use the `--follow`
parameter:

In this case, the log might be empty unless you tested the `shellhttpd`
application with `curl` or the browser:

bash host:~$, auto

host:~$ docker logs --follow shellhttpd

**Example Output**:

text

GET / HTTP/1.1 Host: 127.0.0.1:8080 Connection: keep-alive
Cache-Control: max-age=0 DNT: 1 Upgrade-Insecure-Requests: 1 User-Agent:
Mozilla/5.0 (X11; Fedora; Linux x86\_64) AppleWebKit/537.36 (KHTML, like
Gecko) Chrome/88.0.4324.150 Safari/537.36 Accept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,\*/\*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none Sec-Fetch-Mode: navigate Sec-Fetch-User: ?1
Sec-Fetch-Dest: document Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7

= Thu Mar 18 01:03:14 UTC 2021 ============================= GET
/favicon.ico HTTP/1.1 Host: 127.0.0.1:8080 Connection: keep-alive
Pragma: no-cache Cache-Control: no-cache User-Agent: Mozilla/5.0 (X11;
Fedora; Linux x86\_64) AppleWebKit/537.36 (KHTML, like Gecko)
Chrome/88.0.4324.150 Safari/537.36 DNT: 1 Accept:
image/avif,image/webp,image/apng,image/svg+xml,image/*,*/\*;q=0.8
Sec-Fetch-Site: same-origin Sec-Fetch-Mode: no-cors Sec-Fetch-Dest:
image Referer: <http://127.0.0.1:8080/> Accept-Encoding: gzip, deflate,
br Accept-Language: en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7

= Thu Mar 18 01:03:14 UTC 2021 =============================

## docker exec

The `docker exec` command runs a new command in a running container.

To verify the files in root file system of the container, use the
following command:

bash host:~$, auto

host:~$ docker exec shellhttpd ls /usr/local/bin/

**Example Output**:

text

httpd.sh

To check what processes are running inside the container:

bash host:~$, auto

host:~$ docker exec shellhttpd ps

**Example Output**:

text

PID USER TIME COMMAND 1 root 0:00 {httpd.sh} /bin/sh -e
/usr/local/bin/httpd.sh 13 root 0:00 nc -l -p 8080 36 root 0:00 ps

Finally, you can start a shell inside the container with:

bash host:~$, auto

host:~$ docker exec -it shellhttpd sh

**Example Output**:

bash docker:~$, auto

docker:~$ ls bin dev etc home lib media mnt opt proc root run sbin srv
sys tmp usr var docker:~$ exit

Where:  
-   `-i` - keep STDIN open even if not attached.
-   `-t` - allocate a pseudo-TTY.
-   `shellhttpd` - container name.
-   `sh` - shell command.

## docker rm

To remove the container, run the command below:

bash host:~$, auto

host:~$ docker stop shellhttpd host:~$ docker rm shellhttpd

During development, it is very common to change the Docker image and
test it again, so let’s give it a try:

In the file `httpd.sh`, we specify the MSG variable with `${MSG-OK}`.
This means if MSG is not specified, set it with the default value `OK`.

Let’s change the `OK` to `FoundriesFactory`, then rebuild and run:

bash host:~$, auto

host:~$ gedit httpd.sh

**httpd.sh**:

text

\#!/bin/sh -e

PORT="${PORT-8080}" MSG="${MSG-FoundriesFactory}"

RESPONSE="HTTP/1.1 200 OKrnrn${MSG}rn"

while true; do  
echo -en "$RESPONSE" | nc -l -p "${PORT}" || true echo "= $(date)
============================="

done

Build and run the container again:

bash host:~$, auto

host:~$ docker build --tag shellhttpd:1.0 . host:~$ docker run --name
shellhttpd -d -p 8080:8080 shellhttpd:1.0

Test the new change with curl:

bash host:~$, auto

host:~$ curl 127.0.0.1:8080

**Example Output**:

text

FoundriesFactory

The `docker run` command can accept many other parameters. For example,
the `--env` parameter which specifies an environment variable to the
container. Remove the previous image and launch it again with:
`--env MSG=MyFirstContainer`

Test the new change with curl:

bash host:~$, auto

host:~$ docker stop shellhttpd host:~$ docker rm shellhttpd host:~$
docker run --env MSG=MyFirstContainer --name shellhttpd -d -p 8080:8080
shellhttpd:1.0

Testing the new environment variable:

bash host:~$, auto

host:~$ curl 127.0.0.1:8080

**Example Output**:

text

MyFirstContainer

Use `docker exec` to echo the MSG variable inside the container:

bash host:~$, auto

host:~$ docker exec -it shellhttpd sh

**Inside the Container**:

bash docker:~$, auto

docker:~$ echo $MSG  
MyFirstContainer

docker:~$ exit

Remove the container:

bash host:~$, auto

host:~$ docker stop shellhttpd host:~$ docker rm shellhttpd

All these commands are important in understanding how Docker containers
work. Now let’s see how `docker-compose` works.
