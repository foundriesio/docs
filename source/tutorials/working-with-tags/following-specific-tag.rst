Following an Specific Tag
^^^^^^^^^^^^^^^^^^^^^^^^^

Before configuring a device to follow a specific tag, you must have at least one 
**Target** tagged with the new tag.

Let's start tagging all **Targets** in the latest version with the tag ``devel`` and ``tutorial``.

Use ``fioctl`` on your host machine to list all **Target** versions:

.. prompt:: bash host:~$, auto

    host:~$ fioctl targets list

**Example Output**:

.. prompt:: text

     VERSION  TAGS    APPS                                                   HARDWARE IDs
     -------  ----    ----                                                   ------------
     2        devel                                                          raspberrypi3-64
     3        master                                                         raspberrypi3-64
     4        devel   shellhttpd                                             raspberrypi3-64
     5        devel   shellhttpd                                             raspberrypi3-64
     6        devel   shellhttpd                                             raspberrypi3-64
     7        devel   shellhttpd                                             raspberrypi3-64
     8        devel   shellhttpd-mqtt,mosquitto,shellhttpd,flask-mqtt-nginx  raspberrypi3-64
     9        devel   mosquitto,shellhttpd,flask-mqtt-nginx,shellhttpd-mqtt  raspberrypi3-64
     10       devel   mosquitto,shellhttpd,flask-mqtt-nginx,shellhttpd-mqtt  raspberrypi3-64

Use ``fioctl`` to Tag version 10:

.. prompt:: bash host:~$, auto

    host:~$ fioctl targets tag --by-version 10 -T devel,tutorial

**Example Output**:

.. prompt:: text

     [devel tutorial]
     Changing tags of raspberrypi3-64-lmp-10 from [devel] -> [devel tutorial]
     CI URL: https://ci.foundries.io/projects/<factory>/lmp/builds/10
     # Waiting for worker with tag: amd64-partner.
     --- Status change: QUEUED -> RUNNING
     # Run sent to worker: og-partner-01
     ==  Setting up runner on worker
     ==  Steps to recreate inside simulator
     
         wget -O simulate.sh https://api.foundries.io/projects/<factory>/lmp/builds/10/runs/UpdateTargets//.simulate.sh
         # wget'ing the file may require the --header flag if the
         # jobserv API requires authentication.
         sh ./simulate.sh
     ==  Pulling container: hub.foundries.io/aktualizr
     Using default tag: latest
     latest: Pulling from aktualizr
     Digest: sha256:a89f306e297de7e9b37f30f851d345340f1aa7619e0fcb6566ee84920984de75
     Status: Image is up to date for hub.foundries.io/aktualizr:latest
     ==  Preparing bind mounts
         INFO  Creating secret: targets
         INFO  Creating secret: triggered-by
         INFO  Creating secret: osftok
         INFO  Creating secret: git.http.extraheader
         INFO  Creating volume: /srv/jobserv-worker/volumes/<factory>/lmp/bitbake
     ==  Creating container .netrc file
         INFO  Creating token for jobserv run access
     ==  Preparing script
         INFO  Repo is: https://github.com/foundriesio/ci-scripts
     Cloning into '/srv/jobserv-worker/runs/tmpsm3dnfvj/script-repo'...
         INFO  Git HEAD reference is: 9d1779efed401ddfd17e613fdc7eaa3bf10b8156
     ==  Setting up container environment
         INFO  Container environment variables:
       UPDATE_ACTION=patch
       H_PROJECT=<factory>/lmp
       H_BUILD=10
       H_RUN=UpdateTargets
       H_WORKER=og-partner-01
     ==  Running script inside container
     fetch http://dl-cdn.alpinelinux.org/alpine/v3.9/main/x86_64/APKINDEX.tar.gz
     
     --- Status change: RUNNING -> UPLOADING
     fetch http://dl-cdn.alpinelinux.org/alpine/v3.9/community/x86_64/APKINDEX.tar.gz
     (1/1) Installing curl (7.64.0-r5)
     Executing busybox-1.29.3-r10.trigger
     OK: 165 MiB in 91 packages
     == Extracting credentials
     Saved keys to /tufrepo/keys/{targets.sec, targets.pub}
     Finished init for /tufrepo using /tmp/tmp.lFIcBD
     ==  Pulling TUF targets
     Pulled targets
     ==  Updating targets
     Patching targets
     ==  Signing new targets
     signed targets.json to /tufrepo/roles/targets.json
     ==  Uploading new targets
     Pushed targets
     Script completed
     ==  Finding artifacts to upload
     Uploading 2 items 19495 bytes
     ==  Runner has completed
                 _  _
                | \/ |
             \__|____|__/
               |  o  o|           Thumbs Up
               |___\/_|_____||_
               |       _____|__|
               |      |
               |______|
               | |  | |
               | |  | |
               |_|  |_|

Use ``fioctl`` again to list all **Target** versions:

.. prompt:: bash host:~$, auto

    host:~$ fioctl targets list

**Example Output**:

.. prompt:: text

     VERSION  TAGS    APPS                                                   HARDWARE IDs
     -------  ----    ----                                                   ------------
     2        devel                                                                   raspberrypi3-64
     3        master                                                                  raspberrypi3-64
     4        devel            shellhttpd                                             raspberrypi3-64
     5        devel            shellhttpd                                             raspberrypi3-64
     6        devel            shellhttpd                                             raspberrypi3-64
     7        devel            shellhttpd                                             raspberrypi3-64
     8        devel            shellhttpd-mqtt,mosquitto,shellhttpd,flask-mqtt-nginx  raspberrypi3-64
     9        devel            mosquitto,shellhttpd,flask-mqtt-nginx,shellhttpd-mqtt  raspberrypi3-64
     10       devel,tutorial   mosquitto,shellhttpd,flask-mqtt-nginx,shellhttpd-mqtt  raspberrypi3-64

Note that version 10 is now tagged with ``devel`` and ``tutorial``.

Change the device configuration to start following the ``tutorial`` tag:

.. prompt:: bash host:~$, auto

    host:~$ fioctl devices config updates --tags tutorial <device-name>

**Example Output**:

.. prompt:: text

     Changing tags from: [] -> [tutorial]
     Changing packagemanager to ostree+compose_apps