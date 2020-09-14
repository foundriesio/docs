.. _ref-signup:

Sign Up |:clipboard:|
==========================

To create a FoundriesFactory, you first need to `create an account <signup_>`_ with us. 

.. figure:: /_static/signup/login.png
   :width: 400
   :align: center
   :target: signup_
   
   This is the beginning  of your journey.

.. _signup: https://app.foundries.io/signup

Create a Factory |:gear:|
============================

:ref:`ref-factory` is the start of your embedded OS, tailored specifically
for your product. When you create a Factory, we immediately bootstrap the CI
build process for a vanilla, unmodified :ref:`ref-linux` OS Image, which is from
this point onward, **owned by you**. 

When your account is created, it is not associated with any factories. 

Create one by clicking **Create Factory**

.. figure:: /_static/signup/no-factories.png
   :width: 400
   :align: center

   Your journey begins empty handed

.. note::
   
   |:closed_lock_with_key:| Upon Factory creation you will be sent an email containing your
   :ref:`ref-offline-keys`. Read this documentation for information on key
   rotation. 

   It is incredibly important that your keys are kept **safe and
   private**. Please store these keys securely. 

.. todo:: 

    Suggest methods of storing TuF keys securely, such as by USB in a
    safety deposit box, or yubikey.

.. _ref-select-platform:

Select Your Platform |:desktop:|
################################

Choose a hardware platform from the dropdown menu in the  **Create New Factory** wizard
and continue.

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

.. _ref-watch-build:

Watch Your Build |:hammer_and_wrench:|
######################################

Once you have created your Factory, an initial build of the the LmP will be
generated for you to build your product on top of. You can monitor the progress
of this initial build in the **Targets** tab of your Factory. 

This section will become more useful as you begin to build your application and
declare new targets for us to build. You can learn about creating targets in the
:ref:`ref-advanced-tagging` section

.. note:: 

   |:pencil:| If you'd like to learn, `we wrote a blog
   <https://foundries.io/insights/2020/05/14/whats-a-target/>`_ about what targets
   are and why we made them the way they are. 

.. figure:: /_static/signup/build.png
   :width: 900
   :align: center

.. warning::
   
   |:timer:| Bootstrapping your OS securely takes some time. Secure caching isn't simple,
   so your first build will take up to an hour to complete. Subsequent builds
   will be much faster. 

   |:books:| Read through the rest of this section and set up your development
   environment while you wait for us to build your OS from scratch. 

.. _
