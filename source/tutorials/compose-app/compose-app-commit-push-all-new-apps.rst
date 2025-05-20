Commit and Push New Applications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use ``git status`` in the ``containers`` folder to verify the changes:

.. prompt:: bash host:~$, auto

    host:~$  git status

**Example Output**:

.. prompt:: text

    On branch main
    Your branch is up to date with 'origin/main'.
    
    Changes to be committed:
      (use "git restore --staged <file>..." to unstage)
	    new file:   flask-mqtt-nginx/docker-compose.yml
	    new file:   flask-mqtt-nginx/nginx.conf
	    new file:   flask-mqtt/Dockerfile
	    new file:   flask-mqtt/app.py
	    new file:   mosquitto/docker-compose.yml
	    new file:   shellhttpd-mqtt/Dockerfile
	    new file:   shellhttpd-mqtt/docker-compose.yml
	    new file:   shellhttpd-mqtt/httpd.sh
    
    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git restore <file>..." to discard changes in working directory)
	    modified:   flask-mqtt-nginx/docker-compose.yml
	    modified:   shellhttpd-mqtt/docker-compose.yml

Add the new files and changes:

.. prompt:: bash host:~$, auto

    host:~$ git add mosquitto shellhttpd-mqtt flask-mqtt-nginx flask-mqtt

Commit your changes with the message:

.. prompt:: bash host:~$, auto

    host:~$ git commit -m "Adding Flask, Mosquitto and shellhttpd-MQTT apps"

Push all committed modifications to the remote repository:

.. prompt:: bash host:~$, auto

    host:~$ git push

.. prompt:: text

     Enumerating objects: 15, done.
     Counting objects: 100% (15/15), done.
     Delta compression using up to 16 threads
     Compressing objects: 100% (13/13), done.
     Writing objects: 100% (14/14), 2.48 KiB | 2.48 MiB/s, done.
     Total 14 (delta 0), reused 4 (delta 0), pack-reused 0
     remote: Trigger CI job...
     remote: CI job started: https://ci.foundries.io/projects/<factory>/lmp/builds/61/
     To https://source.foundries.io/factories/<factory>/containers.git/
        f358677..72a9da5  main -> main

.. note::

   The ``git push`` output will indicate the start of a new CI job.

Go to https://app.foundries.io, select your Factory and click on :guilabel:`Targets`:

The latest **Target** named :guilabel:`containers-main` should be the CI job you just created.

Wait until it finishes to move on to the next step.

