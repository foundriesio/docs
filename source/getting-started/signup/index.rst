.. _gs-signup:

Sign Up
=======

To create a FoundriesFactory, you first need to `create an account <signup_>`_ with us.

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

Create one by clicking :guilabel:`Create Factory`

.. figure:: /_static/signup/no-factories.png
   :width: 400
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

.. _gs-select-platform:

Select Your Platform
####################

Choose a hardware platform from the dropdown menu in the  **Create New Factory** wizard
and continue. Click :guilabel:`Create Factory` once your details are entered.

The :ref:`ref-linux` supports a wide range of platforms out of the box. This
includes QEMU_ images for ARM_ and RISC-V_ architectures.

.. figure:: /_static/signup/create.png
   :width: 400
   :align: center

.. tip::

   Your chosen platform determines what the initial value for the ``machines:``
   key will be for your first build. This key and its value can later be changed
   via ``factory-config.yml`` in :ref:`ref-Factory-definition`

.. _QEMU: https://www.qemu.org/
.. _ARM: https://www.arm.com/
.. _RISC-V: https://riscv.org/

.. _gs-watch-build:

Watch Your Build
################

Once you have created your Factory, an initial build of the LmP will be
generated for you to build your product on top of. You can monitor the progress
of this initial build in the :guilabel:`Targets` tab of your Factory after a few
minutes. Additionally, you will recieve an Email once your build is complete.

This section will become more useful as you begin to build your application and
declare new Targets for the Factory to build. You can learn about creating Targets in the
:ref:`ref-advanced-tagging` section

.. note::

   If you'd like to learn more, `we wrote a blog
   <https://foundries.io/insights/blog/2020/05/14/whats-a-target/>`_ about what Targets
   are and why we made them the way they are.

.. figure:: /_static/signup/build.png
   :width: 900
   :align: center

.. warning::

   Bootstrapping your OS securely takes some time. Secure caching isn't simple,
   so your first build will take up to 3 hours to complete. Subsequent builds
   will be much faster.

   Read through the rest of this section and set up your development
   environment while you wait for us to build your OS from scratch.

.. _cgit: https://git.zx2c4.com/cgit/
