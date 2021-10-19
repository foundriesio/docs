.. _ref-private-registries:

Using Third-Party Private Container Registries
==============================================

Users sometimes need Foundries.io CI services access container images
from a private third-party container registry such as AWS's ECR_.
There are two reasons this would normally happen:

 * A container in ``containers.git`` is based on a private container
   image. e.g. It's Dockerfile has ``FROM <private
   registry>/<container>``

 * A Docker Compose App references a private container image. e.g.
   It's ``docker-compose.yml`` has a line like ``image: <private
   registry>/<container>``

In either case, CI will need read access to the private container image
in order to construct a Target. The :ref:`ref-factory-definition`
(``ci-scripts.git``) provides a way to configure this.


Configuring for AWS ECR
-----------------------

CI uses the `aws ecr get-login-password`_ command to authenticate. A
factory can be configured to use this by first providing an AWS
credentials file to CI::

 $ fioctl secrets update aws_creds="$(cat $HOME/.aws/credentials)"

.. note::

   Using a personal credentials file is probably not secure. An AWS
   admin should create an IAM account that can only **pull** from
   the container registry.

Then set the factory configuration with something like::

  # factory-config.yml
  container_registries:
  - type: aws
    region: us-east-2
    url: XXXXXXXXXX.dkr.ecr.us-east-2.amazonaws.com
    aws_creds_secret_name: aws_creds

.. _ECR:
   https://aws.amazon.com/ecr/

.. _aws ecr get-login-password:
   https://docs.aws.amazon.com/cli/latest/reference/ecr/get-login-password.html
