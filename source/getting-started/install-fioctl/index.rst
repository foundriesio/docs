.. _ref-install-fioctl:

Fioctl CLI Installation
=======================

:ref:`ref-fioctl` is a simple tool that interacts with the Foundries.io REST API
for managing a Factory. It is based on the `ota-lite API
<https://api.foundries.io/ota/>`_, also built by Foundries.io.

:ref:`ref-fioctl`, is used to manage:

- :ref:`Tags (per device, and per Factory) <ref-advanced-tagging>`
- :ref:`Device configuration <ref-fioconfig>`
- :ref:`OTA updates <ref-aktualizr-lite>`
- :ref:`CI Secrets <ref-container-secrets>`

Installation
------------

Via Package Manager
^^^^^^^^^^^^^^^^^^^

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

Manual Installation
^^^^^^^^^^^^^^^^^^^

We use `Github Releases`_ to distribute static golang binaries. If you don't have a
package manager, are not on a supported distribution, or would prefer to install
manually, you can refer to this section for manual installation instructions.

.. tabs::

   .. group-tab:: Linux

      1. Download a Linux binary from the `Github Releases`_ page.
      2. Put it in a folder of your choosing.
      3. Add that folder to your ``$PATH``. e.g ``~/.bashrc`` for bash or
         ``~/.zshrc`` for zsh.

         An example path string if installing to the home directory would look
         like this: ``PATH="/home/stetson/fio/bin/:$PATH"``

      We provide a script that implements those steps below. It assumes you want
      to use a folder in your your home directory. Replace ``INSTALL_DIR`` with the
      directory in your ``$HOME`` that you'd like to put your Foundries.io application
      into. Additionally, you can change ``FIOCTL_VERSION`` to set the version of
      :ref:`ref-fioctl` you'd like to install. If you use this script as is,
      :ref:`ref-fioctl` will be installed to ``~/fio/bin/fioctl``, and it will be
      added to your ``$PATH`` as long as you are using either ``zsh`` or ``bash`` as
      your shell.

        .. code-block:: shell

           INSTALL_DIR=fio
           FIOCTL_VERSION="0.10"

           mkdir -p ~/$INSTALL_DIR/bin
           wget https://github.com/foundriesio/fioctl/releases/download/$FIOCTL_VERSION/fioctl-linux-amd64 -O ~/$INSTALL_DIR/bin/fioctl
           chmod +x $INSTALL_DIR/bin/fioctl

           if [ $SHELL == '/bin/bash' ]
           then
             echo "PATH=\"$HOME/$INSTALL_DIR/bin/:\$PATH\"" >> ~/.bashrc
             source ~/.bashrc
           elif [ $SHELL == '/bin/zsh' ]
           then
             echo "PATH=\"$HOME/$INSTALL_DIR/bin/:\$PATH\"" >> ~/.zshrc
             source ~/.zshrc
           fi

   .. group-tab:: macOS

      1. Download a Darwin binary from the `Github Releases`_ page.
      2. Put it in a folder of your choosing.
      3. Add that folder to your ``$PATH``. e.g ``~/.bashrc`` for bash or
         ``~/.zshrc`` for zsh.

         An example path string if installing to the home directory would look
         like this. ``PATH="/Users/stetson/fio/bin/:$PATH"``

      We provide a script that implements those steps below. It assumes you want
      to use a folder in your your home directory. Replace ``INSTALL_DIR`` with the
      directory in your ``$HOME`` that you'd like to put your Foundries.io application
      into. Additionally, you can change ``FIOCTL_VERSION`` to set the version of
      :ref:`ref-fioctl` you'd like to install. If you use this script as is, fioctl will
      be installed to ``~/fio/bin/fioctl``, and it will be added to your ``$PATH`` as
      long as you are using either ``zsh`` or ``bash`` as your shell.

        .. code-block:: shell

           INSTALL_DIR=fio
           FIOCTL_VERSION="0.10"

           mkdir -p ~/$INSTALL_DIR/bin
           wget https://github.com/foundriesio/fioctl/releases/download/$FIOCTL_VERSION/fioctl-darwin-amd64 -O ~/$INSTALL_DIR/bin/fioctl
           chmod +x $INSTALL_DIR/bin/fioctl

           if [ $SHELL == '/bin/bash' ]
           then
             echo "PATH=\"$HOME/$INSTALL_DIR/bin/:\$PATH\"" >> ~/.bashrc
             source ~/.bashrc
           elif [ $SHELL == '/bin/zsh' ]
           then
             echo "PATH=\"$HOME/$INSTALL_DIR/bin/:\$PATH\"" >> ~/.zshrc
             source ~/.zshrc
           fi

   .. group-tab:: Windows

      1. Download a Windows binary from the `Github Releases`_ page.
      2. Put it in a folder of your choosing and rename it to ``fioctl.exe``
      3. Press ``Win + R`` and type ``SystemPropertiesAdvanced``
      4. Press ``enter`` or click ``OK``.
      5. Click "Environment Variables..." in the resultant menu..
      6. Click the ``Path`` **system** variable, then click ``Edit...``
      7. Click ``New`` in the "Edit environment variable" menu.
      8. Enter the path to the folder in which you have placed :ref:`ref-fioctl`.

         An example path string if installing to a folder on the desktop would
         look like this.

         ``C:\Users\Stetson\Desktop\fio\bin``

      You should now be able to open ``cmd.exe`` or ``powershell.exe`` and type
      ``fioctl``.

Post-Install
^^^^^^^^^^^^
Now that :ref:`ref-fioctl` is installed, you must authenticate with our backend
before you're able to use it. This requires you to generate OAuth2 application
credentials for interacting with Factory APIs::

  fioctl login

:ref:`ref-fioctl` will now ask for your API token and walk you through the
authentication process.

.. note:: Tokens can be generated at https://app.foundries.io/settings/tokens

.. tip::

   We recommend creating a new API token for each device you plan to use our
   tools with. For example, if you intend to develop on multiple systems such
   as a laptop and a desktop, you should create a new token for each, just as
   you would with SSH keys. This way you can revoke tokens for individual systems,
   should they be compromised.

Configuration
-------------

.. note::
   Refer to the :ref:`ref-fioctl` section of the documentation to learn more
   about configuration.

.. _AUR Package: https://aur.archlinux.org/packages/fioctl-bin
.. _Chocolatey: https://chocolatey.org/install
.. _WSL: https://docs.microsoft.com/en-us/windows/wsl/install-win10
.. _launchpad: https://launchpad.net/~fio-maintainers/+archive/ubuntu/ppa
.. _Github Releases: https://github.com/foundriesio/fioctl/releases

.. todo:: Document M2M Services

.. todo:: Create Brew, Chocolatey, PPA packages for installation
