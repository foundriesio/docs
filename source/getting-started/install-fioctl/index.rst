.. _ref-install-fioctl:

Fioctl CLI Installation |:package:|
===================================

:ref:`ref-fioctl` is a simple tool that interacts with the Foundries.io REST API
for managing a Factory. It is based on the `"ota-lite" API
<https://app.swaggerhub.com/apis/foundriesio/ota-lite/>`_, also made by
Foundries.

:ref:`ref-fioctl`, is used to manage:

- :ref:`Tags (per device, and per Factory) <ref-advanced-tagging>`
- :ref:`Device configuration <ref-fioconfig>`
- :ref:`OTA updates <ref-aktualizr-lite>`
- :ref:`CI Secrets <ref-container-secrets>`

Installation
------------

Via Package Manager (Recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. tabs::

   .. group-tab:: Ubuntu/Debian
      
      We maintain a PPA on launchpad_.

        .. code-block:: shell
           
           sudo add-apt-repository ppa:fio-maintainers/ppa
           sudo apt-get update
           sudo apt-get install fioctl

   .. group-tab:: macOS

      We maintain a brew Formula
 
        .. code-block:: shell    

           brew install fioctl

   .. group-tab:: Windows
     
        .. note:: 
           We recommend using either the WSL_ or Chocolatey_ to manage your
           :ref:`ref-fioctl` installation.
      
        **Via Chocolatey**
         
        1. Install Chocolatey_ 
        2. Run ``cmd.exe`` as Administrator
        3. Run ``choco install fioctl``

        **Via Windows Subsystem for Linux (WSL)**

        1. Enable the WSL_
        2. `Install a supported Linux Distribution
           <https://docs.microsoft.com/en-us/windows/wsl/install-win10#install-your-linux-distribution-of-choice>`_
           such as Ubuntu, Debian.
        3. Launch a shell via WSL, usually bash.exe is available from the start
           menu.
        4. You can now follow our docs as if you were running Linux, refer to
           the Ubuntu/Debian installation steps.

   .. group-tab:: Arch Linux
     
      We maintain an `AUR Package`_

      **Via yay**

        .. code-block:: shell
           
          yay -S fioctl
     
      **Or via makepkg**

        .. code-block:: shell
           
          git clone https://aur.archlinux.org/fioctl-bin.git
          cd fioctl-bin
          makepkg -si

