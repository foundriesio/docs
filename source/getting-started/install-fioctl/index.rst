.. _gs-install-fioctl:

Installing Fioctl
=================

:ref:`Fioctl™ <ref-fioctl>` is a simple tool for interacting with the Foundries.io™ REST API.

.. seealso::
   Fioctl is based on Foundries.io's  `ota-lite API <https://api.foundries.io/ota/>`_.

:ref:`ref-fioctl` is used to manage:

- :ref:`Tags (per device, per device group and per Factory) <ref-advanced-tagging>`
- :ref:`Device Configuration <ref-fioconfig>`
- :ref:`OTA Updates <ref-aktualizr-lite>`
- :ref:`CI Secrets <ref-container-secrets>`
- :ref:`Offline TUF Keys <ref-offline-keys>`
- :ref:`Git Access <gs-git-config>`

.. _gs-fioctl-installation:

Installation
############

.. _gs-fioctl-manual-install:

Manual Installation
^^^^^^^^^^^^^^^^^^^

We use `GitHub Releases`_ to distribute static golang binaries.

.. tip::
   Fioctl v0.36 and later has an auto-update feature.
   Run ``fioctl version`` to check for an update, then run ``fioctl version --update-to <version>``.
   For more details checkout the :ref:`Fioctl user guide <ug-fioctl>`.

.. tabs::

   .. group-tab:: Linux

      .. attention::
        Make sure you have ``curl`` installed.

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
        Make sure you have ``curl`` installed.

      1. Download a Darwin binary from the `GitHub Releases`_ page to a directory on your ``PATH``.

         For example, to download version |fioctl_version| on macOS, define the version:

         .. parsed-literal::

              FIOCTL_VERSION="|fioctl_version|"

         Download the binary with curl:

         .. prompt:: bash host:~$, auto

            host:~$ sudo curl -o /usr/local/bin/fioctl -L https://github.com/foundriesio/fioctl/releases/download/$FIOCTL_VERSION/fioctl-darwin-amd64

         .. important::

            For MacOS running on a Apple M1 processor, replace ``fioctl-darwin-amd64`` with ``fioctl-darwin-arm64``, and set ``FIOCTL_VERSION`` to v0.21 or newer.

      2. Make the :ref:`ref-fioctl` binary executable:

         .. prompt:: bash host:~$, auto

            host:~$ sudo chmod +x /usr/local/bin/fioctl


   .. group-tab:: Windows

      1. Download a Windows binary from the `GitHub Releases`_ page.
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


Authenticating Fioctl
#####################

With :ref:`ref-fioctl` installed, authenticate it with our backend.
For this, you will generate OAuth2 application credentials for interacting with the FoundriesFactory™ Platform API:

.. prompt:: bash host:~$, auto

   host:~$ fioctl login
     Please visit:

     https://app.foundries.io/settings/credentials/

     and create a new "Application Credential" to provide inputs below.

     Client ID:

:ref:`ref-fioctl` will now ask for your Client ID and Secret. Follow the next steps to generate them.

Adding Application Credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Go to `Application Credentials <https://app.foundries.io/settings/credentials>`_ and click on :guilabel:`+ New Credentials`.

.. figure:: /_static/getting-started/install-fioctl/application_credentials.png
   :width: 900
   :align: center

   Application Credentials

Complete with a **Description** and the **Expiration date** and select :guilabel:`next`.

Check the :guilabel:`Use for tools like fioctl` box and select your **Factory**.
You can revoke this access and set up a new credential later once you are familiar with the :ref:`ref-api-access`.

.. figure:: /_static/getting-started/install-fioctl/fioctl_token.png
   :width: 500
   :align: center

   API Token

.. tip::

   We recommend creating a new API token for each computer you plan to use our tools with.
   For example, if you develop on both a laptop and a desktop, create a new token for each, as you would with SSH keys.
   This way you can revoke tokens for individual systems should they be compromised.

Use the Client ID and Secret to finish the Fioctl login.

.. figure:: /_static/getting-started/install-fioctl/token.png
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

Use the following command to test the configuration:

.. prompt:: bash host:~$, auto

   host:~$ fioctl -f <factory> status
      Total number of devices: 0
      TAG  LATEST TARGET  DEVICES  ON LATEST  ONLINE
      ---  -------------  -------  ---------  ------

      Orphan target versions below are marked with a star (*)

.. seealso::
   :ref:`ref-fioctl` documentation.

.. _GitHub Releases: https://github.com/foundriesio/fioctl/releases

.. _gs-git-config:

Configuring Git
###############

After :ref:`Fioctl <ref-fioctl>` is setup, you can leverage it as a Git credential helper.
This allows pushing to your :ref:`Factory <ref-factory-definition>` repositories.
With this, Git knows when you connect to ``source.foundries.io`` and uses Fioctl for authentication when utilizing ``git`` commands.

.. note::
   Make sure ``git`` is installed on your host machine.

Setting Up Git
^^^^^^^^^^^^^^

Run the following command to add the relevant entries to the Git configuration:

.. prompt:: bash host:~$, auto

   host:~$ fioctl configure-git

.. warning::
   * If for some reason the command ``fioctl configure-git`` fails with an error, manual steps can be taken to get the exact same result.
     For comprehensive instructions, please see the :ref:`Fioctl™ Errors <ref-ts-errors>` section.

   * Existing users reconfiguring Git access may need to remove the following lines from ``.gitconfig`` to use ``fioctl configure-git`` utility::

      [http "https://source.foundries.io"]
      extraheader = Authorization: basic <TOKEN>

   * If editing scopes on existing tokens, the user should refresh the local ``fioctl`` credentials with::

      fioctl login --refresh-access-token

Verify this has succeeded by cloning a repository from your Factory, such as your ``containers.git`` repo.
Replace ``<factory>`` with your Factory's name:

.. prompt:: bash host:~$, auto

   host:~$ git clone https://source.foundries.io/factories/<factory>/containers.git

.. tip::

   You can also use ``git config --global --list`` to show the current state of the
   global Git configuration, where ``source.foundries.io`` should be referenced
   along with a username and a helper.

.. seealso::
   * :ref:`Fioctl Reference Manual <ref-fioctl>`
   * :ref:`API Access for factory <ref-api-access>`
