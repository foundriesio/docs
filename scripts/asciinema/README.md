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
