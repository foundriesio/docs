FoundriesFactory_ Documentation
===============================

FoundriesFactory is a cloud service to build, test, deploy,
and maintain secure, updatable IoT and Edge products. It is used to
customize open source software projects including U-Boot, OP-TEE,
OE/Yocto Project, the Linux microPlatform™ and Docker®.

.. tip::
   If you require offline documentation,
   see the `HTML releases <https://github.com/foundriesio/docs/releases>`_ on GitHub.
   After downloading, unzip and open ``html/index.html`` with a browser.
   You may also clone and build from source.
   While HTML is the optimal way to view our docs,
   you may also download a PDF from the link in the footer.
   Note that some elements in the PDF, such as board flashing sections, do not render correctly.

.. toctree::
   :maxdepth: 2
   :caption: Getting started
   :name: sec-learn

   getting-started/signup/index
   getting-started/flash-device/index
   getting-started/register-device/index
   getting-started/install-fioctl/index
   getting-started/emulation-with-qemu/index
   getting-started/building-deploying-app/index

.. toctree::
   :maxdepth: 2
   :caption: Tutorials
   :name: sec-tutorials

   tutorials/getting-started-with-docker/getting-started-with-docker
   tutorials/creating-first-target/creating-first-target
   tutorials/deploying-first-app/deploying-first-app
   tutorials/configuring-and-sharing-volumes/configuring-and-sharing-volumes
   tutorials/compose-app/compose-app
   tutorials/customizing-the-platform/customizing-the-platform
   tutorials/working-with-tags/working-with-tags

.. toctree::
   :maxdepth: 2
   :glob:
   :caption: User Guide
   :name: sec-user-guide

   user-guide/fioctl/index
   user-guide/qemu/qemu
   user-guide/account-management/account-management
   user-guide/ip-protection/ip-protection
   user-guide/custom-ci/custom-ci
   user-guide/mirror-action/mirror-action
   user-guide/submodule/submodule
   reference-manual/remote-access/remote-access
   user-guide/foundriesio-rest-api/foundriesio-rest-api
   user-guide/containers-and-docker/index
   reference-manual/docker/private-registries
   user-guide/lmp-customization/index
   user-guide/lmp-auto-hostname/lmp-auto-hostname
   user-guide/lmp-device-auto-register/lmp-device-auto-register
   user-guide/custom-sota-client
   user-guide/offline-update/offline-update
   reference-manual/linux/linux-disk-encryption
   reference-manual/linux/factory-device-reset
   reference-manual/linux/linux-update
   reference-manual/security/secure-machines
   reference-manual/security/offline-keys
   reference-manual/security/factory-keys
   reference-manual/factory/sboms
   user-guide/el2g
   reference-manual/ota/production-targets
   user-guide/device-gateway-pki/device-gateway-pki
   user-guide/rotating-cert
   user-guide/troubleshooting/troubleshooting

.. toctree::
   :maxdepth: 2
   :caption: Reference Manual
   :name: sec-manual
  
   reference-manual/index
   reference-manual/docker/docker
   reference-manual/boards/boards
   reference-manual/factory/factory
   reference-manual/linux/linux
   reference-manual/ota/ota
   reference-manual/remote-access/remote-access
   reference-manual/security/security
   reference-manual/testing/testing

.. toctree::
   :maxdepth: 2
   :caption: Porting Guide
   :name: sec-porting-guide

   porting-guide/pg.rst

.. toctree::
   :caption: Glossary
   :name: sec-glossary

   glossary/index

.. toctree::
   :caption: Release Notes
   :name: sec-release-notes

   v94 <https://github.com/foundriesio/docs/blob/main/release-notes/rn_v94.md>
   v93 <https://github.com/foundriesio/docs/blob/main/release-notes/rn_v93.md>
   v92 <https://github.com/foundriesio/docs/blob/main/release-notes/rn_v92.md>

.. ifconfig:: todo_include_todos is True

   **Documentation-wide TODO List**
   -------------------------------------------

   (This only appears when ``todo_include_todos`` is True.)

.. todolist::
.. _FoundriesFactory: https://foundries.io
