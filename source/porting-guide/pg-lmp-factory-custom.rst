.. _ref-pg-lmp-factory-custom:

Lmp-factory-custom
^^^^^^^^^^^^^^^^^^

The FoundriesFactory includes a file
(``conf/machine/include/lmp-factory-custom.inc``) which can be used to
replace or extend options as defined by ``meta-lmp``, and works to
customize the overall behavior of LmP focusing on the target machine.

It takes place on those cases when the porting does not
create a new machine configuration file and only overrides the definition from
an existing machine.