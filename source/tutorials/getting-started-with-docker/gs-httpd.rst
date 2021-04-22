httpd.sh
^^^^^^^^

As mentioned above, ``Dockerfile`` will copy the ``httpd.sh`` file to your Docker image. 
Move the file from ``shellhttpd.disabled`` to the ``shellhttpd`` folder:

.. prompt:: bash host:~$

    mv ../shellhttpd.disabled/httpd.sh .

Check the content of your ``httpd.sh``:

.. prompt:: bash host:~$, auto

    host:~$ cat httpd.sh

**httpd.sh**:

.. prompt:: text

     #!/bin/sh -e
     
     PORT="${PORT-8080}"
     MSG="${MSG-OK}"
     
     RESPONSE="HTTP/1.1 200 OK\r\n\r\n${MSG}\r\n"
     
     while true; do
      echo -en "$RESPONSE" | nc -l -p "${PORT}" || true
      echo "= $(date) ============================="
     done

This is a shell script file that will respond to a request on the port defined by the 
PORT environment variable (defaults to ``8080``) with the message defined by the MSG 
environment variable (defaults to ``OK``).