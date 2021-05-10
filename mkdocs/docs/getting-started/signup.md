# Sign Up

To create a FoundriesFactory, you first need to [create an
account](https://app.foundries.io/signup) with us.

<figure>
<img src="/_static/signup/login.png" class="align-center" width="380" alt="This is the beginning of your journey." /><figcaption aria-hidden="true">This is the beginning of your journey.</figcaption>
</figure>

# Create a Factory

`ref-factory` is the start of your embedded OS, tailored specifically
for your product. When you create a Factory, we immediately bootstrap
the CI build process for a vanilla, unmodified `ref-linux` OS Image,
which is from this point onward, **owned by you**.

When your account is created, it is not associated with any factories.

Create one by clicking `Create Factory`.

Warning

Once a Factory is created, the chosen platform/machine and Factory name
cannot be changed. Create a new Factory or contact support if a mistake
is made. <https://support.foundries.io/>.

<figure>
<img src="/_static/signup/no-factories.png" class="align-center" width="900" alt="Your journey begins empty handed" /><figcaption aria-hidden="true">Your journey begins empty handed</figcaption>
</figure>

Note

Upon Factory creation you will be sent an email with instructions to
securely download your `ref-offline-keys`. Read
`this documentation<ref-offline-keys>` for information on key rotation.

It is incredibly important that your keys are kept **safe and private**.
Please store these keys securely.

Suggest methods of storing TuF keys securely, such as by USB in a safety
deposit box, or yubikey.

## Select Your Platform

Choose a hardware platform from the dropdown menu in the **Create New
Factory** wizard and continue. Click `Create Factory` once your details
are entered.

The `ref-linux` supports a wide range of platforms out of the box. This
includes [QEMU](https://www.qemu.org/) images for
[ARM](https://www.arm.com/) and [RISC-V](https://riscv.org/)
architectures.

<figure>
<img src="/_static/signup/create.png" class="align-center" width="450" alt="Create Factory" /><figcaption aria-hidden="true">Create Factory</figcaption>
</figure>

Tip

Your chosen platform determines what the initial value for the
`machines:` key will be for your first build. This key and its value can
later be changed via `factory-config.yml` in the
`ref-Factory-definition`

## Watch Your Build

Once you have created your Factory, an initial build of the Foundries.io
Linux microPlatform (LmP) will be generated for you to build your
product on top of. You can monitor the progress of this initial build in
the `Targets` tab of your Factory after a few minutes. Additionally, you
will receive an Email once this initial build is complete.

Targets are a reference to a platform image and docker applications.
When developers push code, the FoundriesFactory produces a new target.
Registered devices update and install targets.

The `Targets` tab of the Factory will become more useful as you begin to
build your application and produce new Targets for the Factory to build.

Note

If you'd like to learn more, [we wrote a
blog](https://foundries.io/insights/blog/2020/05/14/whats-a-target/)
about what Targets are and why we made them the way they are.

<figure>
<img src="/_static/signup/build.png" class="align-center" width="900" alt="FoundriesFactory Targets" /><figcaption aria-hidden="true">FoundriesFactory Targets</figcaption>
</figure>

Warning

Bootstrapping your Factory securely takes some time. Your first build
will take up to 30 minutes to complete.

Read through the rest of this section and set up your development
environment while you wait for us to build your Factory from scratch.
