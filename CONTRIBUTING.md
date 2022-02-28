# Contributing

## Before Working on Documentation

While optional, before you begin working:

- [ ] Check Jira

> See if someone is working on it. If there is no open issue, should there
be? If the fix is going to take more than 30 minutes, consider opening one. Is
it connected to a feature or bug fix task or story? Add documentation as a
subtask, and make sure to mention any related tasks in your commit message.

- [ ] Check the default ("master") branch to see the if work still needs to get
      done

> The published pages reflect the documentation as of the latest release. It is
possible that the change has been implemented and will be included in
the next release.

- [ ] Consider filling out a [Change to Documentation Form](https://forms.gle/RoxtTQEvh72fFKeD8)

> The form can be helpful if: you do not know where to place content, you
want to work with a technical writer, or you notice something that needs fixing.
You should fill it out anytime you add a new feature.

It is recommended that you create a fork rather than working on a
`foundriesio/docs` branch. If on a direct branch, include your username. In any
instance, the branch name should be descriptive and in the
imperative (what you *will* do):

```bash
# If working on a branch of foundriesio/docs:
`git checkout -b kprosise/update-contributing-doc

# or for a fork:
git checkout -b spell-check-everything
```

## Working on Documentation

Try to use spelling and grammar checks when possible and ask a technical writer
if you have questions. You should consult the [style guide](https://foundriesio.atlassian.net/wiki/spaces/ID/pages/2392067/Foundries.io+Style+and+Communication+Guide)
for guidelines and suggestions. The style guide is a "living document", check
for changes periodically.

Before committing run a language linter. Currently the documentation is written
in rst, and can be checked with
[restructuredtext-lint](https://github.com/twolfson/restructuredtext-lint).

Prior to pushing, render and check locally.

When opening a Pull Request, tag a technical writer who will merge it into
the default branch once reviews have been finished or it is deemed complete.

