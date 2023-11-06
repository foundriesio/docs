.. _ref-container-secrets:

Using Secret Credentials When Building Containers
=================================================

There are many cases when building a container that sensitive credentials may be required.
Examples include:

 * Downloading a package from a private NPM registry
 * Grabbing a file via ``scp``.

Each scenario requires a slightly different approach in the Dockerfile.
However, the general approach to getting these secrets securely into your container's build context is the same.

 .. note::

    There are several `insecure ways`_ that should be avoided.
    The proper approach is described here based on new functionality in Docker's BuildKit.

 .. _insecure ways:
    https://pythonspeed.com/articles/docker-build-secrets/


Overview of CI Secrets
-----------------------

The FoundriesFactory® CI System, **JobServ**, has a mechanism for configuring secrets for a project—a Factory's LmP build in this case.
These secrets are placed under ``/secrets/`` when a CI Run is executed.
For example, if a Factory has the following secrets:

 * ``secret_1=A Secret Value``
 * ``secret_2=Could even\\nbe multi-line``

Each build run would have the files:

 * ``/secrets/secret_1``
 * ``/secrets/secret_2``

The question is then how to make these accessible to the Dockerfile's build context.

Defining Factory Secrets
------------------------

`Fioctl®`_ includes support for managing secrets for a factory::

  # List secrets defined in the factory:
  fioctl secrets list

  # Add/Update secrets defined in the factory:
  # NOTE: quotes are needed for arguments with spaces or multi-line files
  fioctl secrets update secret_1=blah secret_2="$(cat $HOME/.ssh/id_rsa)"

  # Remove secrets defined in the factory:
  fioctl secrets update secret_1= secret_2=

.. _Fioctl®:
   https://github.com/foundriesio/fioctl

Passing Secrets to Docker's Build Context
-----------------------------------------

Update ``factory-config.yml`` from ci-scripts.git to instruct the build scripts to pass Factory secrets to Docker:

.. code-block:: YAML

    containers:
      docker_build_secrets: true

Update the Dockerfile for the container with something like::

 # syntax=docker/dockerfile:1.0.0-experimental
 # NOTE: - the first line must be this "syntax=" to enable this feature.
 FROM alpine

 # Docker places secrets under /run/secrets/<id>
 RUN --mount=type=secret,id=secret_1 echo "secret_1 is here:" && cat /run/secrets/secret_1
 RUN --mount=type=secret,id=secret_2 echo "secret_2 is here:" && cat /run/secrets/secret_2
