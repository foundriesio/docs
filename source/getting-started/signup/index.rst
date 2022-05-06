.. _gs-signup:

Sign Up
=======

To create a FoundriesFactory, you first need to `create an account <signup_>`_ with us.

.. figure:: /_static/signup/signup.png
   :width: 380
   :align: center
   :target: signup_

   This is the beginning  of your journey.

.. _signup: https://app.foundries.io/signup

Create a Factory
================

:ref:`ref-factory` is the start of your embedded OS, tailored specifically
for your product. When you create a Factory, we immediately bootstrap the CI
build process for a vanilla, unmodified :ref:`ref-linux` OS Image, which is from
this point onward, **owned by you**.

When your account is created, it is not associated with any factories.

Create one by clicking :guilabel:`Create Factory`.

.. warning::

   Once a Factory is created, the chosen platform/machine and Factory name
   cannot be changed. Create a new Factory or contact support if a mistake is
   made. https://support.foundries.io/.

.. figure:: /_static/signup/no-factories.png
   :width: 900
   :align: center

   Your journey begins empty handed

.. important::

   Upon Factory creation you will be sent an email
   with instructions to securely download your
   :ref:`ref-offline-keys`.

   It is incredibly important that your keys are kept **safe and
   private**. Please store these keys securely.

.. todo::

    Suggest methods of storing TuF keys securely, such as by USB in a
    safety deposit box, or yubikey.

.. _gs-select-platform:

Select Your Platform
####################

Choose a hardware platform from the dropdown menu in the  **Create New Factory** wizard
and continue. Click :guilabel:`Create Factory` once your details are entered.

The :ref:`ref-linux` supports a wide range of platforms out of the box. This
includes QEMU_ images for ARM_ and RISC-V_ architectures.

.. figure:: /_static/signup/create.png
   :width: 450
   :align: center

   Create Factory

.. tip::

   Your chosen platform determines what the initial value for the ``machines:``
   key will be for your first build. This key and its value can later be changed
   via ``factory-config.yml`` in the :ref:`ref-Factory-definition`

.. _QEMU: https://www.qemu.org/
.. _ARM: https://www.arm.com/
.. _RISC-V: https://riscv.org/

.. _gs-watch-build:

Watch Your Build
################

Once you have created your Factory, an initial build of the
Foundries.io Linux microPlatform (LmP) will be
generated for you to build your product on top of. You can monitor the progress
of this initial build in the :guilabel:`Targets` tab of your Factory after a few
minutes. Additionally, you will receive an email once this initial build is
complete.

Targets are a reference to a platform image and docker applications. When
developers push code, FoundriesFactory produces a new target. Registered
devices update and install targets.

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

   Bootstrapping your Factory securely takes some time. Your first build
   will likely take **30 minutes** or more to complete.

   Use this time to set up your development environment 
   and get started with docker commands. These guides do not require any hardware:

   - :ref:`gs-git-config`
   - :ref:`gs-install-fioctl`
   - :ref:`tutorial-gs-with-docker`

.. _cgit: https://git.zx2c4.com/cgit/
