.. _ref-lmp-testplan:


Test Plan
#########

What to Test
============

In the context of this test plan ``mandatory`` means
the testing must be performed to release the software.
Moreover all tests must pass before the release is announced.
``Optional`` means that the tests may be performed if the time allows.
If ``optional`` test results are missing release can be announced.

Testing must focus on the mandatory features of the FoundriesFactory image:

 * Linux Microplatform
 * Base OS running with OSTree based root filesystem
 * Aktualizr-lite daemon
 * Docker engine running docker compose apps
 * Fioconfig

Remaining elements of the system may be tested as optional
but are not as important.
For example, testing of various I/O interfaces can be done case-by-case
depending on the customer requirements and hardware capabilities

A complete test list for all devices can be found in the `qa-tools git
repository`_.

Most of the test are stored in the `test-definitions repository`_.

LmP test plan
-------------

Linux microplatform testing must at least cover:

 * Boot testing

     * Ensure kernel boots and mounts root filesystem

 * Network testing

     * Ensure that networking works correctly
     * Ensure NetworkManager works correctly
       (as it’s a part of default OS installation)

 * Mandatory services testing

     * Ensure that systemd runs and all mandatory services are started
       as required.

         * Ensure that aktualizr daemon runs
         * Ensure that fioconfig daemon runs
         * Ensure that NetworkManager runs

     * Ensure that docker engine runs
     * Ensure that example docker app runs

OS features
-----------

Boot test and smoke test
~~~~~~~~~~~~~~~~~~~~~~~~

 * Mandatory:

     * Check kernel version
     * Check block devices
     * Check network devices
     * Ping test
     * Optee test - xtest (binaries built into the OS image)
     * Timesyncd

         * Ensure NTP is synchronized correctly

 * Optional

     * Check device presence (i2c, spi, video, audio, gpio, …)
       depending on HW capabilities
     * Check driver presence

OSTree
~~~~~~

 * Optional

   OSTree has a runtime test suite. It’s used for validating after
   building libostree but it probably can also be used to test the
   live system. This might be destructive to the FS though.

Docker
~~~~~~

 * Mandatory

     * Docker smoke test
       This includes running example docker containers (hello-world)

 * Optional

     * Docker-compose integration test
     * Docker networking

        * Default bridge
        * User-defined bridge
        * Host

Networking on host
~~~~~~~~~~~~~~~~~~

 * Mandatory

    * DHCP

       * Check if IPv4 address is assigned properly
       * Check if IPv6 address is assigned properly
       * Check for
         wired
         and wireless interfaces
         (requires external hardware)

    * DNS

       * Check if name resolution works with default settings
         (default DNS must be validated before running tests)

Interface testing (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Various interfaces are tested depending on the hardware and customer
requirements. Current plan is to execute the following tests:

 * HDMI (HDMI capture device)

Device update
-------------

Aktualizr (OTA API)
~~~~~~~~~~~~~~~~~~~

 * Mandatory

    * Update

        * Update of docker compose apps (new target)

           * From previous target

        * Update of base OS

           * From previous ‘platform’ target
           * From previous release ‘platform’ target

    * Rollback

        * Rollback of base OS

Device config (fioconfig)
~~~~~~~~~~~~~~~~~~~~~~~~~

 * Mandatory

    * Test whether factory specific configs are applied properly
    * Test whether group specific configs are applied properly
    * Test whether device specific configs are applied properly
    * Test whether both encrypted and non-encrypted configs are
      available on the device

How to test
===========

LmP tests
---------

Boot testing
~~~~~~~~~~~~

There are several kinds of tests involved.
Basic boot test should be mandatory for all subsequent tests.
If the boot test fails all other testing should be abandoned.
There are 2 scenarios for boot testing:

 * Initial provisioning

   This happens when the software is delivered to the board for the first time.
   Since the aktualizr is not yet running on the board,
   provisioning has to be done in some other way.
   It strongly depends on the hardware limitations and boot source.
   For example RaspberryPi can boot from SD card
   and it works well with available SDMux devices.
   On the other hand iMX8MM should boot from eMMC
   and requires UUU for initial flashing.
   Both of these provisioning methods are supported by LAVA.
   Therefore it is proposed to use LAVA for initial provisioning,
   boot and reboot testing in this scenario.

 * Software update (OS update)

   Booting after software update can be checked in 2 ways:
   with aktualizr-lite or container running on the board
   or with an external tool.
   When checking reboot after update testing rig needs to know:

    * When the test starts (on old target)
    * What are the starting (old)
      and ending (new) targets
      and OSTree hashes
    * When the test is finished
      (aktualizr performs update,
      system is rebooted)

Basic tests
~~~~~~~~~~~

Basic tests are executed on the target either
using the fiotest container (running commands on host)
or LAVA.
Which tool depends on the tested scenario.
We’re currently testing 2 scenarios:

 * *Manufacturing* scenario

   LAVA can execute tests in Linux shell on the target
   and parse results from the serial console.
   Tests are executed after flashing an image to the board.
   DUT always starts fresh without any previously running software.

 * *Rolling update* scenario

   ``Test-runner.py`` is a script from test-definitions repository.
   It’s able to run tests on the remote OS
   using SSH as a connection medium.
   It is used to execute tests in the ‘rolling update’ scenario.
   Test results are reported to both
   qa-reports
   and FIO backend.
   Reporting to FIO backend is done with fiotest.
   Fiotest is also responsible for
   starting a test round following an OTA update.
   Test plan executed in the “Rolling update” scenario is limited.
   Tests disabling networking
   and potentially corrupting the OS
   are disabled.

 * Docker apps update

   Testing of Docker apps update should be done
   using a container registered for aktualizr-lite callbacks.
   This way we’re as close as possible to testing production setup.

When to Test
============

A testing round is started after every merge to ``lmp-manifest``.
If the build is successful
all testing factories pull latest source from ``lmp-manifest`` project
and merge to their working branches.
Successful build in the testing factory triggers tests on the devices.
OTA update is delivered to the *rolling update* devices.
This also triggers a testing round on the new target.
For a release candidate build additional manual tests are performed.

.. _qa-tools git repository:
   https://github.com/foundriesio/qa-tools

.. _test-definitions repository:
   https://github.com/linaro/test-definitions
