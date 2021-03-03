#!/usr/bin/env python

import subprocess
import datetime
import re

nowe_spotkania = ""
with open("Spotkania.md") as f:
    for line in f:
        if line.startswith("[") and 'pad.hs-ldz.pl' in line:
            data = line.split("[")[1].split("]")[0]
            orig_url = line.split("(")[1].split(")")[0]
            url = orig_url.split("?")[0].strip("#")
            print(data, url, repr(line))
            fname = "Spotkania::" + data.replace(" ", "-")
            with open(fname + ".md", "w") as f:
                s = subprocess.check_output(
                    ["curl", "-s", url + "/download"], encoding="utf-8"
                )
                f.write(
                    s
                    + "\n***\nPrzemigrowano z pada "
                    + url
                    + ". Znajdziesz tam historię edycji sprzed migracji.\n***"
                )
            opis = re.split(".* [-–] (.*)$", line)[1]
            line = (
                "[["
                + data
                + "|"
                + fname
                + "]]<sup>"
                + "[pad]("
                + url
                + ")</sup> - "
                + opis
                + "\n"
            )
        nowe_spotkania += line

with open("Spotkania.md", "w") as f:
    f.write(nowe_spotkania)
