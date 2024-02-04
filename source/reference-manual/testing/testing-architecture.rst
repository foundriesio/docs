.. highlight:: sh

.. _ref-testing-architecture:

Architecture Overview
=====================

Your Factory includes a generic :ref:`API and data model <ref-fiotest>` that allows you the freedom to test how you choose.
In most cases, you'll be able to use fiotest as-is for your testing needs.

All things in a Factory revolve around Targets, and the testing mechanism is no different.
Devices run Targets.
The results of any tests they run are correlated with its Target.
This allows you to get a test reporting of Targets in your Factory.

The fiotest container can be set up in your Factory as a :ref:`Docker Compose application <ref-compose-apps>`.
The fiotest container has the ability to interact with the host OS.
It can configure aktualizr-lite to notify it when a new Target has been installed.
Then, fiotest is able to run tests and report the results back through the :ref:`device gateway <ref-ota-architecture>`.

fiotest includes a `test specification`_ that allows you to define how and what to test.
The container can also be extended/customized for your specific needs.

Workflow
~~~~~~~~

The way testing typically flows:

 * Customer pushes code (``git push``)
 * CI builds a new Target
 * aktualizr-lite will see this new Target and:

   * Installs Target
   * Notifies fiotest once the Target becomes active

     * Tests are run and results are reported via the device gateway
       for the Target.

.. figure:: /_static/testing-arch.png
     :align: center
     :scale: 70 %
     :alt: Testing architecture diagram

.. _test specification:
   https://github.com/foundriesio/fiotest#testing-specification
