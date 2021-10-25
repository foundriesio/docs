.. _ug-docker-vscode:

Working with Docker and VSCode
==============================

This section helps you to configure the Docker extension for the Visual Studio Code 
and use it to develop and deploy a Docker Compose Application to devices connected over ssh.

Creating, configuring and testing a Docker Compose Application are very important 
stages and they might require debugging before you make sure the application is designed as you like.
The steps below help you during that stage where you are constantly changing your 
``Dockerfile``, ``docker-compose.yml`` and application.

Prerequisites
-------------

In this guide, it is assumed you are familiar with Docker Compose Application 
and its structures.
In case you want to learn more about Docker and Docker Compose Apps, take a look 
at the **Tutorials** starting from :ref:`tutorial-gs-with-docker`.

It is also assumed that you have the software below installed on your computer:

- `Docker Desktop <https://www.docker.com/products/docker-desktop>`_
- `Visual Studio Code <https://code.visualstudio.com/>`_
- `Git <https://git-scm.com/downloads>`_

1. Create an SSH key pair as shown in this `document on GitHub. <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent>`_

2. Install the ``docker-compose`` version ``1.27.1`` using the command below:

.. prompt:: bash host:~$

    sudo curl -L "https://github.com/docker/compose/releases/download/1.27.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose


.. note::

   Several versions of ``docker-compose`` were tested and only version ``1.27.1`` 
   worked correctly, so make sure to install this version.

3. Assuming you have a device running the Linux microPlatform with the ``<device-ip>``, 
use the command below to add your ssh public key to the target:

.. prompt:: bash host:~$

    ssh-copy-id -i ~/.ssh/id_ed25519 fio@<device-ip>

**Example Output**:

.. prompt:: text

     /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "~/.ssh/id_ed25519.pub"
     
     Number of key(s) added: 1
     
Now try logging into the machine, with: "ssh 'fio@<device-ip>'" and make sure 
that only the key(s) you wanted were added.

Docker Context Setup
--------------------

The initial Docker context connects to the Desktop, in other words, if you try 
``docker run | ps | rm | etc`` it runs from your Desktop.

Check the context available with the command:

.. prompt:: bash host:~$

    docker context ls

**Example Output**:

.. prompt:: text

     docker context ls
     NAME        DESCRIPTION                               DOCKER ENDPOINT               KUBERNETES ENDPOINT   ORCHESTRATOR
     default *   Current DOCKER_HOST based configuration   unix:///var/run/docker.sock                         swarm

Create a docker context to attach to the remote device with the command below 
replacing ``<device-ip>``:

.. prompt:: bash host:~$

    docker context create device --docker "host=ssh://fio@<device-ip>"

**Example Output**:

.. prompt:: text

     device
     Successfully created context "device"

List the docker context available again:

.. prompt:: bash host:~$

    docker context ls

**Example Output**:

.. prompt:: text

     docker context ls
     NAME        DESCRIPTION                               DOCKER ENDPOINT               KUBERNETES ENDPOINT   ORCHESTRATOR
     default *   Current DOCKER_HOST based configuration   unix:///var/run/docker.sock                         swarm
     device                                                ssh://fio@<device-ip>

At this point, you can switch context to run any Docker command on the device or 
on the Desktop:

.. prompt:: bash host:~$

    docker context use device

**Example Output**:

.. prompt:: text

     device
     Current context is now "device"

.. note::

   To run Docker commands on your Desktop, you have to switch context back to 
   default: ``docker context use default``

Cloning Container Repository
----------------------------

Clone your ``containers.git`` repo and enter its directory:

.. prompt:: bash host:~$

    git clone -b devel https://source.foundries.io/factories/<factory>/containers.git
    cd containers

Your ``containers.git`` repository is initialized with a simple application 
example in ``shellhttpd.disabled``

Move the ``shellhttpd.disable`` to ``shellhttpd``.

.. prompt:: bash host:~$

    mv shellhttpd.disable shellhttpd

In case you don't have the ``shellhttpd.disable`` or the ``shellhttpd`` folder 
in your ``containers.git`` repository, create the folder with the following files:

.. prompt::

    containers/
    └── shellhttpd
        ├── docker-compose.yml
        ├── Dockerfile
        └── httpd.sh

.. prompt:: bash host:~$

    mkidir shellhttpd; cd shellhttpd

Create the ``Dockerfile``:

.. prompt:: bash host:~$, auto

    host:~$ cat Dockerfile
     
**Dockerfile**:

.. prompt:: text

     FROM alpine
     
     COPY httpd.sh /usr/local/bin/
     
     CMD ["/usr/local/bin/httpd.sh"]

Create the ``httpd.sh``:

.. prompt:: bash host:~$, auto

    host:~$ cat httpd.sh
     
**httpd.sh**:

.. prompt:: text

     #!/bin/sh -e
     
     PORT="${PORT-8080}"
     MSG="${MSG-OK}"
     
          RESPONSE="HTTP/1.1 200 OK\r\n\r\n${MSG}\r\n"
     
     while true; do
	     echo -en "$RESPONSE" | nc -l -p "${PORT}" || true
	     echo "= $(date) ============================="
     done

Create the ``docker-compose.yml`` as the example below replacing ``<factory>`` 
with your Factory name:

.. prompt:: bash host:~$, auto

    host:~$ cat docker-compose.yml
     
**docker-compose.yml**:

.. prompt:: text

     version: '3.2'
     
     services:
       httpd:
         image: hub.foundries.io/<factory>/shellhttpd:latest
         build: .
         restart: always
         ports:
           - 8080:${PORT-8080}
         environment:
           MSG: "${MSG-Hello world}"

.. note::
     In case your ``docker-compose.yml`` doesn’t contain ``build: .`` below the 
     image stanza, edit and add it like the example above.

Visual Studio Code
------------------

Start the Visual Studio Code with the command below inside the ``containers`` folder.

.. prompt:: bash host:~$, auto

    host:~$ code .

Follow the steps below to install the Docker extension in VS Code:

.. figure:: /_static/userguide/docker-vscode/install.png
   :width: 900
   :align: center

   Installing Docker extension on Visual Studio Code

- 1) Click on `Extensions`
- 2) Search for `docker`
- 3) Select the Docker extension
- 4) Install Docker extension

Now you have everything to start to build and deploy the Docker Compose Application 
on the device.

Development Workflow
--------------------

Click on `EXPLORER` to see the file tree you have on the containers folder:

.. figure:: /_static/userguide/docker-vscode/explorer.png
   :width: 900
   :align: center

   Visual Studio Code, explorer view

Right-click on the ``docker-compose.yml`` and select :guilabel:`Compose up`
to launch the ``shellhttpd`` example on your device.

.. figure:: /_static/userguide/docker-vscode/dockerup.png
   :width: 900
   :align: center

   Launching Docker Compose Application

This will trigger the build and deployment on the device. A successful launch should 
look like this in the VSCode terminal:

**VSCode Terminal**:

.. prompt:: text

     > Executing task: docker-compose -f "shellhttpd.disabled/docker-compose.yml" up -d --build <
     
     Creating network "shellhttpddisabled_default" with the default driver
     Building httpd
     Step 1/3 : FROM alpine
     latest: Pulling from library/alpine
     552d1f2373af: Pull complete
     Digest: sha256:e1c082e3d3c45cccac829840a25941e679c25d438cc8412c2fa221cf1a824e6a
     Status: Downloaded newer image for alpine:latest
      ---> bb3de5531c18
     Step 2/3 : COPY httpd.sh /usr/local/bin/
      ---> adadb7638c3f
     Step 3/3 : CMD ["/usr/local/bin/httpd.sh"]
      ---> Running in 171bef474cbb
     Removing intermediate container 171bef474cbb
      ---> 13aa72ac6cfc
     
     Successfully built 13aa72ac6cfc
     Successfully tagged hub.foundries.io/<factory>/shellhttpd:latest
     Creating shellhttpddisabled_httpd_1 ... done

     Terminal will be reused by tasks, press any key to close it.

Switch to the Docker Extension view to explore the extension functionalities:

.. figure:: /_static/userguide/docker-vscode/docker.png
   :width: 900
   :align: center

   Visual Studio Code Docker Extension View

As you can see in the image above, the extension allows you to see many pieces 
of information about Docker in the device.

The first tab :guilabel:`CONTAINERS` will display all the images running on your 
device. Note that it is also possible to see the Container Image file system.

.. figure:: /_static/userguide/docker-vscode/runningimage.png
   :width: 200
   :align: center

   Docker Image running on the Device

Right-click on the image to attach a terminal to the running container:

.. figure:: /_static/userguide/docker-vscode/terminal.png
   :width: 900
   :align: center

   Attach Terminal

.. note::
     You can proceed to test your container as described in the ``shellhttpd`` 
     tutorial: :ref:`tutorial-deploying-first-app-testing`.

Finally, to stop the application, right-click in the App and select :guilabel:`Compose Down`’:

.. figure:: /_static/userguide/docker-vscode/downapp.png
   :width: 300
   :align: center

   Stopping Application