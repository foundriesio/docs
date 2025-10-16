.. _gs-signup-co:

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

Once the signup process is complete, you can proceed with creating a Factory.

Creating Your Factory
=====================

:ref:`ref-factory` is the start of your embedded OS, tailored specifically for your product.
When your account is created, it is not associated with any factories.
Create one by clicking :guilabel:`New Factory`.

.. figure:: /_static/getting-started/signup/no-factories.png
   :width: 900
   :align: center
   :alt: no Factories screen

   Your journey begins empty handed

.. _gs-select-platform-co:

Selecting Your Container-only Platform
######################################

Choose a hardware platform from the dropdown menu in the  **Create Factory** wizard and continue.
Click :guilabel:`Create Factory` once your details are entered.

.. warning::

   Once a Factory is created, the chosen platform/machine and Factory name cannot be changed.
   Create a new Factory or `contact support <https://support.foundries.io>`_ if a mistake is made.

The dropdown menu includes a range of choices. You must choose one of these options to create a container-only Factory:

- Community Edition Arm64
- Community Edition x86
- Arduino UNO Q

The Initial Target
##################

Factory creation takes 30-60 seconds to complete.
Once created, your Factory will show an initial "Target" and you will receive an email.

.. figure:: /_static/getting-started/signup/build.png
   :width: 900
   :align: center
   :alt: Targets view showing prebuilt target

   FoundriesFactory Targets

A Target is a reference to the specific version of applications.
When developers push code, FoundriesFactory produces a new :term:`Target`.
Registered devices then update and install Targets.
The initial Target for a new Factory does not include any applications.
