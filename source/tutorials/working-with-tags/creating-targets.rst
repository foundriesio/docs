Creating Targets
^^^^^^^^^^^^^^^^

Let's simulate regular development on the branch ``devel``.
Recall that as you commit changes, it generates Targets tagged with ``devel``. 
Then all devices following the ``devel`` tag receive updates.

Imagine that—while you will keep developing on ``devel`` —you want to decide the Target your devices tagged with ``tutorial`` will receive.

.. hint::
   On the previous page we tagged the latest ``devel`` Target with the additional tag, ``tutorial``.

Now to change the ``shellhttpd`` application to create new Target.

Edit ``docker-compose.yml``:

.. code-block:: console

    $ vi shellhttpd/docker-compose.yml

.. code-block:: yaml

     version: '3.2'
     
     services:
       httpd:
         image: hub.foundries.io/<factory>/shellhttpd:latest
         restart: always
         ports:
           - 8080:${PORT-8080}
         environment:
           MSG: "Oi Mundo"

Commit and push the changes:

.. code-block:: console

    $ git status
    $ git add shellhttpd/docker-compose.yml
    $ git commit -m "Update msg"
    $ git push

Go to https://app.foundries.io, select your Factory and click on :guilabel:`Targets`:

The latest Target named :guilabel:`containers-devel` should be the CI job you created.

Wait until it finishes and change your application again.

Edit ``docker-compose.yml``:

.. code-block:: console

    $ vi shellhttpd/docker-compose.yml

.. code-block:: yaml

     version: '3.2'
     
     services:
       httpd:
         image: hub.foundries.io/<factory>/shellhttpd:latest
         restart: always
         ports:
           - 8080:${PORT-8080}
         environment:
           MSG: "Hallo Welt"

Commit and push the changes:

.. code-block:: console

    $ git status
    $ git add shellhttpd/docker-compose.yml
    $ git commit -m "Change msg again"
    $ git push

Keep watching your jobs on https://app.foundries.io and once it finishes, change your application one more time.

.. code-block:: console

    $ vi shellhttpd/docker-compose.yml

.. code-block:: yaml

     version: '3.2'
     
     services:
       httpd:
         image: hub.foundries.io/<factory>/shellhttpd:latest
         restart: always
         ports:
           - 8080:${PORT-8080}
         environment:
           MSG: "Howdy world"

Commit and push the changes:

.. code-block:: console

    $ git status
    $ git add shellhttpd/docker-compose.yml
    $ git commit -m "Update msg once again"
    $ git push

You now have three new versions in the Targets version list.

.. note::

  Because your device is now following ``tutorial``, it should not receive updates.
