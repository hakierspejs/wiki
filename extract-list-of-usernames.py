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
    projects_per_user = collections.defaultdict(list)
    for fname in pathlib.Path('wiki.wiki').glob('**/*.md'):
        with open(fname) as f:
            parsed = markdown(f.read())
        ftitle = '/'.join([
            x[:-3] if x.endswith('.md') else x for x in fname.parts[1:]
        ])
        title = None
        for entry in parsed:
            if entry['type'] == 'heading':
                title = f"{ftitle}#{entry['children'][0]['text']}"
            else:
                for child in entry.get('children', []):
                    for user in re.findall('@\w+', child.get('text', '')):
                        projects_per_user[user[1:]].append(title)
    for user in sorted(projects_per_user, key=lambda x: x.lower()):
        print(f'\n# {user}\n')
        for project in sorted(projects_per_user[user]):
            print(f' * [[{project}]]')


if __name__ == '__main__':
    main()
