#!/usr/bin/env python3

import argparse
import collections
from datetime import datetime, timezone, timedelta
from itertools import dropwhile, takewhile
import sys
import textwrap

import pygit2

DEFAULT_INDENT = (' ' * 14)
MERGEUP_SAUCE_TAG = 'LTD mergeup'
HIGHLIGHTS = '''highlights
----------'''
UPSTREAM_CHANGES = '''upstream changes
----------------'''


def mergeup_commits(repository_path, baseline_commit, stop_commit=None):
    repository = pygit2.init_repository(repository_path)
    if stop_commit is None:
        stop_commit = repository.head.target
    walker = repository.walk(stop_commit, pygit2.GIT_SORT_TIME)
    walker.hide(baseline_commit)
    return [c for c in walker if MERGEUP_SAUCE_TAG in c.message]


def mergeup_highlights(commit):
    def is_not_highlights(paragraph):
        return paragraph.lower() != HIGHLIGHTS

    def is_not_upstream_changes(paragraph):
        return paragraph.lower() != UPSTREAM_CHANGES

    paragraphs = commit.message.split('\n\n')
    start = dropwhile(is_not_highlights, paragraphs)
    hls = [hl for hl in takewhile(is_not_upstream_changes, start)]
    return hls[1:]  # skip HIGHLIGHTS itself


def commit_date(commit):
    author_timestamp = float(commit.author.time)
    author_time_offset = commit.author.offset
    author_tz = timezone(timedelta(minutes=author_time_offset))
    return datetime.fromtimestamp(author_timestamp, author_tz)


def main():
    parser = argparse.ArgumentParser(
        description='''Script which searches Git history for 'Highlights'
                    commit log messages in LTD mergeup commits.''')
    parser.add_argument('-c', '--commit', default=None,
                        help='Commit to start from (default is HEAD)''')
    parser.add_argument('-i', '--indent', default=DEFAULT_INDENT,
                        help='Indentation to apply when printing.')
    parser.add_argument('repo',
                        help='''Path to repository to search.''')
    parser.add_argument('baseline',
                        help='''Baseline commit to begin search
                        for mergeup highlight commit messages.''')

    args = parser.parse_args()

    mergeups = mergeup_commits(args.repo, args.baseline,
                               stop_commit=args.commit)
    highlights = collections.OrderedDict((m, mergeup_highlights(m))
                                         for m in mergeups)
    missing = []
    wrapper = textwrap.TextWrapper(initial_indent=args.indent,
                                   subsequent_indent=args.indent)
    for m, hls in highlights.items():
        if not hls:
            missing.append(m)
            continue
        print('From mergeup {} on {}:'.format(str(m.id)[:7], commit_date(m)))
        for hl in hls:
            print(wrapper.fill(hl))
            print()
    if missing:
        print(file=sys.stderr)
        print('WARNING: the following mergeup commit(s) had no highlights.',
              file=sys.stderr)
        for m in missing:
            print('ID: {}'.format(m.id), file=sys.stderr)
            print('Date: {}'.format(commit_date(m)), file=sys.stderr)
            print('Message:', file=sys.stderr)
            print(textwrap.indent(m.message, '\t'), file=sys.stderr)


if __name__ == '__main__':
    main()
