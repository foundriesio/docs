.. _docker-apps-k3s:

Rancher k3s Docker App
======================

The `k3s`_ docker app represents a minimalistic single node installation
of `kubernetes`_ capable of running on resource constrained devices such
as the Raspberry Pi. 

Accessing k3s locally
~~~~~~~~~~~~~~~~~~~~~

Once the k3s docker-app is installed, docker will also display it in 
the process status listing of our LMP device::
  
  lmp-device:~$ docker ps
  CONTAINER ID  IMAGE  COMMAND  CREATED  STATUS  PORTS   NAMES
  2d738695a9f8  ra...  "/bi...  3 ho...  Up ...  0.0...  k3s_master_1

From this truncated listing, we see that docker lists the container
name as 'k3s_master_1'. This bit of information will prove useful
when preparing to access our Kubernetes installation remotely.

Accessing k3s via kubectl
~~~~~~~~~~~~~~~~~~~~~~~~~

Before running kubectl commands, we will incorporate config
details from our k3s instance. We may extract them directly from
a running container instance like so::

  lmp-device:~$ docker exec k3s_master_1 cat /var/lib/rancher/k3s/agent/kubeconfig.yaml
  apiVersion: v1
  clusters:
  - cluster:
    certificate-authority-data: ...
    server: https://127.0.0.1:6443
  ...

These resulting details still need to be adapted for our remote
device's '~/.kube/config' file. For the sake of brevity, we'll
just change the cluster entry's server field, from::

  server: https://127.0.0.1:6443

to::
  
  server: https://kubernetes:6443

Then, we'll update our remote device's '/etc/hosts' file to
include this snippet::
  
  <INSERT_IP_ADDRESS_OF_LMP_DEVICE> kubernetes

Assuming the LMP device is accessible from our remote device 
and kubectl is already installed, we may now issue kubectl
commands from our remote device::

  remote-device:~$ kubectl get nodes                                                                                                                                                                     ✔  1701  11:12:23
  NAME           STATUS   ROLES    AGE   VERSION
  2d738695a9f8   Ready    master   20h   v1.15.4-k3s.1

Happy orchestrating!


.. _kubernetes:
   https://github.com/kubernetes/kubernetes
.. _k3s:
   https://github.com/rancher/k3s


