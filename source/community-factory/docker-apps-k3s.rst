.. _docker-apps-k3s:

Rancher k3s Docker App
======================

The `k3s`_ docker app represents a minimalistic single node installation
of `kubernetes`_ capable of running on resource constrained devices such
as the Raspberry Pi. 

Accessing k3s locally
~~~~~~~~~~~~~~~~~~~~~

Once the k3s docker-app is installed, docker will display it in the
process status listing of the target LMP device::
  
  lmp-device:~$ docker ps
  CONTAINER ID  IMAGE  COMMAND  CREATED  STATUS  PORTS   NAMES
  2d738695a9f8  ra...  "/bi...  3 ho...  Up ...  0.0...  k3s_master_1

The truncated listing shows the ``k3s_master_1`` container running. This
bit of information will prove useful when preparing to access the
Kubernetes installation remotely.

Accessing k3s via kubectl
~~~~~~~~~~~~~~~~~~~~~~~~~

Before running kubectl commands, config details must be incorporated
from the k3s instance. They may be extracted directly from a running
container instance like so::

  lmp-device:~$ docker exec k3s_master_1 cat /var/lib/rancher/k3s/agent/kubeconfig.yaml
  apiVersion: v1
  clusters:
  - cluster:
    certificate-authority-data: ...
    server: https://127.0.0.1:6443
  ...

The resulting output still needs to be adapted for the host's
``~/.kube/config`` file. For the sake of brevity, just change the 
cluster entry's server field, from::

  server: https://127.0.0.1:6443

to::
  
  server: https://kubernetes:6443

Then, add this snippet to the host machine's ``/etc/hosts`` file::
  
  <INSERT_IP_ADDRESS_OF_LMP_DEVICE> kubernetes

Assuming the target device is accessible from the host machine and
kubectl is already installed, kubectl commands may now be issued from
the host::

  host-machine:~$ kubectl get nodes                                                                                                                                                                     ✔  1701  11:12:23
  NAME           STATUS   ROLES    AGE   VERSION
  2d738695a9f8   Ready    master   20h   v1.15.4-k3s.1

Happy orchestrating!


.. _kubernetes:
   https://github.com/kubernetes/kubernetes
.. _k3s:
   https://github.com/rancher/k3s


