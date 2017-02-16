.. highlight:: sh

.. _device-support-nrf52:

NRF52 (nRF52 DK, Nitrogen)
==========================

For development, Nordic sells a development board called `nRF52 DK
<https://www.nordicsemi.com/eng/Products/Bluetooth-low-energy/nRF52-DK>`_.

The DK comes with an on-board J-Link debugger (`J-Link OB
<https://www.segger.com/jlink-ob.html>`_), which provides a similar
functionality as `ARM CMSIS-DAP
<https://developer.mbed.org/handbook/CMSIS-DAP>`_, but provides a
faster and more stable connection. The disadvantage is that it is a
proprietary solution.

The 96boards Nitrogen board can be flashed and debugged via CMSIS-DAP,
which is provided by the `LPC11U35
<http://www.nxp.com/documents/data_sheet/LPC11U3X.pdf>`_ chip. The
Nitrogen design has LPC11U35 providing the MCU interface to the main
nRF52 chip.

SoftDevice
----------

For Titan, S132 is already enough since ANT is not required.

S132 SoftDevice
~~~~~~~~~~~~~~~

The S132 SoftDevice is a Bluetooth low energy (BLE) Central and
Peripheral protocol stack solution. It supports up to eight
connections with an additional Observer and a Broadcaster role all
running concurrently. The S132 SoftDevice integrates a BLE Controller
and Host, and provides a full and flexible API for building Bluetooth
Smart nRF52 System on Chip (SoC) solutions.

S332 SoftDevice
~~~~~~~~~~~~~~~

The S332 SoftDevice is a combined ANT and Bluetooth low energy (BLE)
protocol stack solution. It supports all four Bluetooth low energy
roles (central, peripheral, observer, broadcaster) and ANT.

Nordik SDK
----------

Available at
https://www.nordicsemi.com/eng/Products/Bluetooth-low-energy/nRF5-SDK.

It provides several examples and components that can be used as
reference, when testing and creating applications for the Nordic SoC.

There is also an easy way to extend the SDK to create support for
additional boards. The support can be created at
sdk/examples/bsp. This is a good way to test boards without requiring
Zephyr support.

Segger
------

The nRF52 DK board can also be used as a J-Link Segger board, by
hooking the debug output pins into the desired board. This is an easy
way to debug custom designs, without requiring external hardware. For
more information, please check
http://infocenter.nordicsemi.com/topic/com.nordic.infocenter.nrf52/dita/nrf52/development/dev_kit_v1.1.0/hw_debug_out.html?cp=2_0_0_1_9.

To use **GDB**, please have a look :ref:`further down in this document
<device-support-nrf52-gdb>`.

Official documentation:

- https://www.segger.com/admin/uploads/productDocs/UM08001_JLink.pdf
- https://www.segger.com/downloads/jlink

It's also possible to retrieve the UART output by using the SWO pin,
as described at
https://devzone.nordicsemi.com/question/78682/using-swo-with-nrf52-redux/.

UART
----

nRF52 DK
~~~~~~~~

Pins P0.05, P0.06, P0.07, and P0.08 are by default used by the UART
connected to the Interface MCU.

Nitrogen
~~~~~~~~

Pins 12, 13, 14, 15, can be accessed via the CMSIS-DAP interface (virtual console).

Flashing
--------

nRF52 DK
~~~~~~~~

The DK board can be flashed via the USB storage interface
(drag-and-drop), and also via the nrfjprog (using J-Link) software.

Using **nrfjprog**:

- Erase: ``nrfjprog -e --family NRF52``
- Flash: ``nrfjprog --family NRF52 --program foo.hex``
- Restart: ``nrfjprog -r --family NRF52``

Nitrogen
~~~~~~~~

Since CMSIS-DAP is available via the LPC11U35 chip, the board can be
flashed via the **USB storage interface** (drag-and-drop), and also
via `pyOCD <https://github.com/mbedmicro/pyOCD>`_ or `openOCD
<http://openocd.org/>`_.

Using pyOCD (supported by ARM):

- Erase: ``pyocd-flashtool -d debug -t nrf52 -ce``
- Flash: ``pyocd-flashtool -d debug -t nrf52 foo.hex``
- Restart: ``pyocd-tool -d debug reset``

For a faster flashing process, change the -f argument to a higher
value, like 90000. We didn't yet investigate how big this value can
be, so use with care.

For openOCD, be aware that the nRF52 support is not yet merged. Check
http://openocd.zylin.com/#/c/3511/ for the latest status.

.. _device-support-nrf52-gdb:

GDB
---

Run GDB on target
~~~~~~~~~~~~~~~~~

The NRF52 Development Kit supports running GDB without any other
peripheral/device than the DK itself and the only connection you need
is with the USB cable, nothing else. You'll need to open two shells
for a working setup. One that runs the GDB server an one that runs the
GDB instance itself. In the example below we are using the "blinky"
application from the Nordic SDK. That file isn't there by default, so
you would need to build the blinky application to start with.

In shell 1, run::

    JLinkGDBServer -if swd -device nrf52 -speed 1000

In shell 2, run::

    ~/toolchains/gcc-arm-none-eabi-4_9-2015q1/bin/arm-none-eabi-gdb
    (gdb) target remote localhost:2331
    (gdb) symbol-file ~/devel/nRF5_SDK_11/examples/peripheral/blinky/pca10040/s132/armgcc/_build/nrf52832_xxaa_s132.out
    (gdb) b main
    (gdb) mon reset
    (gdb) c

Debugging the boot loader example in the Nordic SDK
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First start with flashing the SoftDevice and bootloader::

   nrfjprog --family nrf52 --chiperase --program ./examples/dfu/ble_dfu_send_hex/test_images_update_nrf52/dfu_test_softdevice_w_bootloader_b_s132.hex

When that has been done, let's flash the bootloader built by us (pay
attention to the sectorerase instead of chiperase here)::

   nrfjprog --family nrf52 --sectorerase --program ./examples/dfu/bootloader/pca10040/dual_bank_ble_s132/armgcc/_build/nrf52832_xxaa_s132.hex

When this is done, simply load the
``examples/dfu/bootloader/pca10040/dual_bank_ble_s132/armgcc/_build/nrf52832_xxaa_s132.out``
file in GDB as described above, and you're good to go
(bootloader_init() is a good function to put a breakpoint at for boot
loader debugging).

Applications and runtimes for Nitrogen
--------------------------------------

Micropython
~~~~~~~~~~~

MicroPython is a tiny implementation of `Python 3
<http://www.python.org/>`_ optimised to run on microcontrollers and in
constrained environments. It can target a variety of runtime
environments ranging from bare metal to a full-fledged Unix-like
userspace and, most importantly for Nitrogen, there is an out-of-tree
zephyr port. The out-of-tree port comes from `Paul Sokolovsky
<https://github.com/pfalcon/micropython>`_ but Paul is so busy hacking
to get networking working that his tree sometimes exceeds the memory
limits of the Nitrogen board so we recommend using Daniel's tree
instead.

Assuming you already have have sourced zephyr-env.sh and setup a
toolset (Zephyr SDK v0.8.2 is known to work) then building Micropython
is trivial::

    git clone https://github.com/daniel-thompson/micropython.git -b zephyr
    cd micropython/zephyr
    make BOARD=nrf52_nitrogen
    pyocd-flashtool -t nrf52  outdir/nrf52_nitrogen/zephyr.hex

.. note::

   The micropython build system requires zephyr >= 1.6.0.

JerryScript
~~~~~~~~~~~

JerryScript is a lightweight JavaScript engine intended to run on a
very constrained devices such as microcontrollers. There is already an
upstream zephyr port, although there is still a pending pull request
to make it work with the latest Zephyr SDK (once this is accepted we
will update the below instructions to point at the upstream
jerryscript sources).

As with Micropython you need to have sourced zephyr-env.sh and setup a
toolset (Zephyr SDK v0.8.2 is known to work) before building the
binaries::

    git clone https://github.com/daniel-thompson/jerryscript.git -b zephyr
    cd jerryscript
    make -f targets/zephyr/Makefile.zephyr BOARD=nrf52_nitrogen
    sudo pyocd-flashtool -t nrf52 build/nrf52_nitrogen/zephyr/zephyr.hex
