#!/usr/bin/env python

import subprocess
import pathlib
import collections
import re
import pprint
import colorsys
import math

import mistune


def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))


def optimal_color(i, n):
    hue = (1/n) * i
    light = 1.0
    magic = 0.618033988749895
    magic = 0.3
    hue = math.fmod(i * magic, 1.0)
    light = math.sqrt(1.0 - math.fmod(i * magic, 0.5))
    ret = hsv2rgb(hue, 1, light)
    return '"#' + ''.join([hex(x).split('x')[1].zfill(2) for x in ret]) + '"'


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
                title = f"{ftitle}#{entry['children'][0].get('text', '')}"
            else:
                for child in entry.get('children', []):
                    for user in re.findall('@\w+', child.get('text', '')):
                        projects_per_user[user[1:]].append(title)
    num_users = len(projects_per_user)
    colors_per_user = {}
    for n, user in enumerate(projects_per_user):
        colors_per_user[user] = optimal_color(n, num_users)
    dot = 'graph { rankdir=LR; splines=ortho; ranksep=2; nodesep=0.1;\n'
    for k, v in projects_per_user.items():
        for u in v:
            dot += f'"{k}"--"{u}" [color={colors_per_user[k]}]\n'
    dot += '}'
    rendered = subprocess.check_output(['dot', '-Tsvg'], input=dot.encode())
    with open('media-w-wiki/kto-co-kontroluje.svg', 'wb') as f:
        f.write(rendered)


if __name__ == '__main__':
    main()
