.. _ref-vpn:

WireGuard VPN
=============

Factory users may need to remotely access devices that are behind firewalled
private networks. In order to help make remote access easy, the LmP ships
with WireGuard_ available and integrated into `fioctl` and NetworkManager.

Every organization has unique remote access requirements. The
`Factory WireGuard Server`_ has been created as a guide for deploying
a Factory VPN server to a customer managed server.

.. _WireGuard:
   https://www.wireguard.com/


.. _Factory WireGuard Server:
   https://github.com/foundriesio/factory-wireguard-server/

Actions on VPN Server
---------------------

Install dependencies::

   $ sudo apt install git python3 python3-requests


Create an API token for this service at https://app.foundries.io/settings/tokens/


Clone VPN server code::

   $ git clone https://github.com/foundriesio/factory-wireguard-server/
   $ cd factory-wireguard-server


Configure the Factory with this new service::

   $ sudo ./factory-wireguard.py \
       --apitoken <api token> \  # https://app.foundries.io/settings/tokens
       --factory <factory> \
       --privatekey /root/wgpriv.key \ # where to store generated private key
       enable


Run the daemon::

   $ sudo ./factory-wireguard.py \
       --apitoken <api token> \
       --factory <factory> \
       --privatekey /root/wgpriv.key \
       daemon

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


Troubleshooting
---------------

Wireguard uses UDP. This can be difficult to troubleshoot. The best place
to start troubleshooting is by running ``wg show`` on both the server and
device in question. This output will help show what might be wrong. A very
common problem is when the VPN server has a firewall blocking traffic to
the Wireguard port. This situation will show as::

 # wg show on the device:
 interface: factory-vpn0
  public key: sn4oAhIsJXRdTToO0ofRJRhuC7ObPOJYU+s5n8bPPSA=
  private key: (hidden)
  listening port: 56213

 peer: hn2eMQZNLn56UVnHK8GZGvGD1dSLky0hk7sevZ4piB4=
  endpoint: 192.168.0.111:5555
  allowed ips: 10.42.42.1/32
  transfer: 0 B received, 18.36 KiB sent
  persistent keepalive: every 25 seconds

 # wg show on the server:
 interface: factory
  public key: hn2eMQZNLn56UVnHK8GZGvGD1dSLky0hk7sevZ4piB4=
  private key: (hidden)
  listening port: 5555

 peer: sn4oAhIsJXRdTToO0ofRJRhuC7ObPOJYU+s5n8bPPSA=

The device is trying to connect, but no data has been transferred. The server
is showing that the device hasn't established a connection (there's no data
for the peer). If the server's IP is correct, then its likely a firewall is
blocking UDP traffic to this port.

