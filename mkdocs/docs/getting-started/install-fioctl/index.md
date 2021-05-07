# Fioctl CLI Installation

`ref-fioctl` is a simple tool that interacts with the Foundries.io REST
API for managing a Factory. It is based on the [ota-lite
API](https://api.foundries.io/ota/), also built by Foundries.io.

`ref-fioctl`, is used to manage:

-   `Tags (per device, and per Factory) <ref-advanced-tagging>`
-   `Device configuration <ref-fioconfig>`
-   `OTA updates <ref-aktualizr-lite>`
-   `CI Secrets <ref-container-secrets>`

## Installation

### Manual Installation

We use [Github Releases](https://github.com/foundriesio/fioctl/releases)
to distribute static X86\_64 golang binaries.

Linux

1.  Download a Linux binary from the [Github
    Releases](https://github.com/foundriesio/fioctl/releases) page to a
    directory on your `PATH`, make sure you have Curl installed

    For example, to download version on Linux, define the version:

    FIOCTL\_VERSION=""

    Download the binary with curl:

    bash host:~$, auto

    host:~$ sudo curl -o /usr/local/bin/fioctl -LO
    <https://github.com/foundriesio/fioctl/releases/download/$FIOCTL_VERSION/fioctl-linux-amd64>

2.  Make the `ref-fioctl` binary executable:

    bash host:~$, auto

    host:~$ sudo chmod +x /usr/local/bin/fioctl

You can execute this again in future to overwrite your binary, therefore
updating or changing your version.

macOS

1.  Download a Darwin binary from the [Github
    Releases](https://github.com/foundriesio/fioctl/releases) page to a
    directory on your `PATH`, make sure you have Curl installed

    For example, to download version on macOS, define the version:

    FIOCTL\_VERSION=""

    Download the binary with curl:

    bash host:~$, auto

    host:~$ curl -o /usr/local/bin/fioctl -LO
    <https://github.com/foundriesio/fioctl/releases/download/$FIOCTL_VERSION/fioctl-darwin-amd64>

2.  Make the `ref-fioctl` binary executable:

    bash host:~$, auto

    host:~$ sudo chmod +x /usr/local/bin/fioctl

You can execute this again in future to overwrite your binary, therefore
updating or changing your version.

Windows

1.  Download a Windows binary from the [Github
    Releases](https://github.com/foundriesio/fioctl/releases) page.

2.  Put it in a folder of your choosing and rename it to `fioctl.exe`

3.  Press `Win + R` and type `SystemPropertiesAdvanced`

4.  Press `enter` or click `OK`.

5.  Click "Environment Variables..." in the resultant menu..

6.  Click the `Path` **system** variable, then click `Edit...`

7.  Click `New` in the "Edit environment variable" menu.

8.  Enter the path to the folder in which you have placed `ref-fioctl`.

    An example path string if installing to a folder on the desktop
    would look like this.

    `C:\Users\Gavin\Desktop\fio\bin`

You should now be able to open `cmd.exe` or `powershell.exe` and type
`fioctl`.

### Install From Source

Note

This requires that you have Golang installed. See
<https://golang.org/doc/install> for instructions.

If you intend to use Fioctl on a non X86\_64 platform (like a Raspberry
Pi/Pinebook/Smartphone) such as ARM, RISC-V, PPC, etc. Fioctl can be
compiled and installed from the latest sources and installed via
Golang's own package manager; `go get`:

bash host:~$, auto

host:~$ go get github.com/foundriesio/fioctl

## Authenticate fioctl

Now that `ref-fioctl` is installed, you must authenticate with our
backend before you're able to use it. This requires you to generate
OAuth2 application credentials for interacting with Factory APIs:

bash host:~$, auto

host:~$ fioctl login

`ref-fioctl` will now ask for your application credentials and walk you
through the authentication process.

### fioctl Token

Go to [Token](https://app.foundries.io/settings/tokens/) and create a
new **Api Token** by clicking on the `+ New Token`. Complete with a
**Description** and the **Expiration date** and select `next`.

For fioctl, check the `Use for tools like fioctl` box and select your
**Factory**. Remember that you can revoke this access and set up a new
credential later once you are familiar with the `ref-api-access`.

<figure>
<img src="/_static/install-fioctl/fioctl_token.png" class="align-center" width="500" alt="Token for fioctl" /><figcaption aria-hidden="true">Token for fioctl</figcaption>
</figure>

Tip

We recommend creating a new API token for each device you plan to use
our tools with. For example, if you intend to develop on multiple
systems such as a laptop and a desktop, you should create a new token
for each, just as you would with SSH keys. This way you can revoke
tokens for individual systems, should they be compromised.

## Configuration

When working with multiple factories, specifying a factory name is
mandatory. It can be set using 3 different methods:

> -   Argument:
>
>     bash host:~$, auto
>
>     host:~$ fioctl targets list --factory &lt;factory&gt;
>
> -   Environment Variable:
>
> > bash host:~$, auto
> >
> > host:~$ export FIOCTL\_FACTORY=&lt;factory&gt; host:~$ fioctl
> > targets list
>
> -   Configuration File:
>
> > bash host:~$, auto
> >
> > host:~$ echo "factory: &lt;factory&gt;" &gt;&gt;
> > $HOME/.config/fioctl.yaml host:~$ fioctl targets list

Note

Refer to the `ref-fioctl` section of the documentation to learn more
about configuration.
