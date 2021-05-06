## `create-oci-image.nix`

Creates an OCI Image with the tools from `../requirements.txt` + `git` for working
on the docs in any container runtime, such as Docker/Podman.

### Usage:

Build the image and load it into Docker.

```
nix-build create-oci-image.nix
docker load < ./result
```

You may `rm ./result` after this process, it is merely a symlink to where `nix`
built and placed the real artifacts (`/nix/store`). If you want to delete this
artifact entirely, run `nix-collect-garbage` after removing the `./result`.

