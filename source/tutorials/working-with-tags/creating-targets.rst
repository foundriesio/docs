Creating Targets
^^^^^^^^^^^^^^^^

Let's simulate development in the branch ``devel``, as you change it, it 
generates **Targets** tagged with ``devel`` and all devices following ``devel`` 
receive updates.

Imagine, you will keep developing on ``devel`` but you want to decide which 
**Target** your device tagged with ``tutorial`` should update to.

The latest ``devel`` **Target** is also tagged with ``tutorial``.

Change the ``shellhttpd`` application to create new **Target**:

Edit the file ``docker-compose.yml`` according to the example below:

.. prompt:: bash host:~$, auto

    host:~$ gedit shellhttpd/docker-compose.yml

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
           MSG: "This is the TEST 02"

Note that ``MSG`` is defined with ``This is the TEST 02``.

Commit and push all changes done in the ``containers`` folder:

.. prompt:: bash host:~$, auto

    host:~$ git status
    host:~$ git add shellhttpd/docker-compose.yml
    host:~$ git commit -m "This is the TEST 02"
    host:~$ git push

Go to https://app.foundries.io, select your Factory and click on :guilabel:`Targets`:

The latest **Target** named :guilabel:`containers-devel` should be the CI job you just created.

Wait until it finishes and change your application again.

Edit the file ``docker-compose.yml`` according to the example below:

.. prompt:: bash host:~$, auto

    host:~$ gedit shellhttpd/docker-compose.yml

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
           MSG: "This is the TEST 03"

Note that ``MSG`` is defined with ``This is the TEST 03``.

Commit and push all changes done in the ``containers`` folder:

.. prompt:: bash host:~$, auto

    host:~$ git status
    host:~$ git add shellhttpd/docker-compose.yml
    host:~$ git commit -m "This is the TEST 03"
    host:~$ git push

Keep watching your jobs on https://app.foundries.io and once it finishes change 
your application one more time.

Edit the file ``docker-compose.yml`` according to the example below:

.. prompt:: bash host:~$, auto

    host:~$ gedit shellhttpd/docker-compose.yml

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

Commit and push all changes done in the ``containers`` folder:

.. prompt:: bash host:~$, auto

    host:~$ git status
    host:~$ git add shellhttpd/docker-compose.yml
    host:~$ git commit -m "This is the TEST 04"
    host:~$ git push

Finally, you should have three new versions in the **Targets** version list.

.. note::

  Because your device is now following ``tutorial``, it should not receive updates.
