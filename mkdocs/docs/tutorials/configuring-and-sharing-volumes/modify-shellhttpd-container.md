# Modify shellhttpd Container

To change the environment values on the fly without restarting the
application, you have to edit the `httpd.sh` file.

Open a new terminal in your host machine and find the container folder
used in the previous tutorial.

bash host:~$, auto

host:~$ cd containers/

Edit the file `httpd.sh` according to the example below:

bash host:~$, auto

host:~$ gedit shellhttpd/httpd.sh

**shellhttpd/httpd.sh**:

text

\#!/bin/sh -e

PORT="${PORT-8080}" MSG="${MSG-FoundriesFactory}"

while true; do  
\[ -f /home/shellhttpd/shellhttpd.conf \] && .
/home/shellhttpd/shellhttpd.conf echo "PORT=$PORT" echo "MSG=$MSG"
RESPONSE="HTTP/1.1 200 OKrnrn${MSG}rn" echo -en "$RESPONSE" | nc -w 5 -l
-p "${PORT}" || true echo "= $(date) ============================="

done

The first line in the `while` loop will check for a file
`/home/shellhttpd/shellhttpd.conf` and if it exists it will load the
variables specified in the file. Then, `echo` will print the values of
`PORT` and `MSG`. `RESPONSE` will be redefined with the new `MSG` value.

Finally, `-w 5` configures `nc` to stop listening every 5 seconds. This
allows the script to reload new variables.
