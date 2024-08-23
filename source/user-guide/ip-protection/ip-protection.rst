.. _ref-ug-ip-protection:

Intellectual Property Protection
================================

Protecting your Intellectual Property (IP) is important to us.
Foundries.io™ follows best practices to make sure your code is protected while using the FoundriesFactory™ Platform.

.. seealso::
   :ref:`ref-data-retention`

Here are additional steps you can take to keep your Factory even more secure and isolate source code access:

* Build your own container images, and have FoundriesFactory CI pull these containers using ``secrets``. See :ref:`ref-private-registries`.

* Use git submodules inside compose-apps which point at private git repos. With this, only FoundriesFactory CI builders can access the code by using ``secrets``. Foundries.io team members cannot. See :ref:`ug-submodule`.

* In a similar manner, you can add Yocto Project recipes which reference private git repos, also accessible by FoundriesFactory CI builders with proper ``secrets`` set. See :ref:`ref-ug-private-repo`.

* Manage source access via ``Teams`` permissions. A Foundries.io support engineer can be temporarily invited with restrict source code access, so that they can help with other aspects of your Factory. See :ref:`ref-team-based-access`.
