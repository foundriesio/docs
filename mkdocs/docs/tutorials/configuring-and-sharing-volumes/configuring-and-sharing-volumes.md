# Configuring and Sharing Volumes

In this tutorial, you will learn different techniques that will help you
configure your device.

The goal is to cover different techniques including `fioctl config`.
With `fioctl` you can securely send configuration files to the device.
The `fioconfig` service, which is a daemon running on the device, pulls
the secure configuration files down and decrypts them during boot.

Note

Estimated Time to Complete this Tutorial: 20 minutes

## Learning Objectives

-   Change the shellhttpd application to consume a static configuration
    file.
-   Share a folder allowing you to dynamically change your
    configuration.
-   Use `fioctl` with `fioconfig` to securely send a dynamic
    configuration to the device.

## Prerequisites

-   Completed the `tutorial-gs-with-docker` tutorial.
-   Completed the `tutorial-creating-first-target` tutorial.
-   Completed the `tutorial-deploying-first-app` tutorial.

## Instructions

modify-shellhttpd-container copy-configuration-file-using-dockerfile
sharing-folder dynamic-configuration-file update-shellhttpd-application
configuring-and-sharing-volumes-summary
