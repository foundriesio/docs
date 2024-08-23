Commit and Push Changes
^^^^^^^^^^^^^^^^^^^^^^^

In :ref:`tutorial-gs-with-docker`, you moved most of the files from the ``shellhttpd.disabled`` folder to ``shellhttpd``.
You then built and tested a local version of the container.

In this chapter, you will work on the final adjustments before sending your changes to the remote repository.
This triggers the FoundriesFactory™ Platform CI to start a new build, which compiles and publishes your application to `Foundries.io™ hub <https://hub-ui.foundries.io/>`_.

Open a terminal on your host machine and navigate to the container folder used in the previous tutorial.

Edit ``shellhttpd/docker-compose.yml``, changing the image back to ``hub.foundries.io``:

.. prompt:: text

     version: '3.2'
     
     services:
       httpd:
         image: hub.foundries.io/<factory>/shellhttpd:latest
     #    image: shellhttpd:1.0
         restart: always
         ports:
           - 8080:${PORT-8080}
         environment:
           MSG: "${MSG-Hello world}"       

There should be one file left in the ``shellhttpd.disabled`` folder: ``docker-build.conf``.
Move it to the ``shellhttpd`` folder:

.. prompt:: bash host:~$, auto

    host:~$ mv shellhttpd.disabled/docker-build.conf shellhttpd/

This file adds advanced configuration for a FoundriesFactory CI build.
Without adding too much detail, one of the tasks of the FoundriesFactory CI is to execute commands after the container image is built.
These commands verify that your container functions correctly.

Check the content of ``docker-build.conf``:

.. prompt:: bash host:~$, auto

    host:~$ cat shellhttpd/docker-build.conf 

``docker-build.conf``:

.. prompt:: text

     # Allow CI loop to unit test the container by running a command inside it
     TEST_CMD="/bin/true"

``TEST_CMD`` tells the CI to run the  command ``/bin/true``.
If this command fails for some reason, it will mark the container build as failed.

Use ``git status`` to verify all the changes:

.. prompt:: bash host:~$, auto

    host:~$ git status

**Example Output**:

.. prompt:: text

     On branch main
     Your branch is up to date with 'origin/main'.
     
     Changes not staged for commit:
       (use "git add/rm <file>..." to update what will be committed)
       (use "git restore <file>..." to discard changes in working directory)
	     deleted:    shellhttpd.disabled/Dockerfile
	     deleted:    shellhttpd.disabled/docker-build.conf
	     deleted:    shellhttpd.disabled/docker-compose.yml
	     deleted:    shellhttpd.disabled/httpd.sh
     Untracked files:
       (use "git add <file>..." to include in what will be committed)
	     shellhttpd/
     no changes added to commit (use "git add" and/or "git commit -a")


Remove ``shellhttpd.disabled`` from git:

.. prompt:: bash host:~$, auto

    host:~$ git rm -r shellhttpd.disabled/

**Example Output**:

.. prompt:: text

     rm 'shellhttpd.disabled/Dockerfile'
     rm 'shellhttpd.disabled/docker-build.conf'
     rm 'shellhttpd.disabled/docker-compose.yml'
     rm 'shellhttpd.disabled/httpd.sh'

Add the ``shellhttpd`` folder:

.. prompt:: bash host:~$, auto

    host:~$ git add shellhttpd/
    
Check the status again before we commit:

.. prompt:: bash host:~$, auto

    host:~$ git status

**Example Output**:

.. prompt:: text

     On branch main
     Your branch is up to date with 'origin/main'.
     Changes to be committed:
       (use "git restore --staged <file>..." to unstage)
	     renamed:    shellhttpd.disabled/Dockerfile -> shellhttpd/Dockerfile
	     renamed:    shellhttpd.disabled/docker-build.conf -> shellhttpd/docker-build.conf
	     renamed:    shellhttpd.disabled/docker-compose.yml -> shellhttpd/docker-compose.yml
	     renamed:    shellhttpd.disabled/httpd.sh -> shellhttpd/httpd.sh

Commit your changes with a message:

.. prompt:: bash host:~$, auto

    host:~$ git commit -m "shellhttpd: add application"

Push all committed modifications to the remote repository:

.. prompt:: bash host:~$, auto

    host:~$ git push

**Example Output**:

.. prompt:: text

     Enumerating objects: 6, done.
     Counting objects: 100% (6/6), done.
     Delta compression using up to 16 threads
     Compressing objects: 100% (5/5), done.
     Writing objects: 100% (5/5), 795 bytes | 795.00 KiB/s, done.
     Total 5 (delta 0), reused 0 (delta 0), pack-reused 0
     remote: Trigger CI job...
     remote: CI job started: https://ci.foundries.io/projects/<factory>/lmp/builds/4/
     To https://source.foundries.io/factories/<factory>/containers.git
        daaca9c..d7bc382  main -> main

.. note::

   The output of ``git push`` indicates the start of a new CI job.
