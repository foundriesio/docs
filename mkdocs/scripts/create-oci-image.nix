let
  pkgs = import (builtins.fetchTarball {
    name = "nixpkgs";
    url = "https://github.com/nixos/nixpkgs/archive/20.09.tar.gz";
    sha256 = "1wg61h4gndm3vcprdcg7rc4s1v3jkm5xd7lw8r2f67w502y94gcy";
  }) { config = {}; overlays = []; };
  mach-nix = import (builtins.fetchGit {
    url = "https://github.com/DavHau/mach-nix/";
    ref = "refs/tags/3.2.0";
  }) { };
  docker-image = mach-nix.mkDockerImage {
    requirements = builtins.readFile ../requirements.txt;
};
in
docker-image.override (oldAttrs: {
  name = "mkdocs-foundries-env";
  config = {
    entrypoint = [ "mkdocs" ];
    cmd = [ "serve" "-f" "/git/mkdocs.yml" "--dev-addr=0.0.0.0:8000" ];
    ports = [ "8000:8000" ];
    Env = [ "SSL_CERT_FILE=${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt" ];
  };
})
