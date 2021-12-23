.. _gs-install-fioctl:

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

.. _gs-fioctl-installation:

Installation
############

.. _gs-fioctl-manual-install:

Manual Installation
^^^^^^^^^^^^^^^^^^^

We use `Github Releases`_ to distribute static X86_64 golang binaries.

.. tabs::

   .. group-tab:: Linux

      1. Download a Linux binary from the `Github Releases`_ page to a directory
         on your ``PATH``, make sure you have Curl installed

         For example, to download version |fioctl_version| on Linux, define the 
         version:

         .. parsed-literal::

              FIOCTL_VERSION="|fioctl_version|"

         Download the binary with curl:

         .. prompt:: bash host:~$, auto

            host:~$ sudo curl -o /usr/local/bin/fioctl -LO https://github.com/foundriesio/fioctl/releases/download/$FIOCTL_VERSION/fioctl-linux-amd64

      2. Make the :ref:`ref-fioctl` binary executable:

         .. prompt:: bash host:~$, auto

            host:~$ sudo chmod +x /usr/local/bin/fioctl

      You can execute this again in future to overwrite your binary, therefore
      updating or changing your version.

   .. group-tab:: macOS

      1. Download a Darwin binary from the `Github Releases`_ page to a directory
         on your ``PATH``, make sure you have Curl installed

         For example, to download version |fioctl_version| on macOS, define the 
         version:

         .. parsed-literal::

              FIOCTL_VERSION="|fioctl_version|"

         Download the binary with curl:

         .. prompt:: bash host:~$, auto

            host:~$ curl -o /usr/local/bin/fioctl -LO https://github.com/foundriesio/fioctl/releases/download/$FIOCTL_VERSION/fioctl-darwin-amd64
        
         .. note::
        
            For MacOS running on a Apple M1 processor, replace
            ``fioctl-darwin-amd64`` with ``fioctl-darwin-arm64``, and set
            ``FIOCTL_VERSION`` to v0.21 or newer.

      2. Make the :ref:`ref-fioctl` binary executable:

         .. prompt:: bash host:~$, auto

            host:~$ sudo chmod +x /usr/local/bin/fioctl

      You can execute this again in future to overwrite your binary, therefore
      updating or changing your version.

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

         ``C:\Users\Gavin\Desktop\fio\bin``

      You should now be able to open ``cmd.exe`` or ``powershell.exe`` and type
      ``fioctl``.

.. _gs-fioctl-package-install:

Install From Source
^^^^^^^^^^^^^^^^^^^

.. note::

    This requires that you have Golang installed. See
    https://golang.org/doc/install for instructions.

If you intend to use Fioctl on a non X86_64 platform (like a Raspberry
Pi/Pinebook/Smartphone) such as ARM, RISC-V, PPC, etc. Fioctl can be compiled
and installed from the latest sources and installed via Golang's own package
manager; ``go get``:

.. prompt:: bash host:~$, auto

   host:~$ go get github.com/foundriesio/fioctl

.. _gs-fioctl-authenticate-fioctl:

Authenticate fioctl
###################
Now that :ref:`ref-fioctl` is installed, you must authenticate with our backend
before you're able to use it. This requires you to generate OAuth2 application
credentials for interacting with Factory APIs:

.. prompt:: bash host:~$, auto

   host:~$ fioctl login
     Please visit:
     
     https://app.foundries.io/settings/tokens/
     
     and create a new "Application Credential" to provide inputs below.
     
     Client ID:

:ref:`ref-fioctl` will now ask for your Client ID and Secret. Follow the next steps to generate it.

Application Credentials
^^^^^^^^^^^^^^^^^^^^^^^

Go to `Tokens <https://app.foundries.io/settings/tokens/>`_ and create a new **Application Credentials** by clicking on 
:guilabel:`+ New Credentials`.

.. figure:: /_static/install-fioctl/application_credentials.png
   :width: 900
   :align: center

   Application Credentials

Complete with a **Description** and the **Expiration date** and select :guilabel:`next`.

For fioctl, check the :guilabel:`Use for tools like fioctl` box and 
select your **Factory**. Remember that you can revoke this access and set up a new credential later once you are
familiar with the :ref:`ref-api-access`.

.. figure:: /_static/install-fioctl/fioctl_token.png
   :width: 500
   :align: center

   API Token

.. tip::

   We recommend creating a new API token for each device you plan to use our
   tools with. For example, if you intend to develop on multiple systems such
   as a laptop and a desktop, you should create a new token for each, just as
   you would with SSH keys. This way you can revoke tokens for individual systems,
   should they be compromised.

Use the Client ID and Secret to finish the fioctl login.

.. figure:: /_static/install-fioctl/token.png
   :width: 500
   :align: center

   Client ID and Secret 

.. prompt:: bash host:~$, auto

   host:~$ fioctl login
     Please visit:
     
     https://app.foundries.io/settings/tokens/
     
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

.. note::
   Refer to the :ref:`ref-fioctl` section of the documentation to learn more
   about configuration.

.. _AUR Package: https://aur.archlinux.org/packages/fioctl-bin
.. _Scoop: https://scoop.sh/
.. _WSL: https://docs.microsoft.com/en-us/windows/wsl/install-win10
.. _launchpad: https://launchpad.net/~fio-maintainers/+archive/ubuntu/ppa
.. _Github Releases: https://github.com/foundriesio/fioctl/releases
.. _Formula: https://github.com/foundriesio/homebrew-fioctl
