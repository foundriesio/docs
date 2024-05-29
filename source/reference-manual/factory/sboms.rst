.. _sbom:

Software Bill of Materials
==========================

A Software Bill of Materials(SBOM) declares *the list of software packages used to build a Target*.
SBOMs are foundational to understanding:

 * Inventory management—the packages a Target uses.
 * License compliance—the software licenses of the packages.
 * Vulnerability management—the package versions.

The FoundriesFactory® SBOM feature extracts the SBOM data and analyzes it according to your needs.

.. important::
   `Per our terms and conditions <https://foundries.io/company/terms/>`_:
   FoundriesFactory build SBOMs (“the SBOM data”) are provided for your use and are generated from SPDX metadata in all project source code files.
   Responsibility for open source license compliance rests with you.
   In no event shall Foundries.io Limited be liable for any claim, damages or other liability,
   whether in an action of contract, tort or other legal theory, arising from, out of, or in connection with the use of the SBOM data.

SBOMs and Builds
----------------

The FoundriesFactory CI generates SBOM artifacts whenever there a change happens in a Factory build.
This happens for two kinds of builds:

 * Yocto Project: `Software Package Data Exchange`_ (SPDX) artifacts using built-in tooling.
 * Container: produce SDPX artifacts using Syft_.

You can download them from the web UI when viewing a Target.
Both artifacts go into the ``sboms`` directory.

Yocto Project Artifacts
^^^^^^^^^^^^^^^^^^^^^^^

Yocto builds a comprehensive SPDX per image type.
For example, ``lmp-factory-image-intel-corei7-64.spdx.tar.zst``.
This includes an SPDX file for every package included in the build.

Syft Artifacts
^^^^^^^^^^^^^^

Container builds produce an SPDX file for each container/architecture.
This will look like ``hub.foundries.io/<FACTORY>/shellhttpd/arm64.sdpx.json``.

Customers may disable generating SBOMs for containers by setting the environment variable ``DISABLE_SBOM=1`` in their :ref:`ref-factory-definition`.

Working With SBOMs
------------------

While you can access SBOM information in its raw form by browsing your CI build,
APIs exist that allow Fioctl® to work with Factory SBOMs.


Like other Factory concepts, SBOMs revolve around :ref:`Targets <tutorial-what-is-a-target>`.
You can find out available SBOMs for a Target by running:

.. prompt:: bash host:~$, auto

   host:~$ fioctl targets show sboms <target name or version>

For example::

  $ fioctl targets show sboms 262
  BUILD/RUN            BOM ARTIFACT
  ---------            ------------
  262/intel-corei7-64  core-image-minimal-initramfs-intel-corei7-64.spdx.tar.zst
  262/intel-corei7-64  initramfs-ostree-lmp-image-intel-corei7-64.spdx.tar.zst
  262/intel-corei7-64  lmp-factory-image-intel-corei7-64.spdx.tar.zst
  222/build-aarch64    alpine:latest/arm64.spdx.json
  222/build-aarch64    hub.foundries.io/andy-corp/shellhttpd/arm64.sdpx.json
  222/build-aarch64    nginx:alpine/arm64.spdx.json
  222/build-amd64      alpine:latest/amd64.spdx.json
  222/build-amd64      hub.foundries.io/andy-corp/shellhttpd/amd64.sdpx.json
  222/build-amd64      nginx:alpine/amd64.spdx.json

Notice how:

 * The Target SBOMs come from container build 222 and Yocto build 262.
 * The Yocto build has 3 different SBOMs, available as ``tar.zst`` files. Two of note:
   * ``initramfs-...``; runtime packages
   * ``lmp-factory-image-...``; packages required for boot.

 * Several containers for two architectures were built.
   In this case, the platform is Intel, so the aarch64 builds are experimental or for debug and not production.

   * The  nginx and Alpine containers come from a ``hub.docker.io``.
   * The shellhttpd container comes from the Factory ``hub.foundries.io``.

You can then query each SBOM for more details::

   $ fioctl targets show sboms 262 222/build-aarch64 alpine:latest/arm64.spdx.json
   PACKAGE                 VERSION      LICENSE
   -------                 -------      -------
   alpine-baselayout       3.2.0-r20    GPL-2.0-only
   alpine-baselayout-data  3.2.0-r20    GPL-2.0-only
   alpine-keys             2.4-r1       MIT
   ...

Going Further
-------------

Vendors may provide their own solutions for SBOMs.
These tend to work with two competing SBOM formats:

 * SPDX_
 * CycloneDX_

You may want to just export their SBOM data into spreadsheets for quick, custom processing.
While the native storage format for Factory SBOMs is SPDX,
the Foundries.io™ API provides a best-effort conversion to both CycloneDX and CSV.
This allows users to export data from their Factory and into their tool of choice.

To view an SBOM in a given format::

 # View as cyclonedx
 $ fioctl targets show sboms 262 222/build-aarch64 alpine:latest/arm64.spdx.json --format cyclonedx
 {
    "bomFormat": "CycloneDX",
    "specVersion": "1.4",
    "version": 1,
 ...

You can download all SBOMs for a Target locally::

  # Download everything as SPDX:
  $ mkdir /tmp/sboms
  $ fioctl targets show sboms 262 --download /tmp/sboms

  # Dowload the aarch64 containers as cyclonedx:
  $ fioctl targets show sboms 262 222/build-aarch64 --download /tmp/sboms --format=cyclonedx

.. _Software Package Data Exchange:
   https://spdx.dev/
.. _Syft:
   https://github.com/anchore/syft
.. _SPDX:
   https://spdx.dev/
.. _CycloneDX:
   https://cyclonedx.org/
