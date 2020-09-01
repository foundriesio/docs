.. _ref-cortex-m_p1:

Get Started with NxP i.MX8 Cortex-M - First Example
===================================================

When developing a new product using Embedded Linux, it is quite common to face challenges such as high power consumption and real-time tasks control and determinism. These are the main reasons why several products end up having an architecture with both c and Microcontroller on the same board.

Using a processor and a microcontroller on the same board brings complexity to the hardware and it is necessary to establish communication between both of them. Also, once they are physically divided, any hardware change related to peripherals becomes complicated as it is necessary to redesign and produce a new hardware.

In recent years, major CHIP vendors have begun bringing a cheaper and more convenient solution to previously reported problems, the Heterogeneous Multicore.

The Heterogeneous Multicore comes not just with processors but also brings small microcontrollers directly manufactured in the same SOC, such as a Cortex-A with a Cortex-M.

The idea is very good and in some cases both cores share interfaces such as GPIO, I2C, SPI and others. Therefore, it is possible to control a certain peripheral with the microcontroller and if there is a design change where the processor wants to use that peripheral, it is possible to make this change without the need for hardware change by just changing the software.

In situations where power consumption is essential, it is possible to leave the microcontroller operating while the processor enters in a lower power mode. For real-time activities, it is possible to leave the microcontroller performing precise activities while the processor runs its operating system like Linux without major commitments.

This solution can help a lot, but there is still a lot of discussion about this in relation to high risk activities such as life support products. Leaving critical activities for the microprocessor may not be a good idea in this case since many heterogeneous architectures share the power management unit and depending on the bug, it could end up restarting both cores.

In this tutorial, we will talk about the NxP i.MX8 mini processor. This is one of the heterogeneous multi core examples where you can find processos with 1x / 2x / 4x Arm Cortex-A53 and microcontrollers like the Arm Cortex-M4 in the same SOC. I will show you the first steps to compile, load and run a binary for the Cortex-M4 through u-boot.

   .. figure:: /_static/tutorials/cortex-m_p1/image1.png
      :alt: Add user
      :align: center
      :width: 6in

      i.MX 8M Mini Family Block Diagram

Because it is a relatively new architecture, many of who use Cortex-M4 compile their binary, copy it into the Linux file system used by the Cortex-A and when turning on the product, use u-boot to load and start the microcontroller.

This is the most common way to do it. However, no security measures are applied during the firmware deployment and usually the firmware update is just a remote replacement with the new one.

With your FoundriesFactory and using Linux microPlatform, you can incorporate your firmware with your fitImage and thus use all the over-the-air update and version control infrastructure already implemented on your FondriesFactory to manage your firmware development.

In this series of tutorials, I will show you how to get started with Cortex-M4 by compiling and run the first example, how to customize your Linux microPlatform to incorporate the firmware to the fitImage as well as automate the initialization of it during the boot and finally how to make the communication between Cortex-M4 and Cortex-A.

The Evaluation Board we will be using is the i.MX 8M Mini EVK from NXP.

   .. figure:: /_static/tutorials/cortex-m_p1/image2.png
      :alt: Add user
      :align: center
      :width: 6in

      NXP i.MX 8M Mini EVK



Downloading the MCUXpreesso SDK
-------------------------------

The first thing we will need is the MCUXpresso SDK builder with all the examples, middleware and drivers for its development.

`MCUXpreesso SDK`_

You will need to be logged in to the NXP website in order to download it. Once logged in, go to:

Select Development Board

Search for: ``EVK-MIMX8MM``

Then select: ``Build MCUXpresso SDK``

On the next page, select multicore and FreeRTOS and press Download SDK.

   .. figure:: /_static/tutorials/cortex-m_p1/image3.png
      :alt: Add user
      :align: center
      :width: 6in

      Download MCUXpreesso SDK

Extract the SDK to your preferred folder and inside it, search for ``docs/Getting Started with MCUXpresso SDK for EVK-MIMX8MM.pdf``

Downloading GCC Toolchain
-------------------------

According to chapter 5.1, download the GCC Toolchain. In my case, I will download the `gcc-arm-none-eabi-9-2020-q2`_.

Download the file corresponding to your architecture. In my case: ``gcc-arm-none-eabi-9-2020-q2-update-x86_64-linux.tar.bz2``

Extract the toolchain with the command::

 tar -xf gcc-arm-none-eabi-9-2019-q4-major-x86_64-linux.tar.bz2

Whenever you are going to compile an application for Cortex-M on a given terminal, you need to export the variable ``ARMGCC_DIR`` pointing to the toolchain directory. If you close the terminal and open another one, you will need to execute this command again::

 export ARMGCC_DIR =/home/prjs/m4_tutorial/gcc-arm-none-eabi-9-2019-q4-major/

Compiling the First Example
---------------------------

All examples are in the folder ``SDK_2.8.0_EVK-MIMX8MM/boards/evkmimx8mm/``

The first example that we will compile and test is inside ``SDK_2.8.0_EVK-MIMX8MM/boards/ evkmimx8mm/demo_apps/hello_world/``::

 cd SDK_2.8.0_EVK-MIMX8MM/boards/evkmimx8mm/demo_apps/hello_world/
 code.

hello_world.c::

      /*
      * Copyright (c) 2013 - 2015, Freescale Semiconductor, Inc.
      * Copyright 2016-2017 NXP
      * All rights reserved.
      *
      * SPDX-License-Identifier: BSD-3-Clause
      */

      #include "fsl_device_registers.h"
      #include "fsl_debug_console.h"
      #include "board.h"

      #include "pin_mux.h"
      #include "clock_config.h"
      /*******************************************************************************
      * Definitions
      ******************************************************************************/


      /*******************************************************************************
      * Prototypes
      ******************************************************************************/

      /*******************************************************************************
      * Code
      ******************************************************************************/
      /*!
      * @brief Main function
      */
      int main(void)
      {
            char ch;

            /* Init board hardware. */
            /* Board specific RDC settings */
            BOARD_RdcInit();

            BOARD_InitPins();
            BOARD_BootClockRUN();
            BOARD_InitDebugConsole();
            BOARD_InitMemory();

            PRINTF("hello world.\r\n");

            while (1)
            {
                  ch = GETCHAR();
                  PUTCHAR(ch);
            }
      }

As you can see, the example is very simple and can be compiled with the following commands::

      cd armgcc/
      export ARMGCC_DIR=/home/prjs/m4_tutorial/gcc-arm-none-eabi-9-2019-q4-major/
      ./build_release.sh 
      -- TOOLCHAIN_DIR: /home/prjs/m4_tutorial/gcc-arm-none-eabi-9-2019-q4-major/
      CMake Deprecation Warning at /usr/share/cmake/Modules/CMakeForceCompiler.cmake:72 (message):
      The CMAKE_FORCE_C_COMPILER macro is deprecated.  Instead just set
      CMAKE_C_COMPILER and allow CMake to identify the compiler.
      Call Stack (most recent call first):
      /home/prjs/m4_tutorial/SDK_2.8.0_EVK-MIMX8MM/tools/cmake_toolchain_files/armgcc.cmake:33 (CMAKE_FORCE_C_COMPILER)
      /usr/share/cmake/Modules/CMakeDetermineSystem.cmake:90 (include)
      ...
      ...
      ... 
      -- Configuring done
      -- Generating done
      -- Build files have been written to: /home/prjs/m4_tutorial/SDK_2.8.0_EVK-MIMX8MM/boards/evkmimx8mm/demo_apps/hello_world/armgcc
      Scanning dependencies of target hello_world.elf
      [  5%] Building C object CMakeFiles/hello_world.elf.dir/home/prjs/m4_tutorial/SDK_2.8.0_EVK-MIMX8MM/boards/evkmimx8mm/demo_apps/hello_world/board.c.obj
      ...
      ...
      ...
      [ 95%] Building C object CMakeFiles/hello_world.elf.dir/home/prjs/m4_tutorial/SDK_2.8.0_EVK-MIMX8MM/devices/MIMX8MM6/system_MIMX8MM6_cm4.c.obj
      [100%] Linking C executable release/hello_world.elf
      [100%] Built target hello_world.elf
      cd armgcc/
      export ARMGCC_DIR=/home/prjs/m4_tutorial/gcc-arm-none-eabi-9-2019-q4-major/
      ./build_release.sh 
      -- TOOLCHAIN_DIR: /home/prjs/m4_tutorial/gcc-arm-none-eabi-9-2019-q4-major/
      CMake Deprecation Warning at /usr/share/cmake/Modules/CMakeForceCompiler.cmake:72 (message):
      The CMAKE_FORCE_C_COMPILER macro is deprecated.  Instead just set
      CMAKE_C_COMPILER and allow CMake to identify the compiler.
      Call Stack (most recent call first):
      /home/prjs/m4_tutorial/SDK_2.8.0_EVK-MIMX8MM/tools/cmake_toolchain_files/armgcc.cmake:33 (CMAKE_FORCE_C_COMPILER)
      /usr/share/cmake/Modules/CMakeDetermineSystem.cmake:90 (include)
      ...
      ...
      ... 
      -- Configuring done
      -- Generating done
      -- Build files have been written to: /home/prjs/m4_tutorial/SDK_2.8.0_EVK-MIMX8MM/boards/evkmimx8mm/demo_apps/hello_world/armgcc
      Scanning dependencies of target hello_world.elf
      [  5%] Building C object CMakeFiles/hello_world.elf.dir/home/prjs/m4_tutorial/SDK_2.8.0_EVK-MIMX8MM/boards/evkmimx8mm/demo_apps/hello_world/board.c.obj
      ...
      ...
      ...
      [ 95%] Building C object CMakeFiles/hello_world.elf.dir/home/prjs/m4_tutorial/SDK_2.8.0_EVK-MIMX8MM/devices/MIMX8MM6/system_MIMX8MM6_cm4.c.obj
      [100%] Linking C executable release/hello_world.elf
      [100%] Built target hello_world.elf


After compiling it, the binary ``hello_world.bin`` file will be generated in the release folder.::

      ls -l release/
      total 36
      -rwxrwxr-x. 1 munoz0raul munoz0raul   6364 Aug 20 20:01 hello_world.bin
      -rwxrwxr-x. 1 munoz0raul munoz0raul 146272 Aug 20 20:01 hello_world.elf

Loading the binary on Cortex-M4
-------------------------------

There are several ways to get this file to u-boot to start the Cortex-M4. As mentioned at the beginning of the tutorial, copying to the Cortex-A file system is the easiest way to perform the first tests.

From that step, we assume that you already have an iMX8 EVK with Linux microPlatform installed in your development kit.

The i.MX 8M Mini EVK has a micro USB debug connector which, when connected to your computer, will display two serial interfaces, ttyUSB0 and ttyUSB1. Those interfaces are connected to UART2 and UART4 and will be used to interact with the Cortex-A (Linux) and the Cortex-M (Firmware).

Connect the micro USB connector and open two terminals with the respective interfaces using 115200 bandrate.

Terminal 1::

      sudo picocom -b 115200 /dev/ttyUSB0

Terminal 2::

      sudo picocom -b 115200 /dev/ttyUSB1

Connect the board to the network so that you have access to the internet and also local access via SSH.

Turn on the device and wait for the boot:

   .. figure:: /_static/tutorials/cortex-m_p1/image4.png
      :alt: Add user
      :align: center
      :width: 12in

      Terminal

In my case, ttyUSB1 is the terminal used to handle u-boot and Linux.

On a third terminal, copy the binary to the iMX8 EVK using scp::

      scp release/hello_world.bin fio@192.168.15.87:~
      The authenticity of host '192.168.15.87 (192.168.15.87)' can't be established.
      ECDSA key fingerprint is SHA256:7WWq+MG7JrwZUG17caY3no7swspa+rvprAat/ndF4Fg.
      Are you sure you want to continue connecting (yes/no)? yes
      Warning: Permanently added '192.168.15.87' (ECDSA) to the list of known hosts.
      fio@192.168.15.87's password: 
      hello_world.bin                                                                                                                            100% 6364     2.2MB/s   00:00  

      In the ttyUSB1 serial terminal that gives you access to linux, find the file at home and copy it to the /boot/loader folder with sudo:

      fio@imx8mmevk:~$ ls
      hello_world.bin
      fio@imx8mmevk:~$ sudo hello_world.bin /boot/loader/

Restart the device and be ready to stop u-boot by pressing any key at the start of the boot::

      fio@imx8mmevk:~$ sudo reboot
      Password: 
            Stopping Session c1 of user fio.
      [  OK  ] Removed slice system-modprobe.slice.
      [  OK  ] Removed slice system-sshd.slice.
      [  OK  ] Unmounted /var
      ...
      ...
      ...
      Hit any key to stop autoboot:  0 
      u-boot=> 
      u-boot=> 
      u-boot=> 

In u-boot, we will need to load the binary and start Cortex-M4. To debug the Cortex-M4, it is interesting to leave the terminal ttyUSB0 and ttyUSB1 opened side by side.

Run the commands on u-boot and see the result on the other terminal that is configured to interact with Cortex-M4

Terminal 1::

      u-boot=> ext4load mmc 2:2 0x48000000 /boot/loader/hello_world.bin
      6364 bytes read in 14 ms (443.4 KiB/s)
      u-boot=> cp.b 0x48000000 0x7e0000 0x20000
      u-boot=> bootaux 0x7e0000
      ## Starting auxiliary core at 0x007E0000 ...
      u-boot=> 

Terminal 2::

      Terminal ready
      hello world.


.. figure:: /_static/tutorials/cortex-m_p1/image5.png
   :alt: Add user
   :align: center
   :width: 12in

   Hello World

Conclusion and What comes Next
------------------------------

As you can see, example 1 was executed and the outputs were destined for the second UART.
Several other examples such as GPIO, I2C, FreeRTOS among others are available in the same folder structure.

In the next part, we will explain how to change your FoundriesFactory to embed the firmware together with fitImage and configure u-boot to automatically load the file from fitImage. Last but not least, we will also explain how to communicate between the Cortex-M and Cortex-A.
      
.. _MCUXpreesso SDK:
   https://mcuxpresso.nxp.com/en/welcome

.. _gcc-arm-none-eabi-9-2020-q2:
   https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads


      
