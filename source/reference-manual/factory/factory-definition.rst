.. _ref-factory-definition:

Factory Definition
==================

Each Factory can be customized to control how CI handles it. This is managed
in the "Factory Definition" which is located in a factory's ci-scripts.git
repository in the file `factory-config.yml`::

  notify:
    email:
      # Required: Comma separated list of email addresses to mailed after each CI build.
      users: foo@foo.com
      # Optional: If set to "true" users will only be notified of CI failures.
      # failures_only: false

  lmp:
    # Optional: Specify environment variable to be passed into the LMP build
    # params:
    #   IMAGE: lmp-mini

    # Required: Specify the list of LMP machines to build for. A factory's
    #           subscription is generally only good for a single "machine".
    machines:
    - raspberrypi-cm3

    # Optional: Override options when specific git references are updated
    # ref_options:
    #  refs/heads/devel:
    #    machines:  # Optional: This requires foundries.io support to change
    #      - raspberrypi3-64
    #    params:    # Optional: Add/Override environment variables in build
    #      IMAGE: lmp-mini

    # Optional: Control how OTA_LITE tags are handled.
    #           See "Advanced Tagging" for more details
    # tagging:
    #  refs/heads/master:
    #    - tag: postmerge
    #  refs/heads/devel:
    #    - tag: devel

    # Optional: Do an OE build to produce manufacturing tooling
    # mfg_tools:
    #  - machine: raspberrypi-cm3
    #    params:
    #      DISTRO: lmp-base
    #      IMAGE: mfgtool-signed-files
    #      EXTRA_ARTIFACTS: "mfgtools-signed.tar.gz"

  containers:
    # Optional: Only build containers for the given platforms
    # platforms:
    # - arm
    # - arm64
    # - amd64

    # Optional: Control how OTA_LITE tags are handled.
    #           See "Advanced Tagging" for more details
    # tagging:
    #  refs/heads/master:
    #    - tag: postmerge
    #  refs/heads/devel-foundries:
    #    - tag: devel
    #  refs/heads/devel-foundries-base:
    #    - tag: devel-base
    #      inherit: devel
