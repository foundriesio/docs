# Register your device

Your Linux microPlatform image includes a tool, `lmp-device-register`
that will register your device(s) via the Foundries.io REST API.

1.  From a console on the device run this command to register the device
    to your factory:

> bash device:~$, auto
>
> device:~$ sudo lmp-device-register -n &lt;device-name&gt;

Note

**By default** devices will run **all** applications that are defined in
the `containers.git` repository and therefore available in the latest
Target. This behavior can be changed by enabling only specific
applications. Read `ug-fioctl-enable-apps` to learn how.

1.  You will be prompted by `lmp-device-register` to complete a
    challenge with our API

    **Example Output**:

    text

    Registering device, test, to factory gavin. Device UUID:
    df1295df-ba58-40a0-9239-542ded5ab934

    ----------------------------------------------------------------------------Visit
    the link below in your browser to authorize this new device. This
    link will expire in 15 minutes. Device Name:
    df1295ff-ba58-40a0-9239-542bed5ab964 User code: SQRD-PLBN Browser
    URL: <https://app.foundries.io/activate/>

2.  After completing the previous step, the device is registered and
    should be visible by navigating to the web interface at
    <https://app.foundries.io/factories/>, clicking your **Factory** and
    selecting the **Devices** tab.

    Or by using `ref-fioctl`:

> bash host:~$, auto
>
> host:~$ fioctl devices list
