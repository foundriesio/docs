.. highlight:: sh

.. _iot-gateway-debian_ubuntu:

IoT Gateway: Generic Debian/Ubuntu Instructions
===============================================

Check kernel version
--------------------

The IoT gateway requires a kernel version 4.4+ due to the 6lowpan
requirements.

You can check your kernel version via::

    root@linaro-developer:~# uname -r
    4.9.0-35-arm64

Check / Update BlueZ stack
--------------------------

Check your bluez version with the following command::

    $ sudo dpkg --status bluez | grep '^Version:'
    Version: 5.41-0ubuntu3

It is recommended that IoT gateway run BlueZ v5.41+.  It includes a
fix to a bug which causes the bluetooth stack to corrupt and require
an hci restart to fix.

Debian contains the following BlueZ packages:

- Jessie: 5.23-2 (This should be updated to the Stretch version)
- Stretch: 5.43-1

Ubuntu contains the following BlueZ packages (by version):

- xenial (16.04LTS): 5.37-0ubuntu5 (This should be updated to the version in yakkety)
- yakkety (16.10): 5.41-0ubuntu3

Install radvd (Router Advertisement Daemon)
-------------------------------------------

::

    $ sudo apt-get install radvd
    # (use the text editor of your choice to create the following config file)
    root@linaro-developer:~# cat /etc/radvd.conf
    interface bt0
    {
        IgnoreIfMissing on;
        AdvSendAdvert on;
        MinRtrAdvInterval 300;
        MaxRtrAdvInterval 600;
        AdvDefaultLifetime 7200;
        prefix fc00::/64
        {
            AdvOnLink off;
            AdvValidLifetime 36000;
            AdvPreferredLifetime 36000;
            AdvAutonomous on;
            AdvRouterAddr on;
        };
    };

Install ndppd
-------------

::

    $ sudo apt-get install ndppd
    # (use the text editor of your choice to create the following config file)
    root@linaro-developer:~# cat /etc/ndppd.conf
    route-ttl 30000
    proxy wlan0 {
        router yes
        timeout 500
        ttl 30000
        rule fc00:0:0:0:d4e7::/80 {
            static
        }
    }


Install tinyproxy
-----------------

::

    $ sudo apt-get install tinyproxy
    # (use the text editor of your choice to create the following config file)
    root@linaro-developer:~# cat /etc/tinyproxy.conf
    User nobody
    Group nogroup
    Port 8888
    Listen fc00::d4e7:0:0:1
    Timeout 600
    # TODO: Make this return a 30 second JSON wait response
    DefaultErrorFile "/usr/share/tinyproxy/default.html"
    StatFile "/usr/share/tinyproxy/stats.html"
    Logfile "/var/log/tinyproxy/tinyproxy.log"
    LogLevel Info
    PidFile "/var/run/tinyproxy/tinyproxy.pid"
    MaxClients 100
    StartServers 10
    Allow fc00::/7
    Allow fe80::/64
    Allow ::1
    ViaProxyName "tinyproxy"
    ReversePath "/DEFAULT/" "http://gitci.com:8080/DEFAULT/"
    ReverseOnly Yes


Set IP address for bt0 interface
--------------------------------

::

    # (use the text editor of your choice to create the following config file)
    root@linaro-developer:~# cat /etc/network/interfaces.d/bt0
    auto bt0
    allow-hotplug bt0
    iface bt0 inet6 static
        address fc00:0:0:0:d4e7::1
        netmask 80
        up service tinyproxy start
        down service tinyproxy stop

Setup sysctrl for router services
---------------------------------

::

    # (use the text editor of your choice to create the following config file)
    root@linaro-developer:~# cat /etc/sysctl.d/gateway.conf
    # don't ignore RA on wlan0
    net.ipv6.conf.wlan.accept_ra=2
    # enable ip forwarding
    net.ipv6.conf.all.forwarding=1
    # enable IPv6 neighbour proxy, in case the 6lowpan needs to share the same host IPv6 subnet
    net.ipv6.conf.all.proxy_ndp=1

Set Network Manager to ignore the bt0 interface
-----------------------------------------------

.. highlight:: none

Add the following lines to /etc/NetworkManager/NetworkManager.conf::

    ...

    [keyfile]
    unmanaged-devices=interface-name:bt0

Download bluetooth_6lowpand script
----------------------------------

.. highlight:: sh

The attached script looks for Linaro FOTA IoT devices which are ready
to connect and auto attaches them via 6lowpan

https://raw.githubusercontent.com/Hashcode/iot-gateway-files/master/bluetooth_6lowpand.sh

(OPTIONAL) Set the location of gitci.com in /etc/hosts
------------------------------------------------------

If you are running a local Hawkbit server, you will need to add an
entry to the hosts file for gitci.com otherwise DNS will be used to
locate the gitci.com server.

Reboot
------

Start the IoT gateway processes
-------------------------------

To start the IoT gateway processes do the following::

    $ sudo service radvd start
    $ sudo service ndppd start
    # start the bluetooth_6lowpand script downloaded above
    $ sudo bash ./bluetooth_6lowpand.sh

