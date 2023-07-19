.. _ref-wireguard:

WireGuard VPN
=============

Factory users may need to remotely access devices that are behind firewalled
private networks. In order to help make remote access easy, the LmP ships
with WireGuard_ available and integrated into :ref:`fioctl` and NetworkManager.

Every organization has unique remote access requirements. The
`Factory WireGuard Server`_ has been created as a guide for deploying
a Factory VPN server to a customer managed server.

.. _WireGuard:
   https://www.wireguard.com/


.. _Factory WireGuard Server:
   https://github.com/foundriesio/factory-wireguard-server/

Actions on VPN Server
---------------------

.. note::

   Make sure to replace the ``<factory>`` (name of your FoundriesFactory)
   placeholder with your own information in the following commands.

Install dependencies::

   $ sudo apt install git wireguard wireguard-tools python3 python3-requests


Clone VPN server code::

   $ git clone https://github.com/foundriesio/factory-wireguard-server/
   $ cd factory-wireguard-server


Configure the Factory with this new service and enable the daemon::

   $ sudo ./factory-wireguard.py \
       --oauthcreds /root/fiocreds.json \ # oauth2 credentials will be written here
       --factory <factory> \
       --privatekey /root/wgpriv.key \ # where to store generated private key
       enable

At this point you will be prompted to authorize an Oauth2 request. It
will look something like::

   External Endpoint: 165.227.222.126:5555
   VPN Address: 10.42.42.0
   Registring with foundries.io...
   Visit this link to authorize this application:

     https://app.foundries.io/authorize?client_id=fioid_B68H03zaynCXzycBX9M3WKL7xLqJYJyf&response_type=code&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=andy-corp%3Adevices%3Aread-update+andy-corp%3Adevices%3Aread

    Enter code:  <copy/paste code from previous link>
    Creating systemd service factory-vpn-andy-corp.service
    Service is running. Logs can be viewed with: journalctl -fu factory-vpn-andy-corp.service

The daemon keeps track of connected devices by putting entries into
``/etc/hosts`` so that they can be easily referenced from the server.

Enabling remote access to a device
----------------------------------

A device can be configured to connect to the VPN server using fioctl::

  $ fioctl devices config wireguard <device> enable

This setting can take up to 5 minutes to be applied by `fioconfig` on the
device. Once active, it can be reached from the VPN server with a command
like::

  $ ssh <device>

Remote access can be disabled from fioctl with::

  $ fioctl devices config wireguard <device> disable


Changing wireguard server address
---------------------------------

It is sometimes necessary to change the WireGuard server's private VPN address.
For example, when the initial setup is done using a developer's laptop, default
factory-wireguard.py settings are probably used. Later on, when it's required for
more developers to have remote access to the devices, the server should be moved
(for example to a cloud hosted VM). When such move happens it might be necessary
to change WireGuard's address (default might already be in use). This is easy on
the server side as it's just a command line parameter::

   $ sudo ./factory-wireguard.py \
       --apitoken <api token> \  # https://app.foundries.io/settings/tokens
       --factory <factory> \
       --privatekey /root/wgpriv.key \ # where to store generated private key
       enable
       --vpnaddr 10.42.44.1

It's a bit more complicated on the device side. Once the WireGuard configuration is
initiated, it's not changed when server endpoint moves. This needs to be done
manually by updating device settings. The settings are stored in
``wireguard-client`` file. Example *old settings*::

  address=10.42.42.2
  pubkey=abcdefghijk123456789

The public key corresponds to a private key that is already stored on the device.
This part should not be changed. It is important to keep this configuration file
unencrypted. After the change the file should look like this::

  address=10.42.44.2
  pubkey=abcdefghijk123456789

This change can be done using ``fioct devices config set`` command. More details
can be found in :ref:`fioctl` section. This can be done with::

  $ fioctl devices config set my-device-1 --raw my-device-1.config.json

The contents of the ``my-device.config.json`` below:

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

Wireguard uses UDP. This can be difficult to troubleshoot. A very common problem
is when the VPN server has a firewall blocking traffic to the Wireguard port.

.. note::

  When configuring a server behind a firewall, make sure the desired port
  is passed through to the host running the server.

When activating the wireguard server, you may get::

  ERROR: A UDP socket is already opened on 165.227.222.126:5555

Make sure no other service is using the port.

If no other service is using that port, add ``--no-check-ip``
after the ``enable`` to activate the wireguard server.

Method 1
~~~~~~~~

One way to debug this situation is by running ``wg show`` on both the server and
device in question. This output will help show what might be wrong.

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

This shows that the device is trying to connect, but no data has been
transferred. The server is showing that the device hasn't established a
connection (there's no data for the peer). If the server's IP is correct, then
its likely a firewall is blocking UDP traffic to this port.

Method 2
~~~~~~~~

Another method that can be used to debug this scenario is to use ``nc -lup
12345`` (netcat) in UDP listen mode on the server running Wireguard. Then
attempting to send text via UDP to the specified port, which in this example is
``12345``. This port can be replaced in order to test another.

Netcat should be available by default on any Unix system (Linux,
macOS, WSL_, BSD).

Any machine can be used as the client in this example. It is
often helpful to try this with multiple clients on multiple networks and
internet connections to confirm your results.

On the server running Wireguard::

  nc -lup 12345

On any client::

  echo "UDP is not blocked on this port!" | nc -u <server address> 12345

Watch the terminal of the server where you ran ``nc -lup 12345``, you will see
the text appear if UDP is not blocked on the port ``12345``.

If something is preventing traffic reaching the destination then you will not
see a message appear. After trying one client, try another to confirm your
results.

.. note::

   Since UDP is stateless, each successful connection means you need to restart
   the ``nc`` session on the server. For each debug attempt, rinse and repeat
   this process by killing and restarting the ``nc -lup`` command.

.. _WSL: https://learn.microsoft.com/en-us/windows/wsl/about

Further Debug
~~~~~~~~~~~~~
On a client, it is also possible to setup firewall rules that would prevent
WireGuard from working correctly. In that case you will need to add something
like this::

  sudo iptables -I INPUT -p udp -m udp --sport 5555 -j ACCEPT
  sudo iptables -I OUTPUT -p udp -m udp --dport 5555 -j ACCEPT
