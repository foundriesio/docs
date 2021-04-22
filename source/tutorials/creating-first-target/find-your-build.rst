Find your build
^^^^^^^^^^^^^^^

Remember that in the previous tutorial, you cloned the ``devel`` branch. 
Right after the push, our CI will automatically trigger a new ``container-devel`` build.
Go to https://app.foundries.io, select your Factory and click on :guilabel:`Targets`:

The last **Target** named :guilabel:`containers-devel` should be the CI job you just created.

.. figure:: /_static/tutorials/creating-first-target/tutorial-find-build.png
   :width: 900
   :align: center

   FoundriesFactory Targets

Click on it and if you are checking it right after the ``git push``, you might 
be able to see the CI jobs on :guilabel:`queued` and/or :guilabel:`building` status.

Your FoundriesFactory is configured by default to build your container for 
``arm32``, ``arm64``, and ``x86``. If you select the :guilabel:`+` signal in a 
:guilabel:`building` architecture you will be able to see the live build log:

.. figure:: /_static/tutorials/creating-first-target/tutorial-containers.png
   :width: 900
   :align: center

   containers-devel

A live log example:

.. figure:: /_static/tutorials/creating-first-target/tutorial-logs.png
   :width: 900
   :align: center

   Containers build log

When the CI finishes the three different architecture builds, it will launch a 
final job to publish your images.

.. tip::

   At this point is where the CI job creates a **Target**

If all the builds finished without error, the **Target** was created and published correctly, 
everything will be marked as :guilabel:`passed`:

.. figure:: /_static/tutorials/creating-first-target/tutorial-finish.png
   :width: 900
   :align: center

   Containers build log

If you reload the :guilabel:`Target` page, it will indicate a new :guilabel:`Apps` available:

.. figure:: /_static/tutorials/creating-first-target/tutorial-tag.png
   :width: 900
   :align: center

   Apps available
