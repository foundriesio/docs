Tagging a Specific Version
^^^^^^^^^^^^^^^^^^^^^^^^^^

Use :term:`Fioctl` on your host machine to list all Target versions:

.. code-block:: console

    $ fioctl targets list

     VERSION  TAGS    APPS                                                   HARDWARE IDs
     -------  ----    ----                                                   ------------
     2        devel                                                                   raspberrypi4-64
     3        main                                                                  raspberrypi4-64
     4        devel            shellhttpd                                             raspberrypi4-64
     5        devel            shellhttpd                                             raspberrypi4-64
     6        devel            shellhttpd                                             raspberrypi4-64
     7        devel            shellhttpd                                             raspberrypi4-64
     8        devel            shellhttpd-mqtt,mosquitto,shellhttpd,flask-mqtt-nginx  raspberrypi4-64
     9        devel            mosquitto,shellhttpd,flask-mqtt-nginx,shellhttpd-mqtt  raspberrypi4-64
     10       devel,tutorial   mosquitto,shellhttpd,flask-mqtt-nginx,shellhttpd-mqtt  raspberrypi4-64
     11       devel            mosquitto,shellhttpd,flask-mqtt-nginx,shellhttpd-mqtt  raspberrypi4-64
     12       devel            mosquitto,shellhttpd,flask-mqtt-nginx,shellhttpd-mqtt  raspberrypi4-64
     13       devel            mosquitto,shellhttpd,flask-mqtt-nginx,shellhttpd-mqtt  raspberrypi4-64

If you have any device following a ``devel`` tag, it should be running the latest Target.
In the example above, this is version 13.

Because your device is configured to follow ``tutorial``, it should be stuck in the last version that was tagged with ``tutorial``.
In the example above, version 10.

We had just created 4 different Targets.
Each one with a different message.

Your device is currently running a version with the ``MSG``:  ``This is the TEST 01``.

Let's imagine you do not want to deploy the second version, the one with the ``MSG``: ``This is the TEST 02``.

Also, you do not want to deploy the latest version you created with the ``MSG``: ``This is the TEST 04``.

There is something special in the third change you did with the ``MSG``:``This is the TEST 03``.
You want to deploy this version.

Looking at the Target list above, you would tag version 12 with ``tutorial``.

Use Fioctl to tag version you want, making sure to use the version you want from your Factory:

.. code-block:: console

    $ fioctl targets tag --by-version -T devel,tutorial 12

     [devel tutorial]
     Changing tags of raspberrypi4-64-lmp-12 from [devel] -> [devel tutorial]
     CI URL: https://ci.foundries.io/projects/<factory>/lmp/builds/12
     # Waiting for worker with tag: amd64-partner.
     --- Status change: QUEUED -> RUNNING
     # Run sent to worker: og-partner-01
     ==  Setting up runner on worker
     ==  Steps to recreate inside simulator
     
         wget -O simulate.sh https://api.foundries.io/projects/<factory>/lmp/builds/12/runs/UpdateTargets//.simulate.sh
         # wget-ing the file may require the --header flag if the
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
       H_BUILD=12
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

Within a few minutes, your device should receive an update.

On your device, test the container:

.. code-block:: console

    device:~$ wget -qO- 127.0.0.1:8080

     This is the TEST 03
