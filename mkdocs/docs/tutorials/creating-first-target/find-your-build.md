# Find your build

In the previous tutorial, you cloned the `devel` branch. Once your
changes to the `containers.git` repository were pushed, FoundriesFactory
CI automatically started a new `container-devel` build. Go to
<https://app.foundries.io>, select your Factory and click on `Targets`:

The latest **Target** named `containers-devel` should be the CI job you
just created.

<figure>
<img src="/_static/tutorials/creating-first-target/tutorial-find-build.png" class="align-center" width="900" alt="FoundriesFactory Targets" /><figcaption aria-hidden="true">FoundriesFactory Targets</figcaption>
</figure>

The status of the new Target will be `queued` or `building`, depending
on how quickly you reached this page after pushing your changes. Click
anywhere on the Target's line in the list to see more details.

Your FoundriesFactory is configured by default to build your container
for `armhf`, `arm64`, and `amd64`. If you select the `+` signal in a
`building` architecture you will be able to see the live build log:

<figure>
<img src="/_static/tutorials/creating-first-target/tutorial-containers.png" class="align-center" width="900" alt="containers-devel" /><figcaption aria-hidden="true">containers-devel</figcaption>
</figure>

A live log example:

<figure>
<img src="/_static/tutorials/creating-first-target/tutorial-logs.png" class="align-center" width="900" alt="Containers build log" /><figcaption aria-hidden="true">Containers build log</figcaption>
</figure>

When FoundriesFactory CI finishes all three architecture builds, it will
launch a final job to publish your images.

Tip

At this point, the CI job creates a new **Target**.

If all the builds finished without error, the **Target** was created and
published correctly, everything will be marked as `passed`:

<figure>
<img src="/_static/tutorials/creating-first-target/tutorial-finish.png" class="align-center" width="900" alt="Containers build log" /><figcaption aria-hidden="true">Containers build log</figcaption>
</figure>

If you reload the `Target` page, it will indicate new available `Apps`:

<figure>
<img src="/_static/tutorials/creating-first-target/tutorial-tag.png" class="align-center" width="900" alt="Apps available" /><figcaption aria-hidden="true">Apps available</figcaption>
</figure>
