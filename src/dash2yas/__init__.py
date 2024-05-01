from collections import namedtuple
import csv
import re

dash_ph_pattern = re.compile(r"__([a-zA-Z0-9\-]+)__")

yas_template = """
# -*- mode: snippet -*-
# name: {name}
# key: {key}
# --

{body}$0
""".strip()


class Snippet(namedtuple("Snippet", ["mode", "key", "body"])):
    __slots__ = ()

    @classmethod
    def from_csv_row(__cls__, row):
        mode = row[0]
        key = row[1]
        body = row[2].replace("\\n", "\n")
        return __cls__(mode, key, body)

    @property
    def name(self):
        return self.key.replace("/", " ").replace("-", " ")


def placeholder_mapping(body):
    matches = dash_ph_pattern.findall(body)
    placeholders = {}
    for i, m in enumerate(matches):
        k = "__{0}__".format(m)
        if k not in placeholders:
            v = "${" + "{0}:{1}".format(i + 1, m) + "}"
            placeholders[k] = v
    return placeholders


def render_yasnippet(snippet):
    body = snippet.body
    for k, v in placeholder_mapping(snippet.body).items():
        body = body.replace(k, v)
    return yas_template.format(name=snippet.name, key=snippet.key, body=body)


def main():
    dry_run = True
    with open("to_import.csv", "r") as f:
        for row in csv.reader(f):
            snippet = Snippet.from_csv_row(row)
            yasnippet = render_yasnippet(snippet)
            if dry_run:
                print("Key: {0}; Mode: {1}".format(snippet.key, snippet.mode))
                print()
                print("Dash Snippet:")
                print(snippet.body)
                print()
                print("Yasnippet:")
                print(yasnippet)
                print("-" * 72)
                print("")
