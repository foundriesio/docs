# Configure your device

At this point, your device should be registered to your Factory
according to the `Getting Started guide <gs-register>`. Once registered,
two services start to communicate with your Factory: `aktualizr-lite`
and `fioconfig`.

**aktualizr-lite**:

This is the daemon responsible for updating the device. It checks for
new updates and implements [The Update Protocol
(TUF)](https://theupdateframework.com/) to guarantee the integrity of
platform and container updates.

**fioconfig**:

This is the daemon responsible for managing configuration data for your
device. The content is encrypted in a way that only the device will be
able to decrypt and use.

Both applications are configured to communicate with your Factory. That
being said, an update could take up to 10 minutes to be triggered. This
can be configured according to your product needs.

To improve your experience during this tutorial, you will configure both
`aktualizr-lite` and `fioconfig` to check every minute.

This configuration will only apply to the device where the commands
below are run. To change the timing for the entire fleet, you will need
to customize your Factory image.

On your device, create a settings file in the `/etc/sota/conf.d/` folder
to configure `aktualizr-lite`:

bash device:~$

sudo mkdir -p /etc/sota/conf.d/ sudo bash -c 'printf
"\[uptane\]npolling\_sec = 60" &gt; /etc/sota/conf.d/z-01-polling.toml'

Next, create a settings file in the `/etc/default/` folder to configure
`fioconfig`:

bash device:~$

sudo bash -c 'printf "DAEMON\_INTERVAL=60" &gt; /etc/default/fioconfig'

Restart both services:

bash device:~$

sudo systemctl restart aktualizr-lite sudo systemctl restart fioconfig

Tip

In the following instructions, you will disable and enable services.
This will trigger `aktualizr-lite` tasks that might be interesting to
follow.

To watch the `aktualizr-lite` logs and see the updates, leave a device
terminal running the command:

bash device:~$

sudo journalctl --follow --unit aktualizr-lite
