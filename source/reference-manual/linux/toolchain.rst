.. _ref-toolchain:

Toolchain
=========

The default toolchain used in ``openembedded-core`` is ``gcc``, but this is configurable.
The ``clang`` toolchain is provided by ``meta-clang``, and can be set globally or per recipe.
Since version **v89**, the LmP uses ``clang`` as the default compiler, and ``llvm`` as the default runtime.

.. code-block::

   TOOLCHAIN ?= "clang"
   RUNTIME = "llvm"

However, some issues exist when using clang/llvm as the default.
Namely, some recipes are not prepared to be built with this toolchain.
To address this, add a new file where the tweaks to build successfully will be made.

In the public LmP layer ``meta-lmp``, we use the ``meta-lmp-base/conf/distro/include/non-clangable.inc`` for that propose.
We will add another ``non-clangable.inc`` in the Factory layer ``meta-subscriber-overrides``, where we will collect all the ``clang`` tweaks needed.

This configuration can be added in the Factory global configurations file, ``conf/machine/include/lmp-factory-custom.inc``

.. code-block::

   require conf/machine/include/non-clangable.inc

**So we will use the Factory file**, ``conf/machine/include/non-clangable.inc`` to customize everything ``clang`` related.

Changing the Toolchain
----------------------

To change the default values, disable the ``clang`` compiler globally.
Instead, use ``gcc`` by changing the ``TOOLCHAIN`` value:

.. prompt:: text

  TOOLCHAIN = "gcc"

Changing the compiler per recipe is also possible.
To do this, we add the line above in a  recipe ``.bbappend``.
This can also be done in the Factory, changing the file ``conf/machine/include/non-clangable.inc``, in ``meta-subscriber-overrides``:

.. prompt:: text

  TOOLCHAIN:pn-<recipe> = "gcc"


Customizing the Default Toolchain
---------------------------------

When using the clang toolchain, we have the ``toolchain-clang`` override.
This can be used to do the customization, and will only take effect when clang is in use.
All of these customizations can be placed in the Factory.
Once again, do this by changing the file ``conf/machine/include/non-clangable.inc``, in ``meta-subscriber-overrides``:

.. prompt:: text

  STRIP:pn-<recipe>:toolchain-clang = "${HOST_PREFIX}strip"
  OBJCOPY:pn-<recipe>:toolchain-clang = "${HOST_PREFIX}objcopy"
  COMPILER_RT:pn-<recipe>:toolchain-clang = "-rtlib=libgcc --unwindlib=libgcc"


More information can be found via the `meta-clang repository <https://github.com/kraj/meta-clang>`_.
