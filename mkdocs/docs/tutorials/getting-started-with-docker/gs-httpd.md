# httpd.sh

The `Dockerfile` will copy the `httpd.sh` file to your Docker image.
Move that file from `shellhttpd.disabled` to the `shellhttpd` folder:

bash host:~$

mv ../shellhttpd.disabled/httpd.sh .

Check the content of your `httpd.sh`:

bash host:~$, auto

host:~$ cat httpd.sh

**httpd.sh**:

text

\#!/bin/sh -e

PORT="${PORT-8080}" MSG="${MSG-OK}"

RESPONSE="HTTP/1.1 200 OKrnrn${MSG}rn"

while true; do  
echo -en "$RESPONSE" | nc -l -p "${PORT}" || true echo "= $(date)
============================="

done

This is a shell script file that will respond to a request on the port
defined by the PORT environment variable (defaults to `8080`) with the
message defined by the MSG environment variable (defaults to `OK`).
