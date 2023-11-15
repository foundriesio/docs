Commit and Push All New Applications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use ``git status`` within ``meta-subscriber-overrides`` to verify the changes:

.. prompt:: bash host:~$, auto

    host:~$  git status

::

    On branch main
    Your branch is up to date with 'origin/main'.
    
    Changes to be committed:
      (use "git restore --staged <file>..." to unstage)
    	new file:   recipes-support/shellhttpd/shellhttpd/httpd.sh
    	new file:   recipes-support/shellhttpd/shellhttpd/shellhttpd.service
    	new file:   recipes-support/shellhttpd/shellhttpd_0.1.bb
    	Changes not staged for commit:
    	  (use "git add <file>..." to update what will be     	committed)
    	  (use "git restore <file>..." to discard changes in working directory)
	    modified:   recipes-samples/images/lmp-factory-image.bb

Add all new files and changes:

.. prompt:: bash host:~$, auto

    host:~$ git add recipes-support/shellhttpd/shellhttpd/httpd.sh
    host:~$ git add recipes-support/shellhttpd/shellhttpd/shellhttpd.service
    host:~$ git add recipes-support/shellhttpd/shellhttpd_0.1.bb
    host:~$ git add recipes-samples/images/lmp-factory-image.bb

Commit your changes with the message:

.. prompt:: bash host:~$, auto

    host:~$ git commit -m "Adding shellhttpd recipe"

Push:

.. prompt:: bash host:~$, auto

    host:~$ git push

::

     Enumerating objects: 5, done.
     Counting objects: 100% (5/5), done.
     Delta compression using up to 16 threads
     Compressing objects: 100% (2/2), done.
     Writing objects: 100% (3/3), 299 bytes | 299.00 KiB/s,      done.
     Total 3 (delta 1), reused 0 (delta 0), pack-reused 0
     remote: Trigger CI job...
     remote: CI job started: https://ci.foundries.io/projects/cavel/lmp/builds/71/
     To https://source.foundries.io/factories/cavel/meta-subscriber-overrides.git/
     7767e6a..ccebcb5  main -> main

.. note::

   ``git push`` output will indicate the start of a new CI job.

Go to https://app.foundries.io, select your Factory and click on :guilabel:`Targets`:

The latest **Target** named :guilabel:`platform-main` should be the CI job you just created.

.. note::

   Yocto Project builds could take some time. Click on the building target and follow the live console for details.

Wait until it finishes, then move on to the next step.
