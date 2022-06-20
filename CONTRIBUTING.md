# Contributing

## Before Working on Documentation

While optional, before you begin working:

- [ ] Check Jira

> See if someone is working on it.
If there is no open issue, should there be?
If the fix is going to take more than 30 minutes, consider opening one.

- [ ] Check the default branch to see the if the issue is still relevant.

> The published pages reflect the documentation as of the latest release.
The change may exist and will show up in the next release.

Try to use a fork rather than working on a `foundriesio/docs` branch.
If on a direct branch, include your username.
Branch names should be descriptive and in the imperative (what you *will* do):

```bash
# If working on a branch of foundriesio/docs:
`git checkout -b kprosise/update-contributing-doc

# or for a fork:
git checkout -b spell-check-everything
```

## Working on Documentation

Use spelling and grammar checks and ask a technical writer
if you have questions.
Consult the [style guide](https://foundriesio.atlassian.net/wiki/spaces/ID/pages/2392067/Foundries.io+Style+and+Communication+Guide).

Before pushing, check locally with `make linkcheck` and `make html`.

When opening a PR, tag a technical writer.
They will merge it once reviews are in and suggestions considered.
The [PR template](.github/pull_request_template.md) has additional steps. 

