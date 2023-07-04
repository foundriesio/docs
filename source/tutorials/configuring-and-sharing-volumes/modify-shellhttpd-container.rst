Modify Shellhttpd
^^^^^^^^^^^^^^^^^

To change the environment values on the fly without restarting the app, you will edit ``httpd.sh``.
Open a new terminal on your host and find the container folder used previously.

.. prompt:: bash host:~$, auto

    host:~$ cd containers/

Edit ``httpd.sh`` as below:

.. prompt:: bash host:~$, auto

    host:~$ gedit shellhttpd/httpd.sh

.. prompt:: shell

     #!/bin/sh -e
     
     PORT="${PORT-8080}"
     MSG="${MSG-FoundriesFactory}"
     
     while true; do
	     [ -f /home/shellhttpd/shellhttpd.conf ] && . /home/shellhttpd/shellhttpd.conf
	     echo "PORT=$PORT"
	     echo "MSG=$MSG"
	     RESPONSE="HTTP/1.1 200 OK\r\n\r\n${MSG}\r\n"
	     echo -en "$RESPONSE" | nc -w 5 -l -p "${PORT}" || true
	     echo "= $(date) ============================="
     done

The first line in the ``while`` loop will check for the file ``/home/shellhttpd/shellhttpd.conf``.
If it exists, it will load the variables specified in the file.
Then, ``echo`` will print the values of ``PORT`` and ``MSG``.
``RESPONSE`` will be redefined with the new ``MSG`` value.

Finally, ``-w 5`` configures ``nc`` to stop listening every 5 seconds. 
This allows the script to reload new variables.
