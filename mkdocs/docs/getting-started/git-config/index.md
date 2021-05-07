# Configuring Git

Pushing to the Git repositories in your FoundriesFactory is as simple as
configuring Git on your personal machine to use the **api token** you
generated as part of your `account creation <gs-signup>`. Once
configured, `git` will know when are connecting to `source.foundries.io`
and will use this token to authenticate you with our Git server.

## Source Code Access Token

In the right top corner, click on the avatar and select `Settings` in
the drop-down list.

<figure>
<img src="/_static/git-config/settings.png" class="align-center" width="900" alt="FoundriesFactory Settings" /><figcaption aria-hidden="true">FoundriesFactory Settings</figcaption>
</figure>

Select the tab `Tokens` and create a new **Api Token** by clicking on
the `+ New Token`. Complete with a **Description** and the **Expiration
date** and select `next`.

For this tutorial, check the `Use for source code access` box and select
your **Factory**. You can later revoke this access and set up a new
token once you are familiar with the `ref-api-access`.

<figure>
<img src="/_static/git-config/token.png" class="align-center" width="500" alt="Token for source code access" /><figcaption aria-hidden="true">Token for source code access</figcaption>
</figure>

## Git Setup

Replace `YOUR_TOKEN` in the following command with your access token. An
example token looks like this:
`ebAYLaManEgNdRnWKfnwNDJjU45c5LJPmWsYw78z`

bash host:~$, auto

host:~$ git config --global
http.<https://source.foundries.io.extraheader> "Authorization: basic
$(echo -n YOUR\_TOKEN | openssl base64)"

You can verify that this has been successful by attempting to clone a
repository from your FoundriesFactory. As an example, you can clone your
`containers.git` repo.

Replace `<factory>` with your FoundriesFactory name.

bash host:~$, auto

host:~$ git clone
<https://source.foundries.io/factories/>&lt;factory&gt;/containers.git

Tip

You can also use `git config --list` to show you the current state of
the global Git configuration, in which `source.foundries.io` should be
referenced along with your access token, represented as a base64 string.

**git-config** add :ref: to 'FoundriesFactory', 'access token', 'account
creation', 'ci scripts' when pages are available
