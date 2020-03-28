#!/usr/bin/env python

import subprocess
import pathlib
import collections
import re
import pprint

import mistune


WIKI_URL = 'https://github.com/hakierspejs/wiki.wiki.git'


def main():
    if not pathlib.Path('wiki.wiki').exists():
        subprocess.call(['git', 'clone', WIKI_URL])
    markdown = mistune.create_markdown(renderer=mistune.AstRenderer())
    with open('wiki.wiki/Infrastruktura.md') as f:
        parsed = markdown(f.read())
    last_heading = None
    projects_per_user = collections.defaultdict(list)
    for entry in parsed:
        if entry['type'] == 'heading':
            last_heading = entry['children'][0]['text']
        else:
            for child in entry.get('children', []):
                for user in re.findall('@\w+', child.get('text', '')):
                    projects_per_user[user].append(last_heading)
    pprint.pprint(dict(projects_per_user))


if __name__ == '__main__':
    main()
