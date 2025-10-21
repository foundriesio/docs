.. _ref-container-only-arch:

Container-Only Factories
========================

Container-only Factories provide a way for you to manage fleets of Arm64 or x86 devices that do not run the LmP.

Components
----------

1. **App Developer**: An individual or team that creates and maintains containerized applications using Docker Compose.
2. **containers.git**: The Foundries.io provided Git repository where application developers push their Docker Compose files and related resources.
3. **CI Job**: The Foundries.io provided CI job that is triggered when changes are pushed to the ``containers.git`` repository.
   This job builds the container images, packages the application, and publishes it to the Container Registry and OTA Service.
4. **Container Registry**: A storage service where built container images are stored and made available for devices to download.
5. **OTA Service**: The Over-The-Air service that manages application metadata, including available versions and update information.
   It interacts with devices to facilitate updates.
6. **Database**: A storage system used by the OTA Service to persist application metadata and device status information.
7. **Device Gateway**: A communication endpoint that devices use to check for updates and report their status.
   It acts as an intermediary between devices and the OTA Service.
8. **fioup**: The OTA update client running on the device.
   It checks for updates, downloads necessary container images from the Container Registry, and uses ``composeapp`` to manage the application lifecycle on the device.

App Creation And Publishing Flow
--------------------------------
.. mermaid::

   flowchart LR
      n1("App developer") -- push --> n2["contaners.git"]
      n2 -- trigger --> n3["CI Job"]
      n3 -- publish app and its images --> n4["Container Registry"]
      n3 -- publish metadata about app --> n5["OTA Service"]
      n5 -- store app metadata --> n6[("Database")]

1. An application developer pushes a new compose app to the ``containers.git`` repository.
2. This triggers the Foundries.io CI job that builds app's container images, packages the app, and publishes them to Container Registry.
3. The CI job also generates and publishes metadata about the built and published app to the OTA Service.
4. The OTA Service stores the app metadata in its database.

Device Update Flow
------------------
.. mermaid::

   flowchart LR
      n1("fioup<br>&lt;device&gt;") <-- check for updates<br>upload device status --> n2["Device Gateway"]
      n1 <-- fetch app blobs --> n3["Container Registry"]
      n2 <-- get list of available apps</br>persist device status --> n4["OTA Service"]

1. The ``fioup`` client on the device checks for updates by communicating with the Device Gateway.
2. If there are updates available, ``fioup`` can start updating apps to the specified version.
3. The app update involves fetching the necessary container images from the Container Registry, and then using ``composeapp`` to orchestrate the update process.
4. Once the update is complete, ``fioup`` uploads the device status back to the Device Gateway, which in turn persists this information in the OTA Service.

