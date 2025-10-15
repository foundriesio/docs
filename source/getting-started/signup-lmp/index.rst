.. _gs-signup:

Signing Up
==========

To begin using the FoundriesFactory™ Platform, start with `creating an account <signup_>`_ with us.

.. figure:: /_static/getting-started/signup/signup.png
   :width: 380
   :align: center
   :target: signup_
   :alt: signup form

   This is the beginning of your journey.

.. _signup: https://app.foundries.io/signup

Creating Your Factory
=====================

:ref:`ref-factory` is the start of your embedded OS, tailored specifically for your product.
When you create a :term:`Factory`, we immediately bootstrap the CI build process.
This generates an unmodified :ref:`ref-linux` OS Image, which is from this point onward, **owned by you**.

When your account is created, it is not associated with any factories.
Create one by clicking :guilabel:`New Factory`.

.. figure:: /_static/getting-started/signup/no-factories.png
   :width: 900
   :align: center
   :alt: no Factories screen

   Your journey begins empty handed

.. _gs-select-platform:

Selecting Your Platform
#######################

Choose a hardware platform from the dropdown menu in the  **Create Factory** wizard and continue.
Click :guilabel:`Create Factory` once your details are entered.

.. warning::

   Once a Factory is created, the chosen platform/machine and Factory name cannot be changed.
   Create a new Factory or `contact support <https://support.foundries.io>`_ if a mistake is made.

The :ref:`ref-linux` supports a wide range of platforms out of the box.
This includes QEMU_ images.

.. figure:: /_static/getting-started/signup/create.png
   :width: 450
   :align: center
   :alt: platform selection and factory name 

   Create Factory

.. tip::

   Your chosen platform determines the value for the ``machines:`` key for your builds.

.. _QEMU: https://www.qemu.org/

.. _gs-watch-build:

Watching Your Build
###################

Once you have created your Factory, the initial artifacts from the Foundries.io™ Linux® microPlatform (LmP) will be generated.
This is the base to build your product.
You can monitor the progress in the :guilabel:`Targets` tab of your Factory.
Additionally, you will receive an email once the Factory initial setup is complete.

.. figure:: /_static/getting-started/signup/build.png
   :width: 900
   :align: center
   :alt: Targets view showing prebuilt target

   FoundriesFactory Targets

Targets are a reference to a platform image and Docker applications.
When developers push code, FoundriesFactory produces a new :term:`Target`.
Registered devices then update and install Targets.

.. note::

   If you would like to learn more, we wrote a `blog
   <https://foundries.io/insights/blog/whats-a-target/>`_ about what Targets
   are and why we made them the way they are.

The :guilabel:`Targets` tab of the Factory will become more useful as you begin
to build your application and produce new Targets for the Factory to build.
