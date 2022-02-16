.. _ref-pg-reference-board:

Finding a similar reference board already supported
---------------------------------------------------

For some projects, it is easy to understand which reference board is
closest to the one being included. It is common that in early stages,
the project starts using a reference board, and when that is the case, the
reference board is obvious; is only a matter of searching
:ref:`ref-linux-supported` to check if this is supported.

In the other case when it is not an obvious answer, the task of
searching for the closest reference board is looking for what
reference board shares the same SoC which is usually described in the
machine configuration file by the tag ``@SOC``.

If searching for ``@SOC`` through the meta-layers brings more than one
machine with the same SoC used on the project, the suggestion here is to
prefer the machine from the SoC vendor.

The SoC vendor is usually present on the tag ``@NAME`` in the machine
configuration file.

In this document, there are several examples where i.MX8M Mini EVK is
used as a reference board.