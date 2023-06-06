.. _ug-fioctl:

Fioctl
======

This section assumes you have followed :ref:`sec-learn` to its completion. The
aim of this section is to provide you with a template for using
:ref:`ref-fioctl` by way of example.

.. _ug-fioctl-enable-apps:

Enabling/Disabling Apps
-----------------------

By default all apps defined in :term:`containers.git` for any given tag are
enabled. To change this behaviour, a list of allowed apps can be given **per
device**, enabling only those apps that are in a comma separated list.

Via Fioctl
~~~~~~~~~~

``fioctl devices config updates <device_name> --apps <app_name1>,<app_name2>``
  Set the app(s) a device will run.

**Example**

.. code-block:: console
   
   # First, list Targets and ensure app(s) are available in the latest Target.

   $ fioctl targets list -f cowboy

   # Find a device to instruct by name.

   $ fioctl devices list -f cowboy

   # Enable only the desired app(s) on the device.

   $ fioctl devices config updates cowboy-device-1 --apps netdata,shellhttpd

   # Now only the app(s) supplied in the list will run on the device.


Via lmp-device-register
~~~~~~~~~~~~~~~~~~~~~~~

When registering a device, ``lmp-device-register`` can set a list of apps to
enable.

``lmp-device-register --api-token=<token> --apps <app_name1>,<app_name2>``
  Set the app(s) a device will run, during registration.

.. _ug-fioctl-inspecting-targets:

Inspecting Targets
------------------

A Factory produces Targets whenever a
change is pushed to the :ref:`ref-factory-sources`. A Target is a description of
the software a device should run, as defined by a list of metadata which
includes an **OSTree Hash** and one or more **Docker-Compose App URIs**.

This metadata is recorded upon Target creation, making the Target an
**immutable** description of the Factory at a point in time.

:ref:`ref-fioctl` provides many methods of viewing Target metadata, which can
reveal:

* What **apps** are available inside the Target.
* What **tag** a Target has.
* What **MACHINE** a Target has been produced for **(HARDWARE ID).**
* What **git commits** caused the Target to be produced.

Target metadata can be inspected by using 3 primary commands

``fioctl targets list``
    Lists the Targets a Factory has produced so far.

      .. toggle-header::
         :header: **Click to show command output**

         .. code-block::

           $ fioctl targets list
           VERSION  TAGS    APPS                             HARDWARE IDs
           -------  ----    ----                             ------------
           1        master  simple-app,netdata               raspberrypi3-64
           2        devel   mosquitto,simple-app,netdata     raspberrypi3-64
           3        devel   simple-app,netdata,mosquitto     raspberrypi3-64

``fioctl targets list -r``
    Lists the Targets a Factory has produced in ``-r`` (raw) json format.
    This is often piped into ``jq`` in order to format the json neatly.

    The command output below has highlighted the ``docker_compose_apps`` section, which
    contains the **names of apps** that are available in this Target, as well as
    their **Docker-Compose App URIs**.

    Additionally, the **OSTree Hash** for the Target has been highlighted.

      .. toggle-header::
         :header: **Click to show command output**

         .. code-block::
            :linenos:
            :emphasize-lines: 16,37-45

              $ fioctl targets list -r | jq
              {
                "signatures": [
                  {
                    "keyid": "e682f3c903f666344ad4431d5f24c8db5941e9c2649a7aee3e589f92ef1c4a68",
                    "method": "rsassa-pss-sha256",
                    "sig": "nVQdna4yfd5AUrGya1rILOjs2x457L654ou9Ia1guRvhIPNXWNGGxWUVXLxVbKUfZj/M902V9lL3uswC5tCU/HUDfyIVDG6aKH9kCocV146NMA+htmjqX8csaKcjp5xV9/ZWAtqHgYPAhFD3e4t/qhYRaSroIdLnyPTzs0KbibmNVsEz4SfXo+OAr0RxigUfWi+O8r/0FS26drB+9D76cO8oothQgXoTD9Vg7o2YZflV62IBoJBPsnHuCUV9e4NWJvnHSE8qaCVYdwKugcAnBH+Yn+PaTmX+WwfwJ7Zi3/e+qJAQnk8LTUoNo+86zl0TyGR1DGHma0zM8XywsDaoRw=="
                  }
                ],
                "signed": {
                  "_type": "Targets",
                  "expires": "2020-11-21T02:20:20Z",
                  "targets": {
                    "raspberrypi3-64-lmp-57": {
                      "hashes": {
                        "sha256": "2d1655fb1e04e2ed39536dd96485687945ac87d6f9e7d79a01f06ec6e5d161b1"
                      },
                      "length": 0,
                      "custom": {
                        "cliUploaded": false,
                        "name": "raspberrypi3-64-lmp",
                        "version": "57",
                        "hardwareIds": [
                          "raspberrypi3-64"
                        ],
                        "targetFormat": "OSTREE",
                        "uri": "https://ci.foundries.io/projects/cowboy/lmp/builds/53",
                        "createdAt": "2020-10-21T02:20:18Z",
                        "updatedAt": "2020-10-21T02:20:18Z",
                        "lmp-manifest-sha": "f39a2e1d1f81523ce222270ed9ddb3a87ff3ca09",
                        "arch": "aarch64",
                        "image-file": "lmp-factory-image-raspberrypi3-64.wic.gz",
                        "meta-subscriber-overrides-sha": "2cd6253273fc7de5ece8a45b9ec4247bcdd0556e",
                        "tags": [
                          "devel"
                        ],
                        "docker_compose_apps": {
                          "mosquitto": {
                            "uri": "hub.foundries.io/cowboy/mosquitto@sha256:1ec9667ac7877e59d043527675f36b258d6dce33bbb9153bc8504dd20152f42a"
                          },
                          "simple-app": {
                            "uri": "hub.foundries.io/cowboy/simple-app@sha256:a123f517cf68939cb15bcfe9a77fb421b1a2f57bc23834e3e925113bf6d134a7"
                          },
                          "netdata": {
                            "uri": "hub.foundries.io/cowboy/netdata@sha256:4994cbdc80c875783442a7aa88e45258fba190093d27b127ee7a667dfc3f647e"
                          }
                        },
                        "containers-sha": "8d040d62f961289130c1f0dfc366d0ce79c2e571"
                      }
                    }

``fioctl targets show <target>``
    Prints detail about a specific Target, (e.g ``fioctl targets show 58``).

    These details include:

    * A web link to the CI build produced for this Target where to view
      the **console.log** or **download artifacts**.
    * The **hashes for each repo** in the :ref:`ref-factory-sources` at the time
      the Target was produced.
    * The **OSTree Hash** for this Target.
    * The **Docker-Compose App URI** for each available app at the time the Target
      was produced.

      .. toggle-header::
         :header: **Click to show command output**

         .. code-block::

           $ fioctl targets show 58
           Tags:	devel
           CI:	https://ci.foundries.io/projects/cowboy/lmp/builds/58/
           Source:
           	https://source.foundries.io/factories/cowboy/lmp-manifest.git/commit/?id=f39a2e1d1f81523ce222270ed9ddb3a87ff3ca09
           	https://source.foundries.io/factories/cowboy/meta-subscriber-overrides.git/commit/?id=2cd6253273fc7de5ece8a45b9ec4247bcdd0556e
           	https://source.foundries.io/factories/cowboy/containers.git/commit/?id=16ac8d1e169d07bd44ff7b01de72783a0c05d6e2

           TARGET NAME             OSTREE HASH - SHA256
           -----------             --------------------
           raspberrypi3-64-lmp-58  2d1655fb1e04e2ed39536dd96485687945ac87d6f9e7d79a01f06ec6e5d161b1

           COMPOSE APP   VERSION
           -----------   -------
           netdata       hub.foundries.io/cowboy/netdata@sha256:9fe7b87ed796025a3398e40bae4d9e3d2eef84414d9e5f4487f33e7dcb611ec7
           mosquitto     hub.foundries.io/cowboy/mosquitto@sha256:143656c7739f15da23697480f98f1dddbdffe4f16cca2e7f81f32bb7769f3d9d
           simple-app    hub.foundries.io/cowboy/simple-app@sha256:a03a03b4ca50650d5d9f171e92278a5176377c1265f764320d7b55b75d923431

.. _ug-fioctl-common-commands:

Common Commands
---------------

View Targets
  ``fioctl targets list -f <factory>``
    Lists the Targets a Factory has produced so far:

    .. code-block:: console
   
       $ fioctl targets list -f bebop
       VERSION  TAGS    APPS        HARDWARE IDs
       -------  ----    ----        ------------
       2        devel               raspberrypi3-64
       3        master              raspberrypi3-64
       4        master  shellhttpd  raspberrypi3-64
       5        master  shellhttpd  raspberrypi3-64
       6        master              raspberrypi3-64
       7        master              raspberrypi3-64
       8        master  httpd       raspberrypi3-64
       11       master  octofio     raspberrypi3-64

List devices
  ``fioctl devices list -f <factory>``
    Lists the devices that have connected to a Factory, along with associated
    metadata, such as device name, status, Target and enabled apps.

  .. code-block:: console
     
     $ fioctl devices list -f bebop                                                  
     NAME  FACTORY  OWNER           TARGET                  STATUS  APPS     UP TO DATE                                                                              
     ----  -------  -----           ------                  ------  ----     ----------                                                                              
     ein   bebop    <unconfigured>  raspberrypi3-64-lmp-49  OK      netdata  true    

Set device tag
  ``fioctl devices config updates <device_name> --tag <tag>``
    Filter the Targets a device will accept by tag. For example, to move a
    device from accepting 'devel' builds to 'master' builds. See the
    :ref:`ref-advanced-tagging` section for more examples.

  .. code-block:: console

     $ fioctl devices config updates ein --tag devel                                 
     Changing tag from: master -> devel  

Set app(s) to be enabled
  ``fioctl devices config updates <device_name> --apps <app_name1>,<app_name2>``
    Set the app(s) a device will run.
  
    .. code-block:: console

       $ fioctl devices config updates ein --apps simple-app                           
       Changing apps from: [netdata] -> [simple-app] 

Enable :ref:`ref-wireguard`
  ``fioctl devices config wireguard <device_name> <enable|disable>``
    Enable or disable the Wireguard systemd service on a LmP device. This
    requires that you configure a Factory to use an instance of Wireguard you
    have set up on your own server as described in the :ref:`ref-wireguard`
    guide.

  .. code-block::

     $ fioctl devices config wireguard ein enable                                    
     Finding a unique VPN address ... 
