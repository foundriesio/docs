.. _gs-signup:

Signing Up
==========

To begin using FoundriesFactory®, start with `creating an account <signup_>`_ with us.

.. figure:: /_static/signup/signup.png
   :width: 380
   :align: center
   :target: signup_

   This is the beginning  of your journey.

.. _signup: https://app.foundries.io/signup

Creating Your Factory
=====================

:ref:`ref-factory` is the start of your embedded OS, tailored specifically for your product.
When you create a Factory, we immediately bootstrap the CI build process.
This generates a vanilla, unmodified :ref:`ref-linux` OS Image, which is from this point onward, **owned by you**.

When your account is created, it is not associated with any factories.
Create one by clicking :guilabel:`Create Factory`.

.. warning::

   Once a Factory is created, the chosen platform/machine and Factory name cannot be changed.
   Create a new Factory or contact support if a mistake is made: https://support.foundries.io/.

.. figure:: /_static/signup/no-factories.png
   :width: 900
   :align: center

   Your journey begins empty handed




.. _gs-select-platform:

Selecting Your Platform
#######################

Choose a hardware platform from the dropdown menu in the  **Create New Factory** wizard and continue.
Click :guilabel:`Create Factory` once your details are entered.

The :ref:`ref-linux` supports a wide range of platforms out of the box.
This includes QEMU_ images for ARM_ and RISC-V_ architectures.

.. figure:: /_static/signup/create.png
   :width: 450
   :align: center

   Create Factory

.. tip::

   Your chosen platform determines what the initial value for the ``machines:``
   key will be for your first build.

.. _QEMU: https://www.qemu.org/
.. _ARM: https://www.arm.com/
.. _RISC-V: https://riscv.org/

.. _gs-watch-build:

Watching Your Build
###################

Once you have created your Factory, a build of the Foundries.io™ Linux® microPlatform (LmP) will be generated.
This is what you will build your product on top of.
You can monitor the progress of builds in the :guilabel:`Targets` tab of your Factory after a few minutes.
Additionally, you will receive an email once this initial build is complete.

Targets are a reference to a platform image and Docker applications.
When developers push code, FoundriesFactory produces a new target.
Registered devices then update and install targets.

The :guilabel:`Targets` tab of the Factory will become more useful as you begin
to build your application and produce new Targets for the Factory to build.

.. note::

   If you would like to learn more, `we wrote a blog
   <https://foundries.io/insights/blog/2020/05/14/whats-a-target/>`_ about what Targets
   are and why we made them the way they are.

.. figure:: /_static/signup/build.png
   :width: 900
   :align: center

   FoundriesFactory Targets

.. hint::

   Bootstrapping your Factory securely takes some time.
   Your first build will likely take **30 minutes** or more to complete.

   Use this time to set up your development environment and get started with Docker commands.
   These guides do not require any hardware:

   - :ref:`gs-git-config`
   - :ref:`gs-install-fioctl`
   - :ref:`tutorial-gs-with-docker`

