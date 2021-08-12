What is a Target?
^^^^^^^^^^^^^^^^^

FoundriesFactory CI just created your first **Target** triggered by your changes in the 
``containers.git``.

.. tip::

   A **Target** is a description of the software a device should run.

You just pushed changes to the ``devel`` branch of your ``containers.git`` repository. 
By default, your Factory is configured to automatically trigger a ``containers-devel`` 
CI job to build your container application changes.

After a successful build, a **Target** is created that:

- Combines the last successful ``containers-devel`` and ``platform-devel`` builds.
- Has a ``devel`` tag.  Your Factory is configured by default to add the ``devel`` tag to **Targets** triggered by changes to the ``devel`` branch.
- Has a Hardware ID which matches the MACHINE you selected when your Factory was created.

Last but not least, devices configured to watch a tag and Hardware ID (MACHINE) that match 
your latest **Target** will receive an update.

.. tip::

   At this point, your device should be registered to your Factory according to 
   the :ref:`Getting Started guide <gs-register>`. If your device is online, it 
   will automatically receive an update with your latest **Target**, but we will  
   cover more on that in the next tutorial.

.. note::

   Read the blog, `What is a Target?
   <https://foundries.io/insights/blog/2020/05/14/whats-a-target/>`_ 
   to get a high-level overview of **Targets**. Don't worry about the instructions.  
   We will replicate them for your Factory here.

To help you understand What a **Target** is, the instructions below will guide you 
through a similar path as the blog article.

``fioctl status`` will list all devices registered to your Factory and what tag they are 
following.

It also lists what **Target** is installed in each device.

.. prompt:: bash host:~$, auto

    host:~$ fioctl status

**Example Output**:

.. prompt:: text

     Total number of devices: 1
     
     TAG    LATEST TARGET  DEVICES  ON LATEST  ONLINE
     ---    -------------  -------  ---------  ------
     devel  4              1        1          1
     
     ## Tag: devel
	     TARGET  DEVICES  DETAILS
	     ------  -------  -------
	     4       1        `fioctl targets show 4`

Before you inspect **Target 4**, list all your targets available with the command below:

.. prompt:: bash host:~$, auto

    host:~$ fioctl targets list

**Example Output**:

.. prompt:: text

     VERSION  TAGS    APPS        HARDWARE IDs
     -------  ----    ----        ------------
     2        devel               raspberrypi3-64
     3        master              raspberrypi3-64
     4        devel   shellhttpd  raspberrypi3-64

When your Factory is created, two platform builds are launched in 
FoundriesFactory CI: ``devel`` and ``master``.

Based on the output example, they correspond to versions 2 and 3 respectively.

As you probably noticed, we suggest you start your development with the ``devel`` 
branch and install the image from ``platform-devel`` builds.

When you pushed your ``containers.git`` changes, it resulted in version 4. 
In simple terms: The new Version 4 **Target** was created by combining the latest 
container build (Version 4) + the latest platform build (Version 2).

Use this command to see a better overview of **Target 4**:

.. prompt:: bash host:~$, auto

    host:~$ fioctl targets show 4

**Example Output**:

.. prompt:: text

     Tags:	devel
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

- Is tagged with the ``devel`` tag.
- Specifies the OStree HASH corresponding to the latest ``platform-devel`` build.
- Lists all the container apps available, which in this case is just the ``shellhttpd`` app.
- Based on the MACHINE ``raspberrypi3-64``.
