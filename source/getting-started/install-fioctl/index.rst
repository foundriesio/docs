.. _gs-install-fioctl:

Fioctl CLI Installation
=======================

:ref:`ref-fioctl` is a simple tool for interacting with the Foundries.io REST API.

.. seealso::
   Fioctl is based on Foundries.io's  `ota-lite API <https://api.foundries.io/ota/>`_.

:ref:`ref-fioctl`, is used to manage:

- :ref:`Tags (per device, and per Factory) <ref-advanced-tagging>`
- :ref:`Device configuration <ref-fioconfig>`
- :ref:`OTA updates <ref-aktualizr-lite>`
- :ref:`CI Secrets <ref-container-secrets>`

.. _gs-fioctl-installation:

Installation
############

.. note::
   For installing on platforms outside of x86-64 and Apple's M1, you will need to :ref:`install from source <gs-fioctl-package-install>`.

.. _gs-fioctl-manual-install:

Manual Installation
^^^^^^^^^^^^^^^^^^^

We use `Github Releases`_ to distribute static golang binaries.

.. tip::
   Repeating the following steps will overwrite an existing binary, useful for updating or changing version.

.. tabs::

   .. group-tab:: Linux
      
      .. attention::
        Make sure you have Curl installed.

      1. Download a Linux binary to a directory on your ``PATH``.

         For example, to download version |fioctl_version| on Linux, define the version:

         .. parsed-literal::

              FIOCTL_VERSION="|fioctl_version|"

         Download the binary with curl:

         .. prompt:: bash host:~$, auto

            host:~$ sudo curl -o /usr/local/bin/fioctl -LO https://github.com/foundriesio/fioctl/releases/download/$FIOCTL_VERSION/fioctl-linux-amd64

      2. Make the :ref:`ref-fioctl` binary executable:

         .. prompt:: bash host:~$, auto

            host:~$ sudo chmod +x /usr/local/bin/fioctl

   .. group-tab:: macOS
      
      .. attention::
        Make sure you have Curl installed.

      1. Download a Darwin binary from the `Github Releases`_ page to a directory on your ``PATH``.

         For example, to download version |fioctl_version| on macOS, define the version:

         .. parsed-literal::

              FIOCTL_VERSION="|fioctl_version|"

         Download the binary with curl:

         .. prompt:: bash host:~$, auto

            host:~$ curl -o /usr/local/bin/fioctl -LO https://github.com/foundriesio/fioctl/releases/download/$FIOCTL_VERSION/fioctl-darwin-amd64
        
         .. important::
        
            For MacOS running on a Apple M1 processor, replace ``fioctl-darwin-amd64`` with ``fioctl-darwin-arm64``, and set ``FIOCTL_VERSION`` to v0.21 or newer.

      2. Make the :ref:`ref-fioctl` binary executable:

         .. prompt:: bash host:~$, auto

            host:~$ sudo chmod +x /usr/local/bin/fioctl


   .. group-tab:: Windows

      1. Download a Windows binary from the `Github Releases`_ page.
      2. Put it in a folder of your choosing and rename it to ``fioctl.exe``
      3. Press ``Win + R`` and type ``SystemPropertiesAdvanced``
      4. Press ``enter`` or click ``OK``.
      5. Click "Environment Variables..." in the resultant menu..
      6. Click the ``Path`` **system** variable, then click ``Edit...``
      7. Click ``New`` in the "Edit environment variable" menu.
      8. Enter the path to the folder in which you have placed :ref:`ref-fioctl`.

         An example path string if installing to a folder on the desktop would look like this.

         ``C:\Users\Gavin\Desktop\fio\bin``

      You should now be able to open ``cmd.exe`` or ``powershell.exe`` and type
      ``fioctl``.

.. _gs-fioctl-package-install:

Install From Source
^^^^^^^^^^^^^^^^^^^

.. attention::

    This requires that you have `Golang installed <https://golang.org/doc/install>`_.

Fioctl can be compiled and installed from the latest source via Golang's own package manager; ``go get``:

.. prompt:: bash host:~$, auto

   host:~$ go get github.com/foundriesio/fioctl

.. _gs-fioctl-authenticate-fioctl:

Authenticate fioctl
###################

With :ref:`ref-fioctl` installed, authenticate it with our backend.
For this, you will generate OAuth2 application credentials for interacting with the FoundriesFactory API:

.. prompt:: bash host:~$, auto

   host:~$ fioctl login
     Please visit:

     https://app.foundries.io/settings/credentials/

     and create a new "Application Credential" to provide inputs below.
     
     Client ID:

:ref:`ref-fioctl` will now ask for your Client ID and Secret. Follow the next steps to generate it.

Application Credentials
^^^^^^^^^^^^^^^^^^^^^^^

Go to `Application Credentials <https://app.foundries.io/settings/credentials/>`_ and click on :guilabel:`+ New Credentials`.

.. figure:: /_static/install-fioctl/application_credentials.png
   :width: 900
   :align: center

   Application Credentials

Complete with a **Description** and the **Expiration date** and select :guilabel:`next`.

For fioctl, check the :guilabel:`Use for tools like fioctl` box and select your **Factory**.
You can revoke this access and set up a new credential later once you are familiar with the :ref:`ref-api-access`.

.. figure:: /_static/install-fioctl/fioctl_token.png
   :width: 500
   :align: center

   API Token

.. tip::

   We recommend creating a new API token for each computer you plan to use our tools with.
   For example, if you intend to develop on both a laptop and a desktop, create a new token for each, as you would with SSH keys.
   This way you can revoke tokens for individual systems, should they be compromised.

Use the Client ID and Secret to finish the fioctl login.

.. figure:: /_static/install-fioctl/token.png
   :width: 500
   :align: center

   Client ID and Secret 

.. prompt:: bash host:~$, auto

   host:~$ fioctl login
     Please visit:

     https://app.foundries.io/settings/credentials/

     and create a new "Application Credential" to provide inputs below.
     
     Client ID:
     Client secret:
     You are now logged in to Foundries.io services.

.. _gs-fioctl-configuration:

Configuration
#############

When working with multiple factories, specifying a factory name is mandatory.
It can be set using 3 different methods:

   * Argument:

     .. prompt:: bash host:~$, auto

        host:~$ fioctl targets list --factory <factory>

   *  Environment Variable:

     .. prompt:: bash host:~$, auto

        host:~$ export FIOCTL_FACTORY=<factory>
        host:~$ fioctl targets list

   *  Configuration File:

     .. prompt:: bash host:~$, auto

        host:~$ echo "factory: <factory>" >> $HOME/.config/fioctl.yaml
        host:~$ fioctl targets list

.. seealso::
   :ref:`ref-fioctl` documentation.

.. _AUR Package: https://aur.archlinux.org/packages/fioctl-bin
.. _Scoop: https://scoop.sh/
.. _WSL: https://docs.microsoft.com/en-us/windows/wsl/install-win10
.. _launchpad: https://launchpad.net/~fio-maintainers/+archive/ubuntu/ppa
.. _Github Releases: https://github.com/foundriesio/fioctl/releases
.. _Formula: https://github.com/foundriesio/homebrew-fioctl
