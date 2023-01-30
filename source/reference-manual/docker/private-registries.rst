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


Configuring for CI Azure Container Registry (ACR)
-------------------------------------------------

CI can be configured to use an ACR `service principal`_ with read-only
access to a private ACR instance. First, CI must be configured with
the service principal's ID and password::

 $ fioctl secrets update azprincipal='<ID>:<PASSWORD>'

The factory :ref:`configuration <ref-factory-definition>` is then
updated accordingly::

  # factory-config.yml
  container_registries:
  - type: azure
    url: <YOUR REGISTRY>.azurecr.io
    azure_principal_secret_name: azprincipal

.. _service principal:
   https://docs.microsoft.com/en-us/azure/container-registry/container-registry-auth-service-principal#authenticate-with-the-service-principal

.. _ref-acr-devices:

Configuring Devices for ACR
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Azure does not include a built-in way for devices to `securely access`_
a container registry like AWS IoT does. The recommended approach for
this scenario is pushing container images from ACR into
`hub.foundries.io` or having a container image built with something similar to::

 # containers.git <CONTAINER>/Dockerfile
 FROM <YOUR REGISTRY>.azurecr.io

Then compose apps can reference this `hub.foundries.io` container image.

.. _securely access:
   https://docs.microsoft.com/en-us/answers/questions/734990/iot-device-authentication-with-acr.html

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Another approach is to follow the procedure as outlined for devices accessing
the :ref:`Azure Container Registry <ref-acr-devices>`. This wraps the container
images into `hub.foundries.io` . With this setup, devices rely on the Factory
authentication instead of authenticating to AWS ECR.

Configuring for CI Google Artifact Registry (GAR)
-------------------------------------------------

CI can be configured to use a Google Compute Platform(GCP)
`service account`_ with read-only access to a private GAR instance. A
service account can be created that may only do Docker pull operations
with::

 # Create the service account
 $ NAME=<user name, eg "fio-ci">
 $ gcloud iam service-accounts create ${NAME}

 # Grant it minimal access to your GCP account:
 $ GAR_NAME=<Registry name, eg "fio-containers">
 $ LOCATION=<GCP region, eg "us-central-1">
 $ PROJ_ID=<GCP project ID>
 $ gcloud artifacts repositories add-iam-policy-binding \
     ${GAR_NAME} --location=us-central1 \
     --member=serviceAccount:${NAME}@${PROJ_ID}.iam.gserviceaccount.com \
     --role=roles/artifactregistry.reader

 # Create the service account key file required by CI:
 $ gcloud iam service-accounts keys create \
   application_default_credentials.json \
   --iam-account=${NAME}@${PROJ_ID}.iam.gserviceaccount.com

The service account key file created above then needs to be configured
for CI with::

 $ fioctl secrets update gcp_creds==application_default_credentials.json

The factory :ref:`configuration <ref-factory-definition>` is then
updated accordingly::

  # factory-config.yml
  container_registries:
  - type: gar
    gar_creds_secret_name: gcp_creds

.. _service account:
   https://cloud.google.com/iam/docs/service-accounts

Configuring Devices for GAR
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Google does not have a way to authenticate it's IoT core devices with
the Artifact Registry. We recommend following the same approach as
outlined for devices accessing the :ref:`Azure Container Registry <ref-acr-devices>`.
