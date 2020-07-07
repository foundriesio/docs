.. _ref-wireguard:

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
