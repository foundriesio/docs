.. _tutorial-compose-app-checking-app-state:

Checking App State
^^^^^^^^^^^^^^^^^^

This page outlines App status reporting and how to check the state of Apps running on a device.

The *update agent* running on a device inquires Docker Engine on the state of App containers.
The agent then processes the response and sends a state summary to the Device Gateway.
The state inquiry happens periodically and before checking for an update.
The :ref:`aktualizr-lite parameter <ref-aktualizr-lite-params>` ``polling_sec`` defines the update check interval.
It is responsible for the App state inquiry interval as well.

``aktualizr-lite`` reports a state summary:

- only if it has changed since the last check
- directly after device reboot
- when ``aktualizr-lite`` restarts.

.. Important:: The FoundriesFactory™ Platform's backend stores just the last 10 states.

If enabled, container health is determined by a `health check`_ script.
Otherwise, container health is deduced from a container state and exit code.
A healthy container is one in either a ``running`` state or a ``exited`` state with an exit code equal to zero.
An App state is *healthy* only if each container/service is *healthy*.

View a summary of App state using the ``fioctl devices show <device name>`` command.
The output lists *healthy* and *unhealthy* Apps. For example:

.. prompt:: text

        fioctl devices show 58e6e47d-3d2c-415b-afa4-cdc5e0229355

        UUID:		58e6e47d-3d2c-415b-afa4-cdc5e0229355
        Owner:		5e9dc69d7407c5010eed1c5a
        Factory:	<factory>
        Production:	false
        Up to date:	true
        Target:		intel-corei7-64-lmp-1526 / sha256(d6c101e33e6403f8c9aac18b8f8b1393a6b6866eead53631756c90f97b2838eb)
        Ostree Hash:	d6c101e33e6403f8c9aac18b8f8b1393a6b6866eead53631756c90f97b2838eb
        Created At:	2022-08-12T12:58:28+00:00
        Created By:	5e9dc69d7407c5010eed1c5a
        Last Seen:	2022-08-12T13:21:04+00:00
        Tag:		master
        Docker Apps:	app-03,app-04,app-05,app-06,one-shot,one-shot-failing
        Healthy Apps:	one-shot
        Unhealthy Apps:	one-shot-failing,app-06,app-05,app-04,app-03


Inspect the reported states by running ``fioctl devices apps-states <device name>``.
The command prints the last reported state by default.
To output more states, use the ``-n/--limit`` flag.

The output uses the following template:

::

    Time: <timestamp when an Apps state was captured on device, in RFC3339 format>
    Ostree: <ostree commit hash that device's rootfs is based on>

    Unhealthy Apps: <following is a list of *unhealthy* Apps>
        <app-name>:   ["uri": <a pinned App URI, optional>]
                <service-name>:
                    "URI": <a pinned service image URI>
                    "Hash": <a service hash>
                    "Health": <a service container health reported by Docker Engine or deduced from its state>
                    "State": <a service container state reported by Docker Engine>
                    "Status": <a service container status reported by Docker Engine>,
                    "Logs": <last 5 lines of logs yielded by a service container, optional, present only if a container is unhealthy>

    Healthy Apps: <following is a list of *healthy* Apps>
        ...


For example:

.. prompt:: text

        fioctl devices apps-states 58e6e47d-3d2c-415b-afa4-cdc5e0229355

        Time:	2022-08-12T13:02:29Z
        Hash:	d6c101e33e6403f8c9aac18b8f8b1393a6b6866eead53631756c90f97b2838eb
        Unhealthy Apps:
            app-04
                python-www:
                    URI:	hub.foundries.io/factory/app-04@sha256:e03d32df200df34b329672f88040b3d3e73c3daec3de13bdc7f1e7ae214079d7
                    Hash:	e1d31eb6da9212897b65e3a1540b48c28ffed8aaba10957119644cb4735056b5
                    Health:	unhealthy
                    State:	exited
                    Status:	Exited (137) 6 seconds ago

            app-03
                python-www-unhealthy:
                    URI:	hub.foundries.io/factory/app-03@sha256:46793e7be135b55ad25bb5534fe08fcaac4020bcbea993cf951aa81a3a6195a1
                    Hash:	f9fb1e2d6e45910622ea07515694e42e2537a244ce1a5f8a135109b063b24e07
                    Health:	unhealthy
                    State:	exited
                    Status:	Exited (137) 6 seconds ago
                python-www-healthy:
                    URI:	hub.foundries.io/factory/app-03@sha256:46793e7be135b55ad25bb5534fe08fcaac4020bcbea993cf951aa81a3a6195a1
                    Hash:	510755297019574f03ffa9ccf7c5844c6858600c142b8f639c0876e3a34050dd
                    Health:	unhealthy
                    State:	exited
                    Status:	Exited (137) 6 seconds ago
                    Logs:
                     | <127.0.0.1 - - [12/Aug/2022 13:02:13] "GET / HTTP/1.1" 200 -
                     | <127.0.0.1 - - [12/Aug/2022 13:02:14] "GET / HTTP/1.1" 200 -
                     | <127.0.0.1 - - [12/Aug/2022 13:02:15] "GET / HTTP/1.1" 200 -
                     | <127.0.0.1 - - [12/Aug/2022 13:02:16] "GET / HTTP/1.1" 200 -
                     | <127.0.0.1 - - [12/Aug/2022 13:02:17] "GET / HTTP/1.1" 200 -
                     |

            one-shot-failing
                one-shot-app:
                    URI:	hub.foundries.io/factory/alpine@sha256:aef972662b84a23eb55b87caec80967f2c6a1d6f697cb16822bf75e2bfece82a
                    Hash:	8022ec49a307494af0fbffea90ac32e7eb3da4eb894d24b262651a296f31d090
                    Health:	unhealthy
                    State:	exited
                    Status:	Exited (1) 2 minutes ago

            app-06
                python-www:
                    URI:	hub.foundries.io/factory/app-06@sha256:cedad68098623033c60f7ee69c6a45da337aa66cfb9d610deb8a7c2b5de74e44
                    Hash:	5e37e8078a673d2970db60f65a4bb47fc504a3f63945bc8b66d0ee16e3649727
                    Health:	unhealthy
                    State:	exited
                    Status:	Exited (137) 6 seconds ago

            app-05
                python-www:
                    URI:	hub.foundries.io/factory/app-05@sha256:0ec7cd4f8e0443f26f5d1173a6415cb394bebebb9c50339ea1e7a396988c4e63
                    Hash:	f1d3106d102f615c90685fe0de7f472e4a7ac402dfe22489250975b42ed0a432
                    Health:	unhealthy
                    State:	exited
                    Status:	Exited (137) 58 seconds ago

        Healthy Apps:
            one-shot
                one-shot-app:
                    URI:	hub.foundries.io/factory/alpine@sha256:aef972662b84a23eb55b87caec80967f2c6a1d6f697cb16822bf75e2bfece82a
                    Hash:	8022ec49a307494af0fbffea90ac32e7eb3da4eb894d24b262651a296f31d090
                    Health:	healthy
                    State:	exited
                    Status:	Exited (0) 2 minutes ago


Also, by enabling Event Queue for a Factory, you can subscribe for App state change events.
The event type for an App state is ``DEVICE_OTA_APPS_STATE_CHANGED``. See :ref:`Event Queues <ref-event-queues>` for more details.


.. _health check:
   https://docs.docker.com/engine/reference/builder/#healthcheck
