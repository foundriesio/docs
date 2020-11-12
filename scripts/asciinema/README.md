# Usage

This is an Asciinema container for recording casts for usage in the
documentation. This container also installs the latest version of `fioctl` at
runtime via `curl`

Typically, you want to run this with your host machine's fioctl config mapped in
via a volume, as well as the output directory you want your casts to go into.

### First

```
docker build . -t fio-asciinema
```

### Then

```
docker run --rm -v <host-fioctl-config-dir>:/root/.config/fioctl.yaml -v <cast-output-dir>:/home/gavin/casts -it fio-asciinema

# Example on my machine
# docker run --rm -v /home/matthew/.config/fioctl.yaml:/root/.config/fioctl.yaml -v /home/matthew/git/foundries/docs/source/_static/asciinema/:/home/gavin/casts -it fio-asciinema
```

### Inside container

```
asciinema rec <name-of-cast>
```

# demo-magic.sh

This script is used to generate ascii casts in combination with asciinema. If a
demo is included in a section, you should be able to find a `demo/` folder in
that section. For example:

```
source/user-guide/fioctl/
├── demo
│   ├── ug-fioctl-enable-apps.cast
│   └── ug-fioctl-enable-apps.sh
└── index.rst
```

The `fioctl` user-guide section has a `demo/` folder which includes:

1. The cast, as produced by the automation script.
2. The script, which will enact a demo.

The automation script, in this example `ug-fioctl-enable-apps.sh` does not
produce a file, it only executes commands to stdout, as if they were being typed
by a human being, so in order to record this output with Asciinema, you would
run:

```
asciinema rec ./name-of-recording.cast -c ./ug-fioctl-enable-apps.sh
```
