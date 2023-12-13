.. _ref-advanced-tagging:

Advanced Tagging
================

You may sometimes need to incorporate a non-trivial workflow requiring advanced tagging techniques.
These workflows are handled in the :ref:`ref-factory-definition`.

Terminology
-----------

**Platform Build**: A build created by a change in ``lmp-manifest.git`` or ``meta-subscriber-overrides.git``.
This is the base OS image.

**Container Build**: A build created by a change to ``containers.git``.

**Target**: An entry in a Factory's TUF ``targets.json``.
It represents an immutable combination of the Platform build's OSTree hash with the output of a container build.

**Tag**: A Target has a "custom" section where with a list of Tags.
**Tag:**: A user defined attribute of a Target designating its intended usage.
Tags are defined in the "custom" section of a Target.
They can be used to e.g. distinguish between "development" versus "production" builds.

Scenario 1: A New Platform Build That Re-Uses Containers
--------------------------------------------------------

A Factory is set up with the normal ``main`` branch::

  lmp:
    tagging:
      refs/heads/main:
        - tag: main
  containers:
    tagging:
      refs/heads/main:
        - tag: main

You want to introduce a new ``stable`` branch from the LmP, but have it use the latest containers from ``main``.
This can be done with::

  lmp:
    tagging:
      refs/heads/main:
        - tag: main
      refs/heads/stable:
        - tag: stable
          inherit: main
  containers:
    tagging:
      refs/heads/main:
        - tag: main
        - tag: stable

Consider this pseudo Targets example::

  targets:
    build-1:
      ostree-hash: DEADBEEF
      compose-apps: foo:v1, bar:v1
      tags: stable
    build-2:
      ostree-hash: GOODBEEF
      compose-apps: foo:v2, bar:v2
      tags: main

If a change to the stable branch was pushed to the LmP, a new Target, ``build-3``, would be added.
The build logic would then look through the Targets list to find the most recent ``main`` Target.
It can then copy the compose-apps from that most recent Target.
This would result in a new Target::

  build-3:
    ostree-hash: NEWHASH
    compose-apps: foo:v2, bar:v2
    tags: stable

On the other hand, there might also be a new container build for ``main``.
In this case, the build logic will produce two new Targets::

  build-4:  # for stable it will be based on build-3
    ostree-hash: NEWHASH
    compose-apps: foo:v3, bar:v3
    tags: stable

  build-4:  # for master, it will be based on build-2
    ostree-hash: GOODBEEF
    compose-apps: foo:v3, bar:v3
    tags: main

Scenario 2: Multiple Container Builds Using the Same Platform
-------------------------------------------------------------

This scenario is the reverse of the first one.
A Factory might have a platform build tagged with ``main``.
However, there are two versions of containers being worked on: ``main`` and ``foo``.
This could be handled with::

  lmp:
    tagging:
      refs/heads/main:
        - tag: main
        - tag: foo
  containers:
    tagging:
      refs/heads/main:
        - tag: main
      refs/heads/foo:
        - tag: foo
          inherit: main

Scenario 3: Multiple Teams, Different Cadences
----------------------------------------------

Your organization may have separate core platform and application teams.
In this scenario, it may be desirable to let each team move at their own pace.
Furthermore, the application team might have stages(branches) of development they are working on.
This can be handled with something like::

  lmp:
    tagging:
      refs/heads/main:
        - tag: main
  containers:
    tagging:
      refs/heads/main:
        - tag: main
      refs/heads/dev:
        - tag: dev
          inherit: main
      refs/heads/qa:
        - tag: qa
          inherit: main

This will produce ``main`` tagged builds that have no containers, but can be generically verified.
Then, each ``containers.git`` branch will build Targets and grab the latest ``main`` tag to base its platform on.

It is important to note that changes to ``main`` do not cause new container builds.
In order to get a container's branch updated to the latest ``main``, push an empty commit to ``containers.git`` to trigger a new build::

 # from branch qa
 git commit --allow-empty -m 'Pull in latest platform changes from main'
