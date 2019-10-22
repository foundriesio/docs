.. _tutorial-containers:

Docker App Store
================

The Linux microPlatform has the ability to securely deliver and orchestrate
containers using TUF_. This section will guide you through your first deployment.

Our update solution ota-lite uses the `Docker App`_ cloud native application
bundle specification for orchestrating container deployments. This is
essentially a docker-compose definition with a bit of context wrapped around
it to make the applications a bit more generic.

Creating your Docker App Store
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following guide will detail how to create your own `Docker App`_ store.

.. _TUF:
   https://theupdateframework.github.io/overview.html

.. _Docker App:
   https://github.com/docker/app/

In your factory we have provided the ``shellhttpd`` docker application for reference.

However, ``shellhttpd`` is disabled until you instruct your factory to build
the container and Docker App definition. To enable it, clone your **containers.git**
project, and make the following changes::

  git clone https://source.foundries.io/partners/<myfactory>/containers.git/
  cd containers
  git mv shellhttpd.dockerapp.disabled shellhttpd.dockerapp
  git mv shellhttpd.disabled shellhttpd
  git commit -m "enable shellhttpd docker-app"
  git push

If the git clone fails with an unable to access error then check you have a
valid token in your ``.netrc`` file. You can look at
:ref:`ref-getting-started` for instructions.

You can monitor your CI builds here:

 https://ci.foundries.io/projects/<myfactory>/lmp/

Once the container has been built, and the Docker App has been published,
your device will be presented with a new Docker App target that can be 
updated. 

To enable this new Docker App target, on the device edit the following file::

  sudo vim /var/sota/sota.toml

Under the the ``pacman`` section of the ``sota.toml`` file add the following line::

  docker_apps = "shellhttpd"

Save the file and restart the ``aktualizr-lite`` daemon to reload the configuration::

  sudo systemctl restart aktualizr-lite

Your device will begin to update, and once the update is complete, you can check the 
status of the container by running the following commands:

 docker ps -a

Then from your host machine you can access the HTTP server from a browser at:

 http://YOUR_DEVICE_IP:8080

Now that you have successfully deployed your first docker-app, you are free to
create your own containers and app definitions. Simply push them to the
**containers.git** repo and "voila"!

Importing Docker Apps
~~~~~~~~~~~~~~~~~~~~~

If you would like to import existing docker-apps into your factory (this
example uses our Community Docker App store), the process is simple.
To import our ``openthread-gateway.dockerapp`` into your factory, run
the following commands::

  git clone https://source.foundries.io/partners/<myfactory>/containers.git
  cd containers
  git remote add fio https://github.com/foundriesio/containers.git
  git remote update
  git checkout remotes/fio/master -- openthread-gateway.dockerapp
  git add openthread-gateway.dockerapp
  git commit -m "add openthread docker-app"
  git push

The above commands will checkout the docker-app definition from the community
container repository and push it into your FoundriesFactory container repository.
This will trigger a container build.  Once complete the new docker-app will be
available for use on your devices::

  sudo vim /var/sota/sota.toml

If you have followed the example above, extend the ``docker_apps`` list in the ``pacman`` section of the ``sota.toml`` file like the example below::

  docker_apps = "shellhttpd openthread-gateway"

Creating Docker Apps
~~~~~~~~~~~~~~~~~~~~

If you create a new Docker App deployment, and want it to be deployed on a
device, edit the sota.toml on that specific device like below::

 sudo vim /var/sota/sota.toml

Extend the docker_apps list like the example below::

 docker_apps = "shellhttpd, mynewapp"

Now restart the aktualizr-lite daemon to reload the configuration::

 sudo systemctl restart aktualizr-lite

Assuming that your new Docker App has been published, the device will begin to
update.
