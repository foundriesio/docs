Find Your Build
^^^^^^^^^^^^^^^

Once your changes to the :term:`containers.git` repository were pushed, the FoundriesFactory™ Platform CI automatically started a new ``container-main`` build.
Go to https://app.foundries.io, select your Factory and click on :guilabel:`Targets`:

The latest **Target** named :guilabel:`containers-main` should be the CI job you just created.

.. figure:: /_static/tutorials/creating-first-target/tutorial-find-build.png
   :width: 900
   :align: center

   FoundriesFactory Targets

The status of the new Target will be :guilabel:`queued` or :guilabel:`building`, depending on how recently you pushed the changes.
Click anywhere on the Target's line in the list to see more details.

Your Factory is configured by default to build your container for ``armhf``, ``arm64``, and ``amd64``.
If you select the :guilabel:`+` signal in a :guilabel:`building` architecture you will be able to see the live build log:

.. figure:: /_static/tutorials/creating-first-target/tutorial-containers.png
   :width: 900
   :align: center

   containers-main

A live log example:

.. figure:: /_static/tutorials/creating-first-target/tutorial-logs.png
   :width: 900
   :align: center

   Containers build log

When the FoundriesFactory CI finishes all your builds, it will launch a final job to publish your images.

.. tip::

   At this point, the CI job creates a new **Target**.

If all the builds finish without error, the **Target** is created and published and everything will be marked as :guilabel:`passed`.

.. figure:: /_static/tutorials/creating-first-target/tutorial-finish.png
   :width: 900
   :align: center

   Passed Targets

If you reload the :guilabel:`Target` page, it will indicate new available :guilabel:`Apps`.

.. figure:: /_static/tutorials/creating-first-target/tutorial-tag.png
   :width: 900
   :align: center

   Apps available
