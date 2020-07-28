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

Create a Factory |:factory:|
============================

:ref:`ref-factory` is the start of your embedded OS, tailored specifically
for your product. When you create a factory, we immediately bootstrap the CI
build process for a vanilla, unmodified :ref:`ref-linux` OS Image, which is from
this point onward, **owned by you**. 

When your account is created, it is not associated with any factories. 

Create one by clicking **Create Factory**

.. figure:: /_static/signup/no-factories.png
   :width: 400
   :align: center

   Your journey begins empty handed

Select Your Platform |:desktop:|
################################

Choose a hardware platform from the dropdown menu in the  **Create New Factory** wizard
and continue.

The :ref:`ref-linux` supports a wide range of platforms out of the box. We even
provide QEMU_ images for ARM_ and RISC-V_ architectures.

.. figure:: /_static/signup/create.png
   :width: 400
   :align: center

.. tip:: 

   Your chosen platform determines what the initial value for the ``machines:``
   key will be for your first build. This key and its value can later be changed
   via ``factory-config.yml`` in :ref:`ref-factory-definition`

.. note::
   
   |:timer:| Bootstrapping your OS securely takes some time. Secure caching isn't simple,
   so your first build will take up to an hour to complete. Subsequent builds
   will be much faster. 

   |:books:| Read through the rest of this section and set up your development
   environment while you wait for us to build your OS from scratch. 

.. _QEMU: https://www.qemu.org/
.. _ARM: https://www.arm.com/
.. _RISC-V: https://riscv.org/

