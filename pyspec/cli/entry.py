#!/usr/bin/env python
"""
entry point for the pyspec program
"""

import click
from pyspec.cli import run_tests
from pyspec.api import describe

@click.group()
def main():
    """
    CLI companion tool for the Pyspec testing library. 
    """
    pass

@main.command('all')
@click.argument('path')
def all_tests(path):
    """
    Runs all tests in a given directory. PATH must be relative to the current $PWD.
    This command will only find files in the given directory that end in `_spec.py`.
    """
    run_tests.all_tests(path)

@main.command()
@click.argument('module')
def one(module):
    """
    Runs the specific test file given as a module name. MODULE must be just the file
    name, without any file type extensions.
    """
    run_tests.one_file(module)
