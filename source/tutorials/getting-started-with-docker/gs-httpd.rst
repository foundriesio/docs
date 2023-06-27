Shell Script
^^^^^^^^^^^^

The ``Dockerfile`` instructs Docker to copy the shell script ``httpd.sh`` to the Docker image. 
Move that file from ``shellhttpd.disabled`` to the ``shellhttpd`` folder:

.. prompt:: bash host:~$

    mv ../shellhttpd.disabled/httpd.sh .

Check the content of ``httpd.sh``:

.. prompt:: bash host:~$, auto

    host:~$ cat httpd.sh

**httpd.sh**:

.. prompt::

     #!/bin/sh -e
     
     PORT="${PORT-8080}"
     MSG="${MSG-OK}"
     
     RESPONSE="HTTP/1.1 200 OK\r\n\r\n${MSG}\r\n"
     
     while true; do
      echo -en "$RESPONSE" | nc -l -p "${PORT}" || true
      echo "= $(date) ============================="
     done

This script responds to a request on the port defined by ``PORT``(defaults to ``8080``) with the message defined by ``MSG``(defaults to ``OK``).
