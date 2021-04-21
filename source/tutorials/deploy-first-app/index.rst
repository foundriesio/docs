.. _tutorial-deploy-first-app:

Deploying your first Application
================================

In the previous tutorial ":ref:`tutorial-gs-with-docker`", you created your first 
application locally. This provided a brief overview of Docker containers and 
docker-compose apps. In this tutorial, you will learn how to commit and push 
your application to the server as well as configure your device with desired 
applications.

.. note::

  Tutorial Estimated Time: 20 minutes

.. _tutorial-deploy-first-app-prerequisite:

Learning Objectives
-------------------

- Commit and send your changes to your Factory’s container repository.
- Use our dashboard at https://app.foundries.io/ to find your build and follow the build logs.
- Configure your device with specific applications.
- Watch the over-the-air update.
- Test the running application.

Prerequisites and Prework
-------------------------

- Completed the :ref:`tutorial-gs-with-docker` tutorial.
- Completed the :ref:`gs-install-fioctl` section.
- Completed the :ref:`gs-flash-device` section.
- Completed the :ref:`gs-register` section.

Instructions
------------

Configure your device
^^^^^^^^^^^^^^^^^^^^^

At this point, your device should be registered to your Factory according to 
the :ref:`Getting Started guide <gs-register>`. Once your device is registered, two applications start to 
communicate with your Factory: ``aktualizr-lite`` and ``fioconfig``.

**aktualizr-lite**:

This is the daemon responsible for the updates. It checks for new updates and 
implements `The Update Protocol (TUF) <TUF_>`_ to guarantee the integrity of the platform 
and the container updates. 

**fioconfig**:

This is the daemon responsible for managing configuration data for your device. 
The data content used by ``fioconfig`` is encrypted with the device’s public key. 
The device can then get the configuration and use its private key to decrypt. 
``fioconfig`` also stores the encrypted file and extracts it to the userspace.

Both applications are configured to communicate with your Factory every 5 minutes. 
That being said, an update could take from 5 minutes to 10 minutes to be triggered. 
This can be configured according to your product needs.

To improve your experience during this tutorial, you will configure both 
``aktualizr-lite`` and ``fioconfig`` to check every minute.

This configuration will apply just to the device you run the commands below. 
To change it to your entire fleet permanently you have to customize your image.

In your device, create the folder and the file to configure ``aktualizr-lite``:

.. prompt:: bash device:~$

    sudo mkdir -p /etc/sota/conf.d/
    sudo bash -c 'printf "[uptane]\npolling_sec = 60" > /etc/sota/conf.d/z-01-polling.toml'

Create the file to configure ``fioconfig``:

.. prompt:: bash device:~$

    sudo bash -c 'printf "DAEMON_INTERVAL=60" > /etc/default/fioconfig'

Restart both services:

.. prompt:: bash device:~$

    sudo systemctl restart aktualizr-lite
    sudo systemctl restart fioconfig


Commit and Push our changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. tip::

   In the following instruction, you will commit and push your changes. It will trigger 
   a new build in the server and your device will receive a container update.

   To watch the ``aktualizr-lite`` logs and see the updates, leave your 
   device terminal running the command:

   .. prompt:: bash device:~$

       sudo journalctl -f -u aktualizr-lite

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

Find your build
^^^^^^^^^^^^^^^

Remember that in the previous tutorial, you cloned the ``devel`` branch. 
Right after the push, our CI will automatically trigger a new ``container-devel`` build.
Go to https://app.foundries.io, select your Factory and click on :guilabel:`Targets`:

The last **Target** named :guilabel:`containers-devel` should be the CI job you just created.

.. figure:: /_static/tutorials/deploy-first-app/tutorial-find-build.png
   :width: 900
   :align: center

   FoundriesFactory Targets

Click on it and if you are checking it right after the ``git push``, you might 
be able to see the CI jobs on :guilabel:`queued` and/or :guilabel:`building` status.

Your FoundriesFactory is configured by default to build your container for 
``arm32``, ``arm64``, and ``x86``. If you select the :guilabel:`+` signal in a 
:guilabel:`building` architecture you will be able to see the live build log:

.. figure:: /_static/tutorials/deploy-first-app/tutorial-containers.png
   :width: 900
   :align: center

   containers-devel

A live log example:

.. figure:: /_static/tutorials/deploy-first-app/tutorial-logs.png
   :width: 900
   :align: center

   Containers build log

When the CI finishes the three different architecture builds, it will launch a 
final job to publish your images and after some time you will see all the 
builds as :guilabel:`passed`:

.. figure:: /_static/tutorials/deploy-first-app/tutorial-finish.png
   :width: 900
   :align: center

   Containers build log

If you reload the :guilabel:`Target` page, it will indicate a new :guilabel:`Apps` available:

.. figure:: /_static/tutorials/deploy-first-app/tutorial-tag.png
   :width: 900
   :align: center

   Apps available

Debugging your device
^^^^^^^^^^^^^^^^^^^^^

At this moment, if your container build is finished your device will 
automatically install the ``shellhttpd`` container. If you let the terminal logging 
the ``aktualizr-lite`` log, you should have seen the log below:

**aktualizr-lite receiving update**:

.. prompt:: text

     aktualizr-lite[827]: Active Target: raspberrypi3-64-lmp-2, sha256: 3abd308ea6d4caffcdf250c7170e0dc9c8ff9082c64538bf14ca07c2df1beeff
     aktualizr-lite[827]: Checking for a new Target...
     aktualizr-lite[827]: Image repo Snapshot verification failed: Snapshot metadata hash verification failed
     aktualizr-lite[827]: Signature verification for Image repo Targets metadata failed
     aktualizr-lite[827]: Image repo Target verification failed: Hash metadata mismatch
     aktualizr-lite[827]: Latest Target: raspberrypi3-64-lmp-4
     aktualizr-lite[827]: Updating Active Target: 2        sha256:3abd308ea6d4caffcdf250c7170e0dc9c8ff9082c64538bf14ca07c2df1beeff
     aktualizr-lite[827]: To New Target: 4        sha256:3abd308ea6d4caffcdf250c7170e0dc9c8ff9082c64538bf14ca07c2df1beeff
     aktualizr-lite[827]:         Docker Compose Apps:
     aktualizr-lite[827]:         on: shellhttpd -> hub.foundries.io/cavel/shellhttpd@sha256:3ce57a22faa2484ce602c86f522b72b1b105ce85a14fc5b2a9a12eb12de4ec7f
     aktualizr-lite[827]: Checking for Apps to be installed or updated...
     aktualizr-lite[827]: shellhttpd will be installed
     aktualizr-lite[827]: Found 1 Apps to update
     aktualizr-lite[827]: Fetching shellhttpd -> hub.foundries.io/cavel/shellhttpd@sha256:3ce57a22faa2484ce602c86f522b72b1b105ce85a14fc5b2a9a12eb12de4ec7f
     aktualizr-lite[827]: Validating compose file
     aktualizr-lite[1086]: services:
     aktualizr-lite[1086]:   httpd:
     aktualizr-lite[1086]:     environment:
     aktualizr-lite[1086]:       MSG: Hello world
     aktualizr-lite[1086]:     image: hub.foundries.io/cavel/shellhttpd@sha256:2a302d6dbf48110e0c24389939d2aee4ade7660caced27a48cd50bc1ffdf7e7b
     aktualizr-lite[1086]:     labels:
     aktualizr-lite[1086]:       io.compose-spec.config-hash: 6d551c471b0c5755a108b213a6396e297016e77bd2d5da2c572a4430c44c748e
     aktualizr-lite[1086]:     ports:
     aktualizr-lite[1086]:     - published: 8080
     aktualizr-lite[1086]:       target: 8080
     aktualizr-lite[1086]:     restart: always
     aktualizr-lite[1086]: version: '3.2'
     aktualizr-lite[827]: Pulling containers
     aktualizr-lite[1089]: Pulling httpd (hub.foundries.io/cavel/shellhttpd@sha256:2a302d6dbf48110e0c24389939d2aee4ade7660caced27a48cd50bc1ffdf7e7b)...
     aktualizr-lite[1089]: hub.foundries.io/cavel/shellhttpd@sha256:2a302d6dbf48110e0c24389939d2aee4ade7660caced27a48cd50bc1ffdf7e7b: Pulling from cavel/shellhttpd
     aktualizr-lite[1089]: Digest: sha256:2a302d6dbf48110e0c24389939d2aee4ade7660caced27a48cd50bc1ffdf7e7b
     aktualizr-lite[1089]: Status: Downloaded newer image for hub.foundries.io/cavel/shellhttpd@sha256:2a302d6dbf48110e0c24389939d2aee4ade7660caced27a48cd50bc1ffdf7e7b
     aktualizr-lite[827]: Acquiring lock
     aktualizr-lite[827]: Installing package using ostree+compose_apps package manager
     aktualizr-lite[827]: Target 3abd308ea6d4caffcdf250c7170e0dc9c8ff9082c64538bf14ca07c2df1beeff is same as current
     aktualizr-lite[827]: Installing shellhttpd -> hub.foundries.io/cavel/shellhttpd@sha256:3ce57a22faa2484ce602c86f522b72b1b105ce85a14fc5b2a9a12eb12de4ec7f
     aktualizr-lite[1129]: Creating network "shellhttpd_default" with the default driver
     aktualizr-lite[1129]: Creating shellhttpd_httpd_1 ...
     aktualizr-lite[1129]: [50B blob data]
     aktualizr-lite[827]: Pruning unused docker images
     aktualizr-lite[1298]: Total reclaimed space: 0B
     aktualizr-lite[827]: Update complete. No reboot needed
     aktualizr-lite[827]: Active Target: raspberrypi3-64-lmp-4, sha256: 3abd308ea6d4caffcdf250c7170e0dc9c8ff9082c64538bf14ca07c2df1beeff
     aktualizr-lite[827]: Checking for a new Target...
     aktualizr-lite[827]: Latest Target: raspberrypi3-64-lmp-4
     aktualizr-lite[827]: Checking Active Target status...
     aktualizr-lite[827]: Device is up-to-date


``aktualizr-lite`` is always checking for the latest **Target**. The log above is 
an example of an ``aktualizr-lite`` launching a new application.

Still in the device, check all the containers running:

.. prompt:: bash device:~$, auto

    device:~$ docker ps -a

**Example Output**:

.. prompt:: text

     CONTAINER ID   IMAGE                                  COMMAND                  CREATED       STATUS       PORTS                    NAMES
     48f467ea2461   hub.foundries.io/tutorial/shellhttpd   "/usr/local/bin/http…"   6 hours ago   Up 6 hours   0.0.0.0:8080->8080/tcp   shellhttpd_httpd_1

Testing Container
^^^^^^^^^^^^^^^^^
On your device, ``curl`` is not available, instead run ``wget`` as following to 
test the container:

.. prompt:: bash device:~$, auto

    device:~$ wget -qO- 127.0.0.1:8080

**Example Output**:

.. prompt:: text

     Hello world

You can also test the container from an external device connected to the same 
network. For example, your host machine, the same computer you access your device over ssh.
Run the curl command with the device IP address:

.. prompt:: bash host:~$, auto

    host:~$ #Example curl 192.168.15.11:8080
    host:~$ curl <device IP>:8080

**Example Output**:

.. prompt:: text

     Hello world

What is a Target?
^^^^^^^^^^^^^^^^^

At this point, the CI has created your first **Target** triggered by your changes in the ``containers.git``.

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

.. note::

   Read the blog, `What is a Target?
   <https://foundries.io/insights/blog/2020/05/14/whats-a-target/>`_ 
   but don't worry about the instructions. We will replicate them 
   for your Factory here.

To help you understand What is a **Target**, the instructions below will guide you 
through a similar idea to the blog.

Start taking a high-level look at your fleet:

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

``fioctl status`` will list all devices connected to your Factory and what tag they are following.

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

Enabling Specific Application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Your device should be configured to always download the latest version of a 
specific ``tag``.

By default, devices will run all applications that are defined in the ``containers.git`` 
repository and therefore available in the latest **Target**. This behavior can be changed 
by enabling only specific applications. We will cover this in more detail a little later.

To check your device configuration, you can click on the tab :guilabel:`devices` 
on your Factory and find the column :guilabel:`TAGS:`

.. figure:: /_static/tutorials/deploy-first-app/tutorial-device.png
   :width: 900
   :align: center

   Device List

You used ``fioctl`` to read information about your Factory; however, it can also 
be used to read and configure your device and Factory, your fleet, WireGuard, and so on.

For example, you can see the same information about your device from the UI (User Interface) with 
``fioctl`` by running the command below:

.. prompt:: bash host:~$, auto

    host:~$ fioctl device show <device-name>

**Example Output**:

.. prompt:: text

     UUID:		a06b0bab-38be-409b-b7f8-f1125231a91e
     Owner:		6025791fd93b37d33e03b349
     Factory:	cavel
     Up to date:	true
     Target:		raspberrypi3-64-lmp-4 / sha256(3abd308ea6d4caffcdf250c7170e0dc9c8ff9082c64538bf14ca07c2df1beeff)
     Ostree Hash:	3abd308ea6d4caffcdf250c7170e0dc9c8ff9082c64538bf14ca07c2df1beeff
     Created:	2021-04-20T20:54:37+00:00
     Last Seen:	2021-04-20T22:42:53+00:00
     Tags:		devel
     Docker Apps:	shellhttpd
     Network Info:
	     Hostname:	raspberrypi3-64
	     IP:		192.168.15.11
	     MAC:		b8:27:eb:07:42:04
     Hardware Info: (hidden, use --hwinfo)
     Aktualizr config: (hidden, use --aktoml)
     Active Config:
	     Created At:    2021-04-20T20:54:39
	     Applied At:    2021-04-20T20:54:39
	     Change Reason: Set Wireguard pubkey from fioconfig
	     Files:
		     wireguard-client
		      | enabled=0
		      | 
		      | pubkey=dy7jqKcyU3HZHG4sMVO77pafa93lGEEe1atS4v0adng=
     
     -----BEGIN PUBLIC KEY-----
     MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEXQbnokyT1q5Ve+AECntNTS9D560Z
     yx6kgczb3QNAEe/imtGemFvVsir/qxRPVODVdXSlf2doAJ21cv0VL1M++g==
     -----END PUBLIC KEY-----

As expected, the device is configured to follow the ``devel`` tag. Based on that, 
it found and updated to the latest ``devel``, which is version 4.
Because you didn't specify what application it should run, it automatically loads 
all applications available in the current **Target**. In this case, ``shellhttpd``.

Enabling Specific Applications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As you implement more applications to your ``containers.git``, you might not 
want to run all the applications available on ``containers.git`` to your devices. 
The solution for that is to specify what application the device should run.

Instead of enabling the ``shellhttpd``, which is already done as mentioned before. 
Let's disable and enable it again but before, make sure your device is following the ``aktualizr-lite`` logs with the command:

.. prompt:: bash device:~$

     sudo journalctl -f -u aktualizr-lite

On your host machine, disable the ``shellhttpd`` by replacing the list of app with a simple comma:

.. prompt:: bash host:~$, auto

    host:~$ fioctl devices config updates --compose-apps --apps , <device-name>

**Example Output**:

.. prompt:: text

     Changing apps from: [shellhttpd] -> []
     Changing packagemanager to ostree+compose_apps

In a maximum of 2 minutes, you should see the ``aktualizr-lite`` log removing the application.

Once ``aktualizr-lite`` finished its changes, use ``docker ps`` to see if there is any container running in the device:

.. prompt:: bash device:~$, auto

    device:~$ docker ps -a

**Example Output**:

.. prompt:: text

     CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

Open the ``aktualizr-lite`` log again to follow the log when you enable an application:

.. prompt:: bash device:~$

     sudo journalctl -f -u aktualizr-lite

Enable the ``shellhttpd`` application on your device:

.. prompt:: bash host:~$, auto

    host:~$ fioctl devices config updates --compose-apps --apps shellhttpd <device-name>

**Example Output**:

.. prompt:: text

     Changing apps from: [] -> [shellhttpd]
     Changing packagemanager to ostree+compose_apps

Again in a maximum of 2 minutes, you should see the aktualizr-lite log adding the application.

Test the container again, on your device, running the following command:

.. prompt:: bash device:~$, auto

    device:~$ wget -qO- 127.0.0.1:8080

Check the running containers:

.. prompt:: bash device:~$, auto

    device:~$ docker ps

**Example Output**:

.. prompt:: text

     CONTAINER ID   IMAGE                               COMMAND                  CREATED       STATUS       PORTS                    NAMES
     72a3d00dbc1c   hub.foundries.io/cavel/shellhttpd   "/usr/local/bin/http…"   2 hours ago   Up 2 hours   0.0.0.0:8080->8080/tcp   shellhttpd_httpd_1

Conclusion
----------
This tutorial shows you the daily commands to use during development with 
FoundriesFactory. Together with the previous tutorial on How to get started with 
docker, you will be able to keep developing your application, try it locally, send 
your changes to the CI and receive your updates over-the-air.

.. _TUF: https://theupdateframework.com/