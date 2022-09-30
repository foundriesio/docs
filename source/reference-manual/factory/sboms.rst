Software Bill of Materials
==========================

A Software Bill of Materials(SBOM) declares the list of software packages used to build a Target.
SBOMs are the basic building block to understanding:

 * Inventory management - What packages a Target use.
 * License compliance - What software licenses does a Target use.
 * Vulnerability management - What package versions does a Target use.

The FoundriesFactory SBOM feature allows users to extract SBOM data and analyze it according to their needs.

Background
----------

FoundriesFactory CI builds have a unique position to build up SBOMS whenever a change is built in the Factory.
There are two types of builds that SBOMs are generated for:

 * Yocto builds produce `Software Package Data Exchange`_ (SPDX) artifacts using built-in tooling.
 * Container builds produce SDPX artifacts using Syft_.

Both builds store artifacts under an ``sboms`` directory.
These files can be downloaded directly from the web UI when viewing a Target.
Yocto builds a comprehensive SPDX per image type.
For example, ``lmp-factory-image-intel-corei7-64.spdx.tar.zst``.
This archive format includes an SPDX file for every package included in the build.
Container builds produce an SPDX file per container/architecture such as ``hub.foundries.io/<FACTORY>/shellhttpd/arm64.sdpx.json``.

All this information can be accessed in its raw form by clicking around
CI builds.
However, APIs have been built to allow tooling like fioctl to more easily work with Factory SBOMs.

Working With SBOMs
------------------

Like most Factory concepts, SBOMs revolve around :ref:`Targets <tutorial-what-is-a-target>`.
You can find out what SBOMs a Target is built on by running:

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

There's several things to note about this example:

 * This Target was derived from container build 222 and Yocto build 262.
 * The Yocto build has 3 different SBOMs you can view.
   The two most important are probably, ``initramfs-...`` and ``lmp-factory-image-...``.
   In this case, the former is the packages used at runtime while the latter is a list of packages required to boot the system.
 * The container build produced several containers for two architectures.
   In this case, the platform is Intel, so the aarch64 builds are probably experimental/debug and not running in production.

   * Two containers, nginx and alpine, come from a hub.docker.io.
   * shellhttpd comes from the factory, hub.foundries.io.

With this overview, you can then drill down into each SBOM to get more details::

   $ fioctl targets show sboms 262 222/build-aarch64 alpine:latest/arm64.spdx.json
   PACKAGE                 VERSION      LICENSE
   -------                 -------      -------
   alpine-baselayout       3.2.0-r20    GPL-2.0-only
   alpine-baselayout-data  3.2.0-r20    GPL-2.0-only
   alpine-keys             2.4-r1       MIT
   ...

Going Further
-------------

There is an ever growing landscape of vendors building solutions for SBOMs.
The solutions tend to work with two competing SBOM formats:

 * SPDX_
 * CycloneDX_

In addition, many people just want to export their SBOM data into spreadsheets for quick, custom processing.
While the native storage format for Factory SBOMs is SPDX, the Foundries.io API provides a best-effort conversion to both CycloneDX and CSV.
This allows users to export data from their Factory and into their tool of choice.

Viewing an SBOM in a given format can be done with::

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
