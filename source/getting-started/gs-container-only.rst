.. _ref-gs-container-only:

Getting Started with Container-only Factories
=============================================

Container-only Factories allow users to experience a FoundriesFactory without having to run the Linux microPlatform on their device.
Container-only Factories can be done on any Arm64 or x86 platform.
A Debian package archive_ is included with statically linked binaries for Debian/Ubuntu users.
There are few differences between the Container-only Factory and the LmP-based Factory:

- OS updates are not built into the offering. It's possible, but not integrated the same way OSTree updates are built into LmP based Factories.
- The Fioup_ update agent is used instead of :ref:`Aktualizr-Lite <ref-aktualizr-lite>`. They share the same configuration format and files, but Fioup is focused on container-only updates.
- No TUF_ validation. The Factory includes TUF signed metadata.
  However, its not verfied by Fioup in the Community Edition.
  This can be enabled for paid versions of the product as you get ready to move from evaluation to production.

.. _archive: https://github.com/foundriesio/fioup/blob/main/docs/install.md
.. _Fioup: https://github.com/foundriesio/fioup/blob/main/docs/README.md
.. _TUF: https://theupdateframework.com/


.. toctree::

   signup-container-only/index
   ci-selection
   fioup-registration/index

Additional Resources
--------------------
- :ref:`ref-container-only-arch` architecture
- :ref:`ref-compose-apps`
