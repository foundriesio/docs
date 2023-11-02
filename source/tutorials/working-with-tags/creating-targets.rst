Creating Targets
^^^^^^^^^^^^^^^^

Let's simulate  regular development on the branch ``devel``.
Recall that as you commit changes, it generates Targets tagged with ``devel``. 
Then all devices following the ``devel`` tag receive updates.

Imagine that—while you  will keep developing on ``devel`` —you want to decide which 
Target your devices tagged with ``tutorial`` will receive.

.. hint::
   On the previous page we tagged the latest ``devel`` Target with the additional tag, ``tutorial``.

Now to change the ``shellhttpd`` application to create new Target.

Edit ``docker-compose.yml``:

.. prompt:: bash host:~$, auto

    host:~$ vi shellhttpd/docker-compose.yml

.. prompt:: text

     version: '3.2'
     
     services:
       httpd:
         image: hub.foundries.io/cavel/shellhttpd:latest
         restart: always
         ports:
           - 8080:${PORT-8080}
         environment:
           MSG: "This is the TEST 02"

Note that ``MSG`` is defined with ``This is the TEST 02``.

Commit and push the changes:

.. prompt:: bash host:~$, auto

    host:~$ git status
    host:~$ git add shellhttpd/docker-compose.yml
    host:~$ git commit -m "This is the TEST 02"
    host:~$ git push

Go to https://app.foundries.io, select your Factory and click on :guilabel:`Targets`:

The latest Target named :guilabel:`containers-devel` should be the CI job you just created.

Wait until it finishes and change your application again.

Edit ``docker-compose.yml``:

.. prompt:: bash host:~$, auto

    host:~$ vi shellhttpd/docker-compose.yml

.. prompt:: text

     version: '3.2'
     
     services:
       httpd:
         image: hub.foundries.io/cavel/shellhttpd:latest
         restart: always
         ports:
           - 8080:${PORT-8080}
         environment:
           MSG: "This is the TEST 03"

Note that ``MSG`` is defined with ``This is the TEST 03``.

Commit and push the changes:

.. prompt:: bash host:~$, auto

    host:~$ git status
    host:~$ git add shellhttpd/docker-compose.yml
    host:~$ git commit -m "This is the TEST 03"
    host:~$ git push

Keep watching your jobs on https://app.foundries.io and once it finishes, change your application one more time.

``docker-compose.yml``:

.. prompt:: bash host:~$, auto

    host:~$ vi shellhttpd/docker-compose.yml

**shellhttpd/docker-compose.yml**:

.. prompt:: text

     version: '3.2'
     
     services:
       httpd:
         image: hub.foundries.io/cavel/shellhttpd:latest
         restart: always
         ports:
           - 8080:${PORT-8080}
         environment:
           MSG: "This is the TEST 04"

Note that ``MSG`` is defined with ``This is the TEST 04``.

Commit and push the changes:

.. prompt:: bash host:~$, auto

    host:~$ git status
    host:~$ git add shellhttpd/docker-compose.yml
    host:~$ git commit -m "This is the TEST 04"
    host:~$ git push

Finally, you should have three new versions in the Targets version list.

.. note::

  Because your device is now following ``tutorial``, it should not receive updates.
