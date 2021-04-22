Commit and Push our changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the preview tutorial :ref:`tutorial-gs-with-docker`, you have walked through 
most of the files inside the ``shellhttpd.disabled`` folder.

In this chapter, you will work on final adjustments to send your changes to 
the remote repository. This will trigger a new build in the CI, it will 
compile and publish your application on your `Factory hub <https://hub.foundries.io/>`_.

Open a new terminal in your host machine and find the container folder used in 
the preview tutorial.

.. prompt:: bash host:~$

     cd containers/

Edit the file ``shellhttpd/docker-compose.yml`` and change the image back 
to hub.foundries.io.

.. prompt:: bash host:~$, auto

    host:~$ gedit shellhttpd/docker-compose.yml

**docker-compose.yml**:

.. prompt:: text

     version: '3.2'
     
     services:
       httpd:
         image: hub.foundries.io/unique-name/shellhttpd:latest
     #    image: shellhttpd:1.0
         restart: always
         ports:
           - 8080:${PORT-8080}
         environment:
           MSG: "${MSG-Hello world}"       

In the folder ``shellhttpd.disabled`` there is still one file, the ``docker-build.conf``.

Move the ``docker-build.conf`` to your ``shellhttpd`` folder:

.. prompt:: bash host:~$, auto

    host:~$ mv shellhttpd.disabled/docker-build.conf shellhttpd/

This file will specify advanced configurations for your CI build. We don’t need 
to go further on it right now but just to let you know, one of the features of 
the CI is to execute commands after building the image to test the container.

Check the content of your ``docker-build.conf``:

.. prompt:: bash host:~$, auto

    host:~$ cat shellhttpd/docker-build.conf 

**docker-build.conf**:

.. prompt:: text

     # Allow CI loop to unit test the container by running a command inside it
     TEST_CMD="/bin/true"

``TEST_CMD`` tells CI to run the simple command ``/bin/true``. If this command 
fails for some reason, it will mark the container build as failed.

Use ``git status`` in the ``containers`` directory to verify all the changes you have done:

.. prompt:: bash host:~$, auto

    host:~$ git status

**Example Output**:

.. prompt:: text

     On branch devel
     Your branch is up to date with 'origin/devel'.
     
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

Remove from git the folder ``shellhttpd.disabled``: 

.. prompt:: bash host:~$, auto

    host:~$ git rm -r shellhttpd.disabled/

**Example Output**:

.. prompt:: text

     rm 'shellhttpd.disabled/Dockerfile'
     rm 'shellhttpd.disabled/docker-build.conf'
     rm 'shellhttpd.disabled/docker-compose.yml'
     rm 'shellhttpd.disabled/httpd.sh'

Add the folder ``shellhttpd``:

.. prompt:: bash host:~$, auto

    host:~$ git add shellhttpd/
    
Check the status again before we commit:

.. prompt:: bash host:~$, auto

    host:~$ git status

**Example Output**:

.. prompt:: text

     On branch devel
     Your branch is up to date with 'origin/devel'.
     Changes to be committed:
       (use "git restore --staged <file>..." to unstage)
	     renamed:    shellhttpd.disabled/Dockerfile -> shellhttpd/Dockerfile
	     renamed:    shellhttpd.disabled/docker-build.conf -> shellhttpd/docker-build.conf
	     renamed:    shellhttpd.disabled/docker-compose.yml -> shellhttpd/docker-compose.yml
	     renamed:    shellhttpd.disabled/httpd.sh -> shellhttpd/httpd.sh

Commit your changes with the message:

.. prompt:: bash host:~$, auto

    host:~$ git commit -m "shellhttpd: add application"

Push all committed modification to the remote repository:

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
     remote: CI job started: https://ci.foundries.io/projects/unique-name/lmp/builds/4/
     To https://source.foundries.io/factories/unique-name/containers.git
        daaca9c..d7bc382  devel -> devel

.. note::

   ``git push`` output will indicate the start of a new CI job.
