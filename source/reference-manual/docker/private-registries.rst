.. _ref-private-registries:

Using Third-Party Private Container Registries
==============================================

Users sometimes need Foundries.io CI services access container images
from a private third-party container registry such as AWS's ECR_.
There are two reasons this would normally happen:

 * A container in ``containers.git`` is based on a private container
   image. e.g. Its Dockerfile has ``FROM <private
   registry>/<container>``

 * A Docker Compose App references a private container image. e.g.
   Its ``docker-compose.yml`` has a line like ``image: <private
   registry>/<container>``

In either case, CI will need read access to the private container image
in order to construct a Target. The :ref:`ref-factory-definition`
(``ci-scripts.git``) provides a way to configure this.


Configuring CI for AWS ECR
--------------------------

CI uses the `aws ecr get-login-password`_ command to authenticate. A
factory can be configured to use this by first providing an AWS
credentials file to CI::

 $ fioctl secrets update aws_creds="$(cat $HOME/.aws/credentials)"

.. note::

   Using a personal credentials file is probably not secure. An AWS
   admin should create an IAM account that can only **pull** from
   the container registry.

Next the factory :ref:`configuration <ref-factory-definition>`
needs to be set. Example configuration::

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

Configuring Devices for AWS ECR
-------------------------------

Devices may need access to private ECR container images. While
bootstrapping a project, it is often easiest to simply copy AWS
credentials to each device. However, before going to production, it is
highly recommend to use an approach that can be backed by x509
certificates such as the ones used for the :ref:`device gateway <ref-device-gateway>`.
`AWS IoT`_ includes a mechanism for eliminating hard-coded
credentials_.

.. _AWS IoT:
   https://aws.amazon.com/iot/
.. _credentials:
   https://aws.amazon.com/blogs/security/how-to-eliminate-the-need-for-hardcoded-aws-credentials-in-devices-by-using-the-aws-iot-credentials-provider/

Configuring for CI Azure Container Registry(ACR)
------------------------------------------------

CI can be configured to use an ACR `service principal`_ with read-only
access to a private ACR instance. First, CI must be configured with
the service principal's ID and password::

 $ fioctl secrets update azprincipal='<ID>:<PASSWORD>'

The factory :ref:`configuration <ref-factory-definition>` is then
updated accordingly::

  # factory-config.yml
  container_registries:
  - type: azure
    url: fiotesting1.azurecr.io
    azure_principal_secret_name: azprincipal

.. _service principal:
   https://docs.microsoft.com/en-us/azure/container-registry/container-registry-auth-service-principal#authenticate-with-the-service-principal
