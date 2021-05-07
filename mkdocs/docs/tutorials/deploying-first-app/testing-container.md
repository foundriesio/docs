# Testing the Container

`curl` is not available on your device, instead run `wget` to test the
container like so:

bash device:~$, auto

device:~$ wget -qO- 127.0.0.1:8080

**Example Output**:

text

Hello world

You can also test the container from an external device connected to the
same network (e.g. your host machine: the same computer you use to
access your device with ssh).

bash host:~$, auto

host:~$ \#Example curl 192.168.15.11:8080 host:~$ curl &lt;device
IP&gt;:8080

**Example Output**:

text

Hello world
