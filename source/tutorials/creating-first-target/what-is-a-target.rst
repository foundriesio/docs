.. _tutorial-what-is-a-target:

Targets
^^^^^^^

The FoundriesFactory® CI created your first **Target** triggered by changes to the ``containers.git``.

.. hint::

   A **Target** is a description of the software a device should run.

You previously pushed changes to your ``containers.git`` repository. 
Your Factory automatically triggered a ``containers-main`` CI job to build these changes.

After a successful build, a **Target** is created that:

- Combines the latest successful ``containers-main`` and ``platform-main`` builds.
- Has a Hardware ID which matches the ``MACHINE`` you selected when your Factory was created.

Devices configured to watch a tag and Hardware ID (``MACHINE``) that match your latest **Target** will then receive an update.

.. note::

   At this point, your device should be registered, as covered in the :ref:`Getting Started guide <gs-register>`.
   If your device is online, it will automatically receive an update with your latest **Target**.
   The next tutorial will cover this in detail.

.. tip::

   Read the blog, `What is a Target? <https://foundries.io/insights/blog/2020/05/14/whats-a-target/>`_ 
   to get a high-level overview of **Targets**.
   No need to follow the instructions, as we will replicate them for here.

To help you understand What a **Target** is, the instructions below will guide you through working with them.

To list the devices registered to your Factory and the tag they are following, use ``fioctl status``
It also lists the **Target** they have installed .

.. prompt:: bash host:~$, auto

    host:~$ fioctl status

**Example Output**:

.. prompt:: text

     Total number of devices: 1
     
     TAG    LATEST TARGET  DEVICES  ON LATEST  ONLINE
     ---    -------------  -------  ---------  ------
     main  3              1        1          1
     
     Orphan target versions below are marked with a star (*)

     ## CI Tag: main
	        TARGET  DEVICES  INSTALLING  DETAILS
	        ------  -------  ----------  -------
	        3       1        0           `fioctl targets show 4`

Before inspecting your latest **Target**, list all the **Targets**:

.. prompt:: bash host:~$, auto

    host:~$ fioctl targets list

**Example Output**:

.. prompt:: text

     VERSION  TAGS    APPS        HARDWARE IDs
     -------  ----    ----        ------------
     1        main                raspberrypi3-64
     2        main   shellhttpd  raspberrypi3-64

When you pushed your ``containers.git`` changes, it resulted in a new version, i.e.,  Target 3. 

The new  **Target** was created by combining the latest 
container build  with the latest platform build.

Fioctl® can provide an overview of **Target**:

.. prompt:: bash host:~$, auto

    host:~$ fioctl targets show 3

**Example Output**:

.. prompt:: text

     Tags:	main
     CI:	https://ci.foundries.io/projects/<factory>/lmp/builds/4/
     Source:
	     https://source.foundries.io/factories/<factory>/lmp-manifest.git/commit/?id=fb119f5
	     https://source.foundries.io/factories/<factory>/meta-subscriber-overrides.git/commit/?id=d89efb2
	     https://source.foundries.io/factories/<factory>/containers.git/commit/?id=0bec425
     
     TARGET NAME            OSTREE HASH - SHA256
     -----------            --------------------
     raspberrypi3-64-lmp-4  3abd308ea6d4caffcdf250c7170e0dc9c8ff9082c64538bf14ca07c2df1beeff
     
     COMPOSE APP  VERSION
     -----------  -------
     shellhttpd   hub.foundries.io/<factory>/shellhttpd@sha256:3ce57a22faa2484ce602c86f522b72b1b105ce85a14fc5b2a9a12eb12de4ec7f

The example above, shows a **Target Name** named ``raspberrypi3-64-lmp-4`` that:

- Is tagged with the ``main`` tag.
- Specifies the OStree HASH corresponding to the latest ``platform-main`` build.
- Lists all the container apps available, which in this case is just the ``shellhttpd`` app.
- Based on the MACHINE ``raspberrypi3-64``.
