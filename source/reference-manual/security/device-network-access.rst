.. _ref-device-network-access:

Device Network Access
=====================

LmP devices have no ingress network requirements.
However, they do need to connect to external services for device management:

======================   ============  ===========   =============================
**Host**                 **Protocol**  **Port(s)**   **Description**
----------------------   ------------  -----------   -----------------------------
ota-lite.foundries.io*   TCP           8443          :ref:`Device gateway <ref-device-gateway>`
ostree.foundries.io*     TCP           8443          OSTree server for updates
hub.foundries.io         TCP           443           Docker container registry
hub-auth.foundries.io    TCP           443           Docker registry authentication service
storage.googleapis.com   TCP           443           OSTree and Docker redirects
time[1234].google.com    UDP           123           Primary `NTP servers`_
time.cloudflare.com      UDP           123           Last fallback NTP server
api.foundries.io         TCP           443           If using lmp-device-register
app.foundries.io         TCP           443           If using lmp-device-register
======================   ============  ===========   =============================

\* When a factory has :ref:`PKI <ref-device-gateway>` enabled it will have it's own unique DNS name for the device-gateway and OSTree servers.
These DNS names can be found by running ``fioctl keys ca show --pretty | grep DNS``.

You may do other customizations to a device that require it to access additional services not mentioned here. Common ones include:

 * A :ref:`WireGuard VPN <ref-wireguard>` server
 * Third-party container registries like Docker (registry-1.docker.io, auth.docker.io, index.docker.io, etc)

.. _NTP servers:
   https://developers.google.com/time
