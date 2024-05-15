.. _ref-wireguard:

WireGuard VPN
=============

You may need your Factory to remotely access devices behind private network firewalls.
To make remote access easier, LmP ships with WireGuard_ integrated into :ref:`Fioctl <fioctl>` and NetworkManager.

Every organization has unique remote access requirements.
The `Factory WireGuard Server`_ was created as a guide for deploying a Factory VPN server to a server you manage.

.. _WireGuard:
   https://www.wireguard.com/


.. _Factory WireGuard Server:
   https://github.com/foundriesio/factory-wireguard-server/

Actions on VPN Server
---------------------

.. note::

   In the following commands, replace ``<factory>`` with the name of your Factory.

Install dependencies:

.. prompt:: bash

     sudo apt install git wireguard wireguard-tools python3 python3-requests

Clone the VPN server code:

.. prompt:: bash

     git clone https://github.com/foundriesio/factory-wireguard-server/
     cd factory-wireguard-server

Configure your Factory with this new service, and enable the daemon:

.. code:: bash

     sudo ./factory-wireguard.py \
       --oauthcreds /root/fiocreds.json \ # oauth2 credentials will be written here
       --factory <factory> \
       --privatekey /root/wgpriv.key \ # where to store generated private key
       enable

At this point, you will be prompted to authorize an Oauth2 request.
It will look something like::

   External Endpoint: 165.227.222.126:5555
   VPN Address: 10.42.42.0
   Registring with foundries.io...
   Visit this link to authorize this application:

     https://app.foundries.io/authorize?client_id=fioid_B68H03zaynCXzycBX9M3WKL7xLqJYJyf&response_type=code&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=andy-corp%3Adevices%3Aread-update+andy-corp%3Adevices%3Aread

    Enter code:  <copy/paste code from previous link>
    Creating systemd service factory-vpn-andy-corp.service
    Service is running. Logs can be viewed with: journalctl -fu factory-vpn-andy-corp.service

You will create two tokens.
Token 1, a short-lived token with ``devices:read-update`` to update factory.
Token 2, long-term token with ``devices:read``.

The daemon keeps track of connected devices by putting entries into ``/etc/hosts``.
This is so they can be easily referenced from the server.

Enabling Remote Access to a Device
----------------------------------

A device can be configured to connect to the VPN server using the Fioctl® utility::

  $ fioctl devices config wireguard <device> enable

This setting can take up to 5 minutes to be applied by ``fioconfig`` on the device.
Once active, it can be reached from the VPN server using SSH::

  $ ssh <device>

Remote access can be disabled from Fioctl with::

  $ fioctl devices config wireguard <device> disable


Changing Wireguard Server Address
---------------------------------

It is sometimes necessary to change the WireGuard server's private VPN address.
For example, when initial setup is done on a developer's laptop, the default ``factory-wireguard.py`` settings are used.
Later on, when more developers need to have remote access to the devices, the server should be moved (such as to a cloud hosted VM).
When such a move happens, it may be necessary to change WireGuard's address (the default might already be in use).
This is easy on the server side, as it is just a command line parameter::

   $ sudo ./factory-wireguard.py \
       --apitoken <api token> \  # https://app.foundries.io/settings/tokens
       --factory <factory> \
       --privatekey /root/wgpriv.key \ # where to store generated private key
       enable
       --vpnaddr 10.42.44.1

It is a bit more complicated on the device side.
Once the WireGuard configuration is initiated, it is not changed when server endpoint moves.
This needs to be done manually by updating device settings.
The settings are stored in the ``wireguard-client`` file.
Example of *old settings*::

  address=10.42.42.2
  pubkey=abcdefghijk123456789

A public key corresponds to a private key already stored on the device.
This part should not be changed.
It is important to keep this configuration file unencrypted.
With the *new settings*, the example file would look like::

  address=10.42.44.2
  pubkey=abcdefghijk123456789

.. important::
   If you copy/paste the above example, replace ``pubkey`` value with the
   public key already on the device.

This change can be done with ``fioct devices config set``.
More details can be found under the :ref:`fioctl` section.
An example of this command::

  $ fioctl devices config set my-device-1 --raw my-device-1.config.json

The contents of the ``my-device.config.json`` would look like:

.. code:: json

  {
    "reason": "Update wireguard settings",
    "files": [
      {
        "name": "wireguard-client",
        "value": "address=10.42.44.2\npubkey=abcdefghijk123456789",
        "unencrypted": true
      }
    ]
  }


Troubleshooting
---------------

Wireguard uses UDP, which can be difficult to troubleshoot.
A common problem arises when the VPN server has a firewall blocking traffic to the Wireguard port.

.. note::

  When configuring a server behind a firewall, make sure the desired port is passed through to the host running the server.

When activating the Wireguard server, you may get::

  ERROR: A UDP socket is already opened on 165.227.222.126:5555

Make sure no other service is using the port.

If no other service is using that port, add ``--no-check-ip`` after the ``enable`` to activate the Wireguard server.

Method 1
~~~~~~~~

One way to debug this situation is by running ``wg show`` on both the server and device in question.
This output may help identify the problem.

``wg show`` on the device::

 interface: factory-vpn0
  public key: sn4oAhIsJXRdTToO0ofRJRhuC7ObPOJYU+s5n8bPPSA=
  private key: (hidden)
  listening port: 56213

 peer: hn2eMQZNLn56UVnHK8GZGvGD1dSLky0hk7sevZ4piB4=
  endpoint: 192.168.0.111:5555
  allowed ips: 10.42.42.1/32
  transfer: 0 B received, 18.36 KiB sent
  persistent keepalive: every 25 seconds

``wg show`` on the server::

 interface: factory
  public key: hn2eMQZNLn56UVnHK8GZGvGD1dSLky0hk7sevZ4piB4=
  private key: (hidden)
  listening port: 5555

 peer: sn4oAhIsJXRdTToO0ofRJRhuC7ObPOJYU+s5n8bPPSA=

This shows that the device is trying to connect, but no data has been transferred.
The server is showing that the device has not established a connection (there is no data for the peer).
If the server's IP is correct, then it is likely a firewall is blocking UDP traffic to this port.

Method 2
~~~~~~~~

Another method is to use ``nc -lup 12345`` (netcat) in UDP listen mode on the server running Wireguard.
Then attempt to send text via UDP to the specified port (in this example ``12345``).
This port can be replaced in order to test another.

Netcat is usually available by default on any Unix system (Linux, macOS, WSL_, BSD).

Any machine can be used as the client in this example.
It may be helpful to try this with multiple clients on multiple networks and internet connections to confirm your results.

On the server running Wireguard::

  nc -lup 12345

On any client::

  echo "UDP is not blocked on this port!" | nc -u <server address> 12345

Watch the terminal of the server where you ran ``nc -lup 12345``.
You will see the text appear if UDP is not blocked on port ``12345``.

If something is preventing traffic reaching the destination, then you will not see the text.
After trying one client, try another to confirm your results.

.. note::

   Since UDP is stateless, each successful connection means you need to restart the ``nc`` session on the server.
   For each debug attempt, refresh and repeat this process by killing and restarting the ``nc -lup`` command.

.. _WSL: https://learn.microsoft.com/en-us/windows/wsl/about

Further Debug
~~~~~~~~~~~~~

On a client, it is also possible to setup firewall rules that would prevent WireGuard from working correctly.
In this case, you will need to add something like this::

  sudo iptables -I INPUT -p udp -m udp --sport 5555 -j ACCEPT
  sudo iptables -I OUTPUT -p udp -m udp --dport 5555 -j ACCEPT

When troubleshooting Wireguard issues after rebooting your host,
running the following ``systemctl`` commands can help determine if the 1-shot service is running.
Note that you will have needed to run the ``factory-wireguard.py`` script.

::

 sudo systemctl status factory-vpn-<factory>
 sudo systemctl enable factory-vpn-<factory>
 sudo systemctl start factory-vpn-<factory>
