# Dockerfile

The first file you will use is the `Dockerfile`. Enter the `shellhttpd`
folder and move the `Dockerfile` from `shellhttpd.disabled` to
`shellhttpd`:

bash host:~$

cd shellhttpd mv ../shellhttpd.disabled/Dockerfile .

The `Dockerfile` contains all the commands a user would call on the
command line to assemble a container image.

A `Dockerfile` usually starts from a base image. The base image could be
a distribution such as Alpine, Debian, or Ubuntu or it could be a
distribution already prepared for a specific application like Python,
NGINX.

Think of the `Dockerfile` as your way of customizing the base image.

Tip

For more information, see the [Dockerfile
Reference](https://docs.docker.com/engine/reference/builder/)

Check the content of your `Dockerfile`:

bash host:~$, auto

host:~$ cat Dockerfile

**Dockerfile**:

text

FROM alpine COPY httpd.sh /usr/local/bin/ CMD
\["/usr/local/bin/httpd.sh"\]

This `Dockerfile` is very simple and a great way to get started.

The first line creates a layer from the latest [Alpine Docker
image](https://hub.docker.com/_/alpine). This means that your final
image contains all the files provided by this image plus your additions.

Your first customization is in the second line. `COPY` adds files from
your Docker client’s current directory to your Docker image. In this
case, you will copy the shell script `httpd.sh` to the `/usr/local/bin/`
directory of your Docker image.

Last but not least there is `CMD`, these are arguments for the
`ENTRYPOINT`. In this example, there is no `ENTRYPOINT` specified
because the default entrypoint is enough.

The default entrypoint is `/bin/sh -c` and by passing
`/usr/local/bin/httpd.sh` as `CMD` you are configuring the image to
execute the command line: `/bin/sh -c  /usr/local/bin/httpd.sh` when you
run the container.
