.. _ref-compose-apps-conversion:

Converting Docker Apps to Compose Apps
======================================

Factories created before the introduction of compose apps must be converted
to use compose apps.

Enabling Compose Apps in a Factory
----------------------------------

The factory's definition file in ci-scripts needs to be updated to enable
compose apps::

  git clone https://source.foundries.io/factories/<factory>/ci-scripts

Edit ``factory-config.yml`` so that ``containers.params`` includes
``DOCKER_COMPOSE_APP: "1"``. For example::

  containers:
    params:
      DOCKER_COMPOSE_APP: "1"

Once enabled all new container.git changes will:

 * Continue to build docker apps for each .dockerapp file in the repository
 * Convert .dockerapp files into docker-compose and produce compose apps

Top-level directories containing a docker-compose.yml will be treated *only* as
a compose app.

With ``DOCKER_COMPOSE_APP=1``, all *new* devices will be configured to use
compose apps when registered using `lmp-device-register`.

Converting Existing Devices
---------------------------

Existing devices can be converted to use compose apps using fioctl::

  fioctl devices config updates --compose-apps

If the device is using persistent volume(s) relative to its installed location
then setting `compose-dir` can be used to not lose data::

  fioctl devices config updates --compose-apps --compose-dir /var/sota/docker-apps

Completing The Migration
------------------------

After all Factory devices are converted to compose apps, the .dockerapp files
in containers.git can be converted to compose app style applications. For
example::

  # shellhttpd.dockerapp
  version: 0.1.1
  name: shellhttpd
  description: Dummy shell script that runs an httpd server using netcat

  ---

  version: '3.2'

  services:
    httpd:
      image: hub.foundries.io/andy-corp/shellhttpd:latest
      restart: always
      ports:
        - 8080:${PORT}
      environment:
        MSG: "${MSG}"

  ---

  PORT: 8080
  MSG: Hello world

Can become::

  # shellhttpd/docker-compose.yml
  version: '3.2'

  services:
    httpd:
      image: hub.foundries.io/andy-corp/shellhttpd:latest
      restart: always
      ports:
        - 8080:${PORT-8080}
      environment:
        MSG: "${MSG-Hello world}"
