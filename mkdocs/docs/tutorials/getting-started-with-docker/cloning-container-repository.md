# Cloning Container Repository

Tip

When your Factory is first created, 2 branches are established: `master`
and `devel`. We suggest using the `devel` branch for development. Once
those changes are tested and approved, migrate them to `master`.

Clone your `containers.git` repo and enter its directory:

bash host:~$

git clone -b devel
<https://source.foundries.io/factories/>&lt;factory&gt;/containers.git
cd containers

Your `containers.git` repository is initialized with a simple
application example in `shellhttpd.disabled`

Tip

Directory names ending with `.disabled` in `containers.git` are
**ignored** by FoundriesFactory CI.

For better understanding, it is easier to consume the files in
`shellhttpd.disabled` gradually. Create a new folder with the name
`shellhttpd`:

bash host:~$

mkdir shellhttpd

Your `containers.git` repository should look like this:

containers/ ├── README.md ├── shellhttpd └── shellhttpd.disabled ├──
docker-build.conf ├── docker-compose.yml ├── Dockerfile └── httpd.sh
