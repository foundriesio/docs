# PR Template and Checklist

Please complete as much as possible to speed up the reviewing process.
You may delete items that are not relevant to your contribution.
Readiness and adding reviewers as appropriate is required.

All PRs should be reviewed by a technical writer/documentation team and a peer.
If effecting customers—which is a majority of content changes—a member of Customer Success must also review.

## Readiness

* [ ] Merge (pending reviews)
* [ ] Merge after _date or event_
* [ ] Draft

## Checklist

* [ ] Run spelling and grammar check, preferably with linter.
* [ ] Step through instructions (or ask someone to do so).
* [ ] Review for [wordiness](https://languagetool.org/insights/post/wordiness/)
* [ ] Match tone and style of page/section.
* [ ] Run `make linkcheck`, and add redirects for any moved or deleted pages.
* [ ] View HTML in a browser to check rendering.
* [ ] Use [semantic newlines](https://bobheadxi.dev/semantic-line-breaks/).
* [ ] follow best practices for commits.
  * [ ] Descriptive title written in the imperative.
  * [ ] Include brief overview of QA steps taken.
  * [ ] Mention any related issues numbers.
  * [ ] End message with sign off/DCO line (`-s, --signoff`).
  * [ ] Sign commit with your gpg key (`-S, --gpg-sign`).
  * [ ] Squash commits if needed.
* [ ] Request PR review by a technical writer and at least one peer.

## Comments

_Any thing else that a maintainer/reviewer should know._
_This could include potential issues, rational for approach, etc._
