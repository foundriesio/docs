What is a Target?
^^^^^^^^^^^^^^^^^

The CI has just created your first **Target** triggered by your changes in the ``containers.git``.

It is extremely important to understand what is a **Target**.

.. tip::

   A **Target** is a description of the software a device should run.

You just pushed changes to the branch ``devel`` of your ``containers.git`` repository. 
By default, your Factory is configured to automatically trigger a ``containers-devel`` 
CI job to build your container application changes.

After a successful build, it is created the **Target** description where:

- It’s tied together with the latest successful ``containers-devel`` and ``platform-devel``.
- It's configured by default to add the tag ``devel`` to **targets** triggered by changes in the ``devel`` branch.
- Added the Hardware ID based on what machine you have selected when created your Factory.

Last but not least, devices configured with tag and Hardware ID that matches 
with your latest **Target** will receive an update.

.. tip::

   At this point, your device should be registered to your Factory according to 
   the :ref:`Getting Started guide <gs-register>`. If your device is online, it 
   will automatically receive an update with your latest Target, but we will 
   cover more on that in the next tutorial.

.. note::

   Read the blog, `What is a Target?
   <https://foundries.io/insights/blog/2020/05/14/whats-a-target/>`_ 
   to get a high-level overview of Target. Don't worry about the instructions. 
   We will replicate them for your Factory here.

To help you understand What is a **Target**, the instructions below will guide you 
through a similar idea to the blog.

If you have an online device, ``fioctl status`` will list all devices registered 
to your Factory and what tag they are following.

It also lists what **TARGET** is installed in each device.

.. prompt:: bash host:~$, auto

    host:~$ fioctl status -f <factory_name>

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

    host:~$ fioctl targets list -f <factory_name>

**Example Output**:

.. prompt:: text

     VERSION  TAGS    APPS        HARDWARE IDs
     -------  ----    ----        ------------
     2        devel               raspberrypi3-64
     3        master              raspberrypi3-64
     4        devel   shellhttpd  raspberrypi3-64

When your Factory is created, two platform builds are launched in the CI: ``devel`` and ``master``.

Based on my output example, they correspond to versions 2 and 3 respectively.

As you probably noticed, we suggest you start your development with the ``devel`` 
branch and installed the image from the ``platform-devel``.

When you push your ``containers.git`` changes, it resulted in version 4. 
Making it simple, version 4, created a **Target** with the latest 
container build (Version 4) + the latest platform build (Version 2).

Use the command to have a better overview of **Target 4**:

.. prompt:: bash host:~$, auto

    host:~$ fioctl targets show 4 -f <factory_name>

**Example Output**:

.. prompt:: text

     Tags:	devel
     CI:	https://ci.foundries.io/projects/cavel/lmp/builds/4/
     Source:
	     https://source.foundries.io/factories/cavel/lmp-manifest.git/commit/?id=fb119f5
	     https://source.foundries.io/factories/cavel/meta-subscriber-overrides.git/commit/?id=d89efb2
	     https://source.foundries.io/factories/cavel/containers.git/commit/?id=0bec425
     
     TARGET NAME            OSTREE HASH - SHA256
     -----------            --------------------
     raspberrypi3-64-lmp-4  3abd308ea6d4caffcdf250c7170e0dc9c8ff9082c64538bf14ca07c2df1beeff
     
     COMPOSE APP  VERSION
     -----------  -------
     shellhttpd   hub.foundries.io/cavel/shellhttpd@sha256:3ce57a22faa2484ce602c86f522b72b1b105ce85a14fc5b2a9a12eb12de4ec7f

The example above, shows a **Target** named ``raspberrypi3-64-lmp-4``, it is:

- Tagged with ``devel``.
- Specifying the OStree HASH corresponding to the latest ``platform-devel`` build.
- Listing all the container apps available, which in this case is just the ``shellhttpd``.
