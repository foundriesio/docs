# Troubleshooting and FAQ

## General

### Request Entity Too Large

This error occurs when your Factory has accumulated too much Target
metadata to be signed by TUF. This happens because the `targets.json`
containing all of your Targets that is associated with your Factory
grows large over time:

    Signing local TUF targets
    == 2020-11-24 23:12:53 Running: garage-sign targets sign --repo /root/tmp.dNLAIH
    --key-name targets
    |  signed targets.json to /root/tmp.dNLAIH/roles/targets.json
    |--
    Publishing local TUF targets to the remote TUF repository
    == 2020-11-24 23:12:55 Running: garage-sign targets push --repo /root/tmp.dNLAIH
    |  An error occurred
    |  com.advancedtelematic.libtuf.http.SHttpjServiceClient$HttpjClientError:
    ReposerverHttpClient|PUT|http/413|https://api.foundries.io/ota/repo/magicman//api/v1/user_repo/targets|<html>
    |  <head><title>413 Request Entity Too Large</title></head>
    |  <body>
    |  <center><h1>413 Request Entity Too Large</h1></center>
    |  <hr><center>nginx/1.19.3</center>
    |  </body>
    |  </html>

#### Solution

Pruning (deletion) of Targets is a manual maintenance procedure you must
consider when creating Targets over time.

**The solution** is to prune the Targets that you no longer need using
Fioctl. This removes these targets from the `targets.json` associated
with your Factory, allowing the production of new Targets.

Warning

Ensure there are no important devices running on a Target that is about
to be pruned. If you are intending on pruning `master`, be careful and
make sure you know what you are doing.

You can individually prune/delete targets by their Target number:

    fioctl targets prune <target_number>

Or, you can prune by tag, such as `devel` or `experimental`:

    fioctl targets prune --by-tag <tag>

### Aktualizr-Lite Pruning Containers

By default, `ref-aktualizr-lite` will prune Docker containers
periodically. If this behavior is undesirable, it can be worked around
by adding `aktualizr-lite-no-prune` as a label to Docker containers, or
by adding `docker_prune = "0"` to the `[pacman]` section of
`/var/sota/sota.toml` on a given device.

    LABEL aktualizr-lite-no-prune

Note

<https://docs.docker.com/engine/reference/builder/#label>
