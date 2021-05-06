# nix-build 

let
  pkgs = import (builtins.fetchTarball {
    name = "nixpkgs";
    url = "https://github.com/nixos/nixpkgs/archive/nixos-unstable.tar.gz";
    sha256 = "1s0ckc2qscrflr7bssd0s32zddp48dg5jk22w1dip2q2q7ks6cj0";
  }) { config = {}; overlays = []; };
  mach-nix = import (builtins.fetchGit {
    url = "https://github.com/DavHau/mach-nix/";
    ref = "refs/tags/3.2.0";
  }) { inherit pkgs; };
  docker-image = mach-nix.mkDockerImage {
    requirements = builtins.readFile ../requirements.txt;
    packagesExtra = [ pkgs.git openssh.override { withFIDO = false; } ];
};
in
docker-image.override (oldAttrs: {
  name = "mkdocs-foundries-env";
#  contents = oldAttrs.contents ++ [ pkgs.git ];
})
