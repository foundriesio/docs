Extra Commands
^^^^^^^^^^^^^^

Here is a list of useful commands when working with Docker containers.

Docker Process Status
"""""""""""""""""""""

The first command to learn is: ``docker ps``.
This displays the running containers on the device.
Add ``--all`` to see all containers on the device, even if they are not running.

.. prompt:: bash host:~$, auto

    host:~$ docker ps

**Example Output**:

.. prompt:: text

     CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
     244a84742697        shellhttpd:1.0       "/usr/local/bin/http…"   6 minutes ago       Up 6 minutes        0.0.0.0:8080->8080/tcp   shellhttpd

Docker Logs
"""""""""""

Use ``docker logs <container name>`` to see the container's logs.
If you want the command to keep following the log, use the ``--follow`` parameter:

The log might be empty unless you tested the ``shellhttpd`` application with ``curl`` or the browser:

.. prompt:: bash host:~$, auto

    host:~$ docker logs --follow shellhttpd

.. prompt:: text

     GET / HTTP/1.1
     Host: 127.0.0.1:8080
     Connection: keep-alive
     Cache-Control: max-age=0
     DNT: 1
     Upgrade-Insecure-Requests: 1
     User-Agent: Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
     Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,\*/\*;q=0.8,application/signed-exchange;v=b3;q=0.9
     Sec-Fetch-Site: none
     Sec-Fetch-Mode: navigate
     Sec-Fetch-User: ?1
     Sec-Fetch-Dest: document
     Accept-Encoding: gzip, deflate, br
     Accept-Language: en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7
     
     = Thu Mar 18 01:03:14 UTC 2021 =============================
     GET /favicon.ico HTTP/1.1
     Host: 127.0.0.1:8080
     Connection: keep-alive
     Pragma: no-cache
     Cache-Control: no-cache
     User-Agent: Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
     DNT: 1
     Accept: image/avif,image/webp,image/apng,image/svg+xml,image/\*,\*/\*;q=0.8
     Sec-Fetch-Site: same-origin
     Sec-Fetch-Mode: no-cors
     Sec-Fetch-Dest: image
     Referer: http://127.0.0.1:8080/
     Accept-Encoding: gzip, deflate, br
     Accept-Language: en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7
     
     = Thu Mar 18 01:03:14 UTC 2021 =============================


Docker Execute
""""""""""""""

The ``docker exec`` command runs a new command in a running container.

To verify the files in the root file system of the container, use the following command:

.. prompt:: bash host:~$, auto

    host:~$ docker exec shellhttpd ls /usr/local/bin/

.. prompt:: text

     httpd.sh

To check what processes are running:

.. prompt:: bash host:~$, auto

    host:~$ docker exec shellhttpd ps

.. prompt:: text

     PID   USER     TIME  COMMAND
     1 root      0:00 {httpd.sh} /bin/sh -e /usr/local/bin/httpd.sh
     13 root      0:00 nc -l -p 8080
     36 root      0:00 ps

Finally, you can start a shell inside the container with:

.. prompt:: bash host:~$, auto

    host:~$ docker exec -it shellhttpd sh

.. prompt:: bash docker:~$, auto

     docker:~$ ls
     bin    dev    etc    home   lib    media  mnt    opt    proc   root   run    sbin   srv    sys    tmp    usr    var
     docker:~$ exit


Where: 
 - ``-i`` - keep STDIN open even if not attached.
 - ``-t`` - allocate a pseudo-TTY.
 - ``shellhttpd`` - container name.
 - ``sh`` - shell command.

Docker Remove
"""""""""""""

To stop and then remove the container, run the commands:

.. prompt:: bash host:~$, auto

    host:~$ docker stop shellhttpd
    host:~$ docker rm shellhttpd

During development it is common to make and test changes to the Docker image.
Let us give this a try.
In ``httpd.sh`` we specify the MSG variable with ``${MSG-OK}``. 
This means if ``MSG`` is not otherwise specified, it is set with the default value "OK".

Using a text editor, change ``OK`` to ``FoundriesFactory``.
Rebuild and run:

.. prompt:: bash host:~$, auto

    host:~$ vi httpd.sh

**httpd.sh**:

.. prompt:: text

     #!/bin/sh -e
     
     PORT="${PORT-8080}"
     MSG="${MSG-FoundriesFactory}"
     
     RESPONSE="HTTP/1.1 200 OK\r\n\r\n${MSG}\r\n"
     
     while true; do
	     echo -en "$RESPONSE" | nc -l -p "${PORT}" || true
	     echo "= $(date) ============================="
     done

Build and run the container again:

.. prompt:: bash host:~$, auto

    host:~$ docker build --tag shellhttpd:1.0 .
    host:~$ docker run --name shellhttpd -d -p 8080:8080 shellhttpd:1.0

Test the new change with curl:

.. prompt:: bash host:~$, auto

    host:~$ curl 127.0.0.1:8080

.. prompt:: text

     FoundriesFactory

The ``docker run`` command can accept other parameters.
For example,
the ``--env`` parameter which specifies an environment variable to the container. 
Remove the previous image and launch it again with: ``--env MSG=MyFirstContainer``

Test the new change with curl:

.. prompt:: bash host:~$, auto

    host:~$ docker stop shellhttpd
    host:~$ docker rm shellhttpd
    host:~$ docker run --env MSG=MyFirstContainer --name shellhttpd -d -p 8080:8080 shellhttpd:1.0
    host:~$ curl 127.0.0.1:8080

.. prompt:: text

     MyFirstContainer

Use ``docker exec`` to echo the MSG variable inside the container:

.. prompt:: bash host:~$, auto

    host:~$ docker exec -it shellhttpd sh
     
**Inside the Container**:

.. prompt:: bash docker:~$, auto

     docker:~$ echo $MSG
      MyFirstContainer
     docker:~$ exit

Remove the container:

.. prompt:: bash host:~$, auto

    host:~$ docker stop shellhttpd
    host:~$ docker rm shellhttpd

All these commands are important in understanding how Docker containers work. 
Next we explore how ``docker-compose`` works.
