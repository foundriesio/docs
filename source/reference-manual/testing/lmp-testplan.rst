.. _ref-lmp-testplan:


Test Plan
#########

Below you will find the test plan Foundries.io uses for FoundriesFactory®.

What To Test
============

In the context of this test plan, **mandatory** means the testing that must be performed to release the software.
Moreover, all tests must pass before the release is announced.
**Optional** means that the tests may be performed if time allows.
If optional test results are missing, release can be announced.

Testing must focus on the mandatory features of the FoundriesFactory image:

 * Linux microPlatform
 * Base OS running with OSTree based root filesystem
 * Aktualizr-lite daemon
 * Docker engine running Docker compose apps
 * Fioconfig

Remaining elements of the system may be tested as optional but are not as important.
For example, testing of various I/O interfaces can be done case-by-case depending on the customer requirements and hardware capabilities

A complete test list for all devices can be found in the `qa-tools git repository`_.
Most of the test are stored in the `test-definitions repository`_.

LmP Test Plan
-------------

Linux® microPlatform testing must at least cover:

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

     * Ensure that Docker engine runs
     * Ensure that example Docker app runs

OS Features
-----------

Boot Test and Smoke Test
~~~~~~~~~~~~~~~~~~~~~~~~

 * Mandatory:

     * Check kernel version
     * Check block devices
     * Check network devices
     * Ping test
     * Optee test — xtest (binaries built into the OS image)
     * Timesyncd

         * Ensure NTP is synchronized correctly

 * Optional

     * Check device presence (i2c, spi, video, audio, gpio, …)
       depending on HW capabilities
     * Check driver presence

OSTree
~~~~~~

 * Optional

   OSTree has a runtime test suite.
   It is used for validation after building libostree, but can potentially be used to test a live system.
   However, this may be destructive to the filesystem.

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

Networking on Host
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

Interface Testing (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Various interfaces are tested depending on the hardware and customer requirements.
Current plan is to execute the following tests:

 * HDMI (HDMI capture device)

Device Update
-------------

Aktualizr (OTA API)
~~~~~~~~~~~~~~~~~~~

 * Mandatory

    * Update

        * Update of Docker compose apps (new Target)

           * *From* previous Target

        * Update of base OS

           * From previous platform Target
           * From previous *release* platform Target

    * Rollback

        * Rollback of base OS

Device Config (Fioconfig)
~~~~~~~~~~~~~~~~~~~~~~~~~

 * Mandatory, to test whether:

    * Factory specific configs are applied properly
    * Group specific configs are applied properly
    * Device specific configs are applied properly
    * Both encrypted and non-encrypted configs are available on the device

How To Test
===========

LmP Tests
---------

Boot Testing
~~~~~~~~~~~~

There are several kinds of tests involved.
Basic boot test should be mandatory for all subsequent tests.
If the boot test fails all other testing should be abandoned.
There are 2 scenarios for boot testing:

 * Initial provisioning

   This happens when the software is delivered to the board for the first time.
   Since the aktualizr is not yet running on the board,
   provisioning has to be done in some other way.
   This is strongly dependent on hardware limitations and boot source.
   For example, RaspberryPi can boot from an SD card, and works well with available SDMux devices.
   Conversely, iMX8MM should boot from eMMC, and requires UUU for initial flashing.
   Both of these provisioning methods are supported by LAVA.
   Therefore, it is proposed to use LAVA for initial provisioning, boot, and reboot testing in this scenario.

 * Software update (OS update)

   Booting after a software update can be checked in 2 ways:
   with either aktualizr-lite or a container running on the board, or with an external tool.
   
   When checking reboot after update testing rig needs to know:

    * When the test starts (on old Target)
    * What are the starting (old) and ending (new) Targets and OSTree hashes
    * When the test is finished (aktualizr performs update, system is rebooted)

Basic Tests
~~~~~~~~~~~

Basic tests are executed on the target either using the fiotest container (running commands on host) or LAVA.
Which tool depends on the tested scenario.
We are currently testing 2 scenarios:

 * *Manufacturing* scenario

   LAVA can execute tests in Linux shell on the Target and parse results from the serial console.
   Tests are executed after flashing an image to the board.
   DUT always starts fresh without any previously running software.

 * *Rolling update* scenario

   ``Test-runner.py`` is a script from test-definitions repository.
   It is able to run tests on the remote OS using SSH as a connection medium.
   It is used to execute tests in the ‘rolling update’ scenario.
   Test results are reported to both qa-reports and FIO backend.
   Reporting to FIO backend is done with fiotest.
   Fiotest is also responsible for starting a test round following an OTA update.
   Test plan executed in the “rolling update” scenario is limited.
   Tests disabling networking and potentially corrupting the OS are disabled.

 * Docker apps update

   Testing of Docker apps update should be done using a container registered for aktualizr-lite callbacks.
   This way we are as close as possible to testing a production setup.

When To Test
============

A testing round is started after every merge to ``lmp-manifest``.
If the build is successful, all testing Factories pull the latest source from ``lmp-manifest`` and merge to their working branches.
A successful build in the testing Factory triggers tests on the devices.
OTA update is delivered to the *rolling update* devices.
This also triggers a testing round on the new Target.
For a release candidate build, additional manual tests are performed.

.. _qa-tools git repository:
   https://github.com/foundriesio/qa-tools

.. _test-definitions repository:
   https://github.com/linaro/test-definitions
