Extending the Linux microPlatform
=================================

.. _ref-adding-packages-image:

Adding Packages to the Image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The **meta-subscriber-overrides.git** repo allows you to customize the
packages included in your factory image.

Add packages to the list for ``CORE_IMAGE_BASE_INSTALL`` located in
**recipes-samples/images/lmp-factory-image.bb**.

For a quick example let’s add the "stress-ng" utility package to the build.::

  git clone https://source.foundries.io/factories/<myfactory>/meta-subscriber-overrides.git
  vi meta-subscriber-overrides/recipes-samples/images/lmp-factory-image.bb

If the git clone fails with an unable to access error then check you have a
valid token in your ``.netrc`` file. You can look at
:ref:`ref-getting-started` for instructions.

Add stress to the package list.::

  vim \
  stress-ng \
  ...

Then::

  git add meta-subscriber-overrides/recipes-samples/images/lmp-factory-image.bb
  git commit -m "add stress-ng package to device image"
  git push

Go and get a coffee - your Factory is generating a new image with this package.
This will take at least half an hour (and maybe longer depending on current Factory capacity).

You can check the status at:

 https://ci.foundries.io/projects/<myfactory>/lmp/

Once completed, the device will reboot after the update is applied. This
behavior is customizable so that you can apply rules to determine when
devices should be re-started.  Once restarted the stress-ng command will
be available.

List of available recipes
~~~~~~~~~~~~~~~~~~~~~~~~~
OE provides a tool_ to search layers and recipes.

.. _tool:
   https://layers.openembedded.org/layerindex/branch/master/layers/

Creating a Python3 Package from PyPi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
There are python packages which do not yet have a recipe for python3 in OE.
If this is the case with a desired package, use this template below to add a
new package from PyPi.

Create a recipe in the **meta-subscriber-overrides.git** repository using the
following naming scheme:

  ``recipes-devtools/python/python3-<package name>_<version>.bb``

  (E.g.: recipes-devtools/python/python3-virtualenv_16.4.3.bb)

Example file contents::

  DESCRIPTION = "Virtual Python Environment builder"
  HOMEPAGE = "https://pypi.python.org/pypi/virtualenv"
  SECTION = "devel/python"
  LICENSE = "MIT"
  LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=51910050bd6ad04a50033f3e15d6ce43"

  SRC_URI[md5sum] = "5f012791118fe99990d9422cf560edf3"
  SRC_URI[sha256sum] = "984d7e607b0a5d1329425dd8845bd971b957424b5ba664729fab51ab8c11bc39"

  inherit setuptools pypi

  DEPENDS += " \
        python3-pip \
        "

  RDEPENDS_${PN} += " \
        python3-dateutil \
        "

Using the information and packages at the PyPi website, you can fill in the details about the new python package

.. figure:: /_static/pypi-package.png
   :alt: Pypi package
   :align: center
   :width: 5in

   Pypi package

Update the following variables to reflect the details from the package you wish to create a recipe for.

#. DESCRIPTION
#. HOMEPAGE
#. LICENSE
#. LIC_FILES_CHKSUM
#. SRC_URI[md5sum] (md5sum of the download artifact from pypi)
#. SRC_URI[sha256sum] (sha256sum of the download artifact from pypi)
#. DEPENDS
   Dependencies resolved at do_configure
#. RDEPENDS
   Dependencies resolved at do_build
