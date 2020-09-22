.. _ref-signup:

Sign Up
=======

I am making some changes that will be used to show how we can do PRs directly from the github UI

.. figure:: /_static/signup/login.png
   :width: 400
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

Create one by clicking **Create Factory**

.. figure:: /_static/signup/no-factories.png
   :width: 600
   :align: center

   Your journey begins empty handed

.. note::

   Upon Factory creation you will be sent an email
   with instructions to securely download your
   :ref:`ref-offline-keys`. Read :ref:`this documentation<ref-offline-keys>` for information on key
   rotation.

   It is incredibly important that your keys are kept **safe and
   private**. Please store these keys securely.

.. todo::

    Suggest methods of storing TuF keys securely, such as by USB in a
    safety deposit box, or yubikey.

.. _ref-select-platform:

Select Your Platform
####################

The :ref:`ref-linux` supports a wide range of platforms out of the box. This
includes QEMU_ images for ARM_ and RISC-V_ architectures.

.. note::

   To change the platform your Factory produces builds for, you must change the
   value of the ``machines:`` key in your ``factory-config.yml`` to one of our
   supported boards from the :ref:`ref-linux-targets` section. Read the
   :ref:`ref-Factory-definition` page for more details.

.. _QEMU: https://www.qemu.org/
.. _ARM: https://www.arm.com/
.. _RISC-V: https://riscv.org/

.. _ref-watch-build:

Watch Your Build
################

Once you have created your Factory, an initial build of the LmP will be
generated for you to build your product on top of. You can monitor the progress
of this initial build by clicking the **MICROPLATFORM** button in your Factory
UI. The **SOURCE CODE** button will take you to your Factory source code in the
cgit_ web frontend.

.. figure:: /_static/signup/build.png
   :width: 900
   :align: center

This section will become more useful as you begin to build your application and
declare new targets for the Factory to build. You can learn about creating targets in the
:ref:`ref-advanced-tagging` section

.. note::

   If you'd like to learn more, `we wrote a blog
   <https://foundries.io/insights/2020/05/14/whats-a-target/>`_ about what targets
   are and why we made them the way they are.

.. warning::

   Bootstrapping your OS securely takes some time. Secure caching isn't simple,
   so your first build will take up to an hour to complete. Subsequent builds
   will be much faster.

   Read through the rest of this section and set up your development
   environment while you wait for us to build your OS from scratch.

.. _cgit: https://git.zx2c4.com/cgit/
