.. _ref-toolchain:

Toolchain
=========

The default toolchain used in ``openembedded-core`` is ``gcc`` but this is configurable.
The ``clang`` toolchain is provided by ``meta-clang``, and can be set globally or per recipe.
Since version **v89**, LmP uses ``clang`` as the default compiler and ``llvm`` as the default runtime.

.. prompt:: text

  TOOLCHAIN ?= "clang"
  RUNTIME = "llvm"

However, some issues exist when using clang/llvm as the default,
as some recipes are not prepared to be built with this toolchain.
To address these issues is recomendend to add a new file where these
tweeks will be made to build sucessfully.

In the public LmP layer ``meta-lmp`` we use the
``meta-lmp-base/conf/distro/include/non-clangable.inc``
for that propuse.
Adding another ``non-clangable.inc`` on the factory layer ``meta-subscriber-overrides``
can be a solution, where we will collect all the ``clang`` tweeks needed.

This configuration can be added in the factory global configurations file
``conf/machine/include/lmp-factory-custom.inc``

.. prompt:: text

  require conf/machine/include/non-clangable.inc

**So we will use the factory file ``conf/machine/include/non-clangable.inc``**
to customize everything ``clang`` related.

Changing the toolchain
----------------------

To change the default values disabling the ``clang`` compiler globaly and use the ``gcc``
we need to change the ``TOOLCHAIN`` value.

.. prompt:: text

  TOOLCHAIN = "gcc"

Changing the compiler per recipe is also possible. To do that we add the
line above in a `.bbappend` for the recipe.
This can also be done in the factory, changing the file
``conf/machine/include/non-clangable.inc``, from ``meta-subscriber-overrides``.

.. prompt:: text

  TOOLCHAIN:pn-<recipe> = "gcc"


Customizing the Default Toolchain
---------------------------------

When using the clang toolchain we have the ``toolchain-clang`` override that can be used
to do the customization and this will only take effect when clang is in use.
All of these customizations can be placed in the factory by changing the file
``conf/machine/include/non-clangable.inc``, from ``meta-subscriber-overrides``.

.. prompt:: text

  STRIP:pn-<recipe>:toolchain-clang = "${HOST_PREFIX}strip"
  OBJCOPY:pn-<recipe>:toolchain-clang = "${HOST_PREFIX}objcopy"
  COMPILER_RT:pn-<recipe>:toolchain-clang = "-rtlib=libgcc --unwindlib=libgcc"


More information can be found via the `meta-clang repository <https://github.com/kraj/meta-clang>`_.
