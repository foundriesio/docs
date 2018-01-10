.. _howto-zephyr-boards:

Zephyr microPlatform Boards HOWTO
=================================

This page provides information on porting a board to the Zephyr
microPlatform.

.. warning::

   Porting a board necessarily means altering the Zephyr repository,
   which complicates the ``repo sync`` process used to receive
   updates.

   See :ref:`howto-zephyr-workflows` for more details.

Start with the `Zephyr porting guides`_, and the existing supported
boards. In addition to architecture and basic board support, you'll
need a flash driver and working networking for MCUBoot and FOTA
updates. Some useful starting points:

- ``include/flash.h`` and the ``drivers/flash`` directory in the
  Zephyr source tree for flash drivers.

- The `Zephyr networking documentation`_

Some particular areas to be aware of when porting Zephyr
microPlatform-based applications to a new board follow.

- Flashing hacks in the Zephyr runner infrastructure: the :ref:`zmp
  <ref-zephyr-zmp>` tool currently relies on some hacks (search for
  ``ZEPHYR_HACK_OVERRIDE_BIN``) to flash the signed binary for
  chain-loading by MCUBoot. Currently, only Zephyr boards which use
  pyOCD and DfuSe (USB DFU with STMicroelectronics extensions via
  dfu-util) support this hack. You may need to adjust your runner
  implementation accordingly to enable :ref:`zmp flash
  <ref-zephyr-zmp-flash>` (see the directory
  :file:`zmp/zephyr/scripts/support/runner`)

- `Device tree with flash partitions`_: your board will need a device
  tree defined, which includes flash partitions for MCUBoot itself
  (``boot_partition``), a partition your application runs in
  (``slot0_partition``), a partition to download firmware updates into
  (``slot1_partitition``; this must be the same size as
  ``slot0_partition``), and a scratch partition for MCUBoot to use
  when swapping images between slots 0 and 1 (``scratch_partition``;
  this can be as small as a single sector, but be aware of extra wear
  on your flash). Currently, ``slot0_partition``, ``slot1_partition``,
  and ``scratch_partition`` must be contiguous on flash. The
  ``boot_partition`` must be chosen so that the chip reset vector will
  be loaded from there.

  Each supported board has a device tree with a partition layout you
  can use while getting started.

- A device tree overlay file: your application needs a device tree
  ``.overlay`` file instructing the Zephyr build system to use the
  flash partitions defined in the device tree when linking.

  See the example overlay files in the ``boards`` subdirectory of each
  sample application, along with the build system files which use
  them, for reference.

  Selecting ``slot0_partition`` within your DTS overlay will ensure
  that your application is linked appropriately:

  .. code-block:: none

     / {
             chosen {
                     zephyr,code-partition = &slot0_partition;
             };
     };

  For additional information on this, see the documentation for
  `CONFIG_FLASH_LOAD_OFFSET`_ and `CONFIG_FLASH_LOAD_SIZE`_. Note that
  **these values are set automatically** by Zephyr's
  ``scripts/dts/extract_dts_includes.py`` script as a consequence of
  your DTS overlay file.

- `CONFIG_TEXT_SECTION_OFFSET`_: On ARM targets, this is the offset
  from ``CONFIG_FLASH_LOAD_OFFSET`` at which your application's vector
  table is stored. This is required so :ref:`zmp build
  <ref-zephyr-zmp-build>` can place an MCUBoot header in the space
  between the flash load offset and the beginning of your image.

  If you're unsure, ``0x200`` is a generally safe default value.

  Lower values (such as 0x100) may be possible depending on your
  chip's vector table alignment requirements. Smaller values waste
  less flash space.

- To port MCUBoot to your board, you also need a Zephyr flash driver,
  ideally (though not necessarily) with `CONFIG_FLASH_PAGE_LAYOUT`_
  support.

  (MCUBoot's build system will automatically pick up the device tree
  partitions you define in Zephyr, and :ref:`zmp <ref-zephyr-zmp>`
  will be automatically be able to build MCUBoot for your board once
  it's got Zephyr support.)

  For additional background information on porting MCUBoot to your
  board, see the `MCUBoot README-zephyr.rst`_ file.

.. _Zephyr porting guides: http://docs.zephyrproject.org/porting/porting.html

.. _Zephyr networking documentation: http://docs.zephyrproject.org/subsystems/networking/networking.html

.. _Device tree with flash partitions: http://docs.zephyrproject.org/devices/dts/device_tree.html

.. _CONFIG_TEXT_SECTION_OFFSET: http://docs.zephyrproject.org/reference/kconfig/CONFIG_TEXT_SECTION_OFFSET.html#cmdoption-arg-config-text-section-offset

.. _CONFIG_FLASH_LOAD_OFFSET: http://docs.zephyrproject.org/reference/kconfig/CONFIG_FLASH_LOAD_OFFSET.html#cmdoption-arg-config-flash-load-offset

.. _CONFIG_FLASH_LOAD_SIZE: http://docs.zephyrproject.org/reference/kconfig/CONFIG_FLASH_LOAD_SIZE.html#cmdoption-arg-config-flash-load-size

.. _CONFIG_FLASH_PAGE_LAYOUT: http://docs.zephyrproject.org/reference/kconfig/CONFIG_FLASH_PAGE_LAYOUT.html#cmdoption-arg-config-flash-page-layout

.. _MCUBoot README-zephyr.rst: https://github.com/runtimeco/mcuboot/blob/master/README-zephyr.rst
