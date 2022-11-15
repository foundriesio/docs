Component or Action
===================

Synopsis(Optional)
------------------

If script/command call, show the generalized invocation. Example:

**command** [*options*] [*--flags*]<*input*> ...

If file or environment variables, show where and what to set, accepted value format. Example:

**repo/folder/config.sh:**
```VAR_NUM = "$VAR_NUM+<numerical value 1–5>" ```

Description
-----------

What it does/what the purpose is. The results or outcomes. Keep it short and technical.

Describe the **type** of options/flags/values, how they are passed, generated or found.

Variables or options
--------------------
(Change section name as appropriate)

.. confval:: IN_JOKE=<option>
    :default: ``gavel``

    .. option:: gavel

       What the value/option/flag does

    **Example Result:**  ``decided``

    .. option:: helicopter

       Changes state to ultimate goal achieved

       **Example Result:** ``We made it!``

.. confval:: -h, --help

    Prints help message

Example Usage (optional)
------------------------

Keep it very simple, more showing than explaining.
You can have a sentence or two of what the example achieves.
For example, a fully configured ``local.conf``,
or a CLI tool showing  a common use-case of the tool.
A walk-through/tutorial/how-to belongs in the user-guide.

.. seealso::
   :ref: `related page <ref-page-lable>

   Link to any related user-guide pages, glossary entries, or reference manual pages.
   For inline links like the one above, keep '< >' as they are part of the syntax.

