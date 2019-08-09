#!/usr/bin/env python
"""
{{ cookiecutter.description }}
"""
from __future__ import absolute_import, division, print_function

import os
import re
import sys

import click
from plumbum import FG, local

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

__version__ = "0.1"


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.version_option(version=__version__)
@click.pass_context
def main(ctxt):
    """
    {{ cookiecutter.description }}
    """
    if ctxt.invoked_subcommand is None:
        run_invocation()


@main.command()
def invoke():
    """
    Primary command entry point
    """
    run_invocation()


def run_invocation():
    """
    Handle invocation
    """
    listdir = local["ls"]
    _ = listdir[get_basedir()] & FG
    path = os.path.join(get_basedir(), "data.txt")
    update = os.path.join(get_basedir(), "update.txt")
    if adjust_file(path, "# {{{ update", "# }}} update", update):
        print("Modified")


def get_basedir():
    """
    Locate the current directory of this file
    """
    return os.path.dirname(os.path.abspath(sys.modules[__name__].__file__))


def re_index(lines, regex, start=0):
    """
    Locate the index of the line that matches the regex from the
    provided starting point
    """
    for index, line in enumerate(lines[start:], start):
        if re.match(regex, line):
            return index
    raise ValueError("Line starting with %r not found." % (regex,))


def adjust(lines, start_line, end_line, new_content_lines):
    """
    Apply the desired configuration to a config file
    """
    try:
        start = re_index(lines, "^%s$" % (re.escape(start_line),))
        if end_line is not None:
            end = re_index(lines, "^%s$" % (re.escape(end_line),), start=start + 1)
        else:
            end = start + 1
    except ValueError:
        return (
            lines
            + [start_line]
            + new_content_lines
            + ([end_line] if end_line is not None else [])
        )
    else:
        return lines[: start + 1] + new_content_lines + lines[end:]


def read_lines(path):
    """
    Obtain the lines from a file.
    """
    with open(path) as fobj:
        return [line.rstrip("\r\n") for line in fobj]


def write_lines(path, lines):
    """
    Save the lines from a file.
    """
    with open(path, "w") as fobj:
        for line in lines:
            print(line, file=fobj)


def adjust_file(filepath, start_line, end_line, updatepath):
    """
    Look for a special line marker and update the lines if different otherwise
    append to the end
    """
    srclines = read_lines(filepath)
    updatelines = read_lines(updatepath)
    newlines = adjust(srclines, start_line, end_line, updatelines)
    if newlines == srclines:
        return False
    write_lines(filepath, newlines)
    return True


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
# vim: set ft=python:
