.. _ref-advanced-tagging:

Advanced Tagging
================

The ``OTA_LITE_TAG`` variable can be used in a few ways to add advanced
tagging capabilities to a factory.

Terminology
-----------

**Platform Build** - A build created by a change to the LMP/OE. This is the
base OS image.

**Container Build** - A build created by a change to containers.git.

**Target** - This an entry in a factory's TUF targets.json file. It represents
what should be thought of as an immutable combination of the Platform build's
OSTree hash + the output of a Container build.

**Tag** - A Target has a "custom" section where with a list of Tags. The
tags can be used to say things like "this is a development build"
or this is a "production" build.


OTA_LITE_TAG
------------

The ``OTA_LITE_TAG`` determines what tag a target will get when a container
or platform build is performed. The format is::

  TAG[:INHERIT_TAG][,TAG[:INHERIT_TAG]....]


Scenario 1: A new platform build that re-uses containers
--------------------------------------------------------

Consider the case where a factory might have a tag called "postmerge" defined
for both the lmp.yml and containers.yml builds. A new branch is added to the
LMP called "postmerge-stable" that's going to be based on older, more stable
code. However, this new build will use the containers found in the most
recent "postmerge" target. This can be expressed in lmp.yml with::

  OTA_LITE_TAG: "postmerge-stable:postmerge"

However, this means that changes to containers.git will now also need to
produce a new "postmerge-stable" target. So containers.yaml would need to
be update with::

  OTA_LITE_TAG: "postmerge,postmerge-stable"

Consider this pseudo targets example::

  targets:
    build-1:
      ostree-hash: DEADBEEF
      docker-apps: foo:v1, bar:v1
      tags: postmerge-stable
    build-2:
      ostree-hash: GOODBEEF
      docker-apps: foo:v2, bar:v2
      tags: postmerge

If a change to the postmerge-stable branch was pushed to the LMP, a new
target, build-3, would be added. The build logic would then look through
the targets list to find the most recent "postmerge" target so that
it can copy those docker-apps. This would result in a new target::

  build-3:
    ostree-hash: NEWHASH
    docker-apps: foo:v2, bar:v2
    tags: postmerge-stable


On the other hand, there might also be a new container build for "postmerge".
In this case the tag specification ``postmerge,postmerge-stable`` would tell
the build logic to produce two new targets::

  build-4:  # for postmerge-stable it will be based on build-3
    ostree-hash: NEWHASH
    docker-apps: foo:v3, bar:v3
    tags: postmerge-stable

  build-4:  # for postmerge, it will be based on build-2
    ostree-hash: GOODBEEF
    docker-apps: foo:v3, bar:v3
    tags: postmerge


Scenario 2: Multiple container builds using the same platform
-------------------------------------------------------------

This scenario is the reverse of the previous one. A factory might have a
platform build tagged with "devel-X". However, there are two versions of
containers being worked on: "devel-X" and "devel-Y". This could be handled
by changing lmp.yml to::

 OTA_LITE_TAG: "devel-X,devel-Y"


and containers.yml to::

 OTA_LITE_TAG: "devel-X,devel-Y:devel-X"

Scenario 3: Multiple teams, different cadences
----------------------------------------------

Some organizations may have separate core platform and application teams. In
this scenario, it may be desirable to let each team move at their own decoupled
paces. Furthermore, the applications team might have stages(branches) of
development they are working on. This could be handled by changing lmp.yml to::

 OTA_LITE_TAG: "devel-core"

Then each branch of development for the containers could have things like::

 # For the "app-dev" branch of containers.git
 OTA_LITE_TAG: "app-dev:devel-core"

 # For the "app-qa" branch of containers.git
 OTA_LITE_TAG: "app-qa:devel-core"

This scenario is going to produce ``devel`` tagged builds that have no
containers, but can be generically verfied. Then each containers.git branch
will build targets and grab the latest "devel-core" tag to base its platform
on. **NOTE:** Changes to devel-core don't cause new container builds. In
order to get a container's branch updated to the latest ``devel-core`` a user
would need to push an empty commit to containers.git to trigger a new build.
eg::

 # from branch app-dev
 git commit --allow-empty -m 'Pull in latest devel-core changes'
