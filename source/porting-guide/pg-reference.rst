.. _ref-pg-reference-board:

Finding a Similar Supported Reference Board
-------------------------------------------

For some projects, it is easy to understand which reference board is closest to the one being ported.
It is common that in early stages, the project starts with a reference board.
When that is the case, the reference board is obvious; is only a matter of searching :ref:`ref-linux-supported` to check if this is supported.

The other case is when it is not an obvious answer.
The task of searching for the closest reference board requires looking for one which shares the same SoC.
This is usually described in the machine configuration file by the tag ``@SOC``.

When searching for ``@SOC`` through the meta-layers, you may find more than one machine with the same SoC.
The suggestion here is to prefer the machine from the SoC vendor.

The SoC vendor is usually present on the tag ``@NAME`` in the machine configuration file.

In this document, there are several examples where i.MX8M Mini :term:`EVK` is used as a reference board.
