Fioctl
======

This section assumes you have followed :ref:`sec-learn` to its completion. The
aim of this section is to provide you with a template for using
:ref:`ref-fioctl` by way of example.

Common Commands
---------------

View targets
  ``fioctl targets list -f <factory>``
    Lists the targets your Factory has produced so far.

  .. asciinema:: ../_static/asciinema/view-targets.cast

List devices
  ``fioctl devices list -f <factory>``
    Lists the devices that have connected to your Factory, along with associated
    metadata, such as device name, status, target and enabled apps.

  .. asciinema:: ../_static/asciinema/list-devices.cast

Set device tag(s)
  ``fioctl devices config updates <device_name> --tags <tag>``
    Filter the targets a device will accept by tag. For example, to move a
    device from accepting 'devel' builds to 'master' builds. See the
    :ref:`ref-advanced-tagging` section for more examples.

  .. asciinema:: ../_static/asciinema/set-device-tags.cast

Set app(s) to be enabled
  ``fioctl devices config updates <device_name> --apps <app_name1>,<app_name2>``
    Set the app(s) a device will run.

  .. asciinema:: ../_static/asciinema/set-apps.cast

Enable :ref:`ref-wireguard`
  ``fioctl devices config wireguard <device_name> <enable|disable>``
    Enable or disable the Wireguard systemd service on your LmP device. This
    requires that you configure your Factory to use an instance of Wireguard you
    have set up on your own server as described in the :ref:`ref-wireguard`
    guide.

  .. asciinema:: ../_static/asciinema/enable-wireguard.cast
