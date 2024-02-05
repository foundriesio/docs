.. _ref-pg-lmp-factory-custom:

``lmp-factory-custom``
^^^^^^^^^^^^^^^^^^^^^^

Your Factory includes a file, ``conf/machine/include/lmp-factory-custom.inc``.
This can be used to replace or extend options as defined by ``meta-lmp``.
It works to customize the overall behavior of LmP, focusing on the target machine.

This applies to cases when the porting does not create a new machine configuration file,
and only overrides the definition from an existing machine.
