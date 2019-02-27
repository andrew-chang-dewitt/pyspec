#!/usr/bin/env python
"""
entry point for the pyspec program
"""

import click
from pyspec.cli import run_tests
from pyspec.api import describe

@click.group()
def main():
    pass

@main.command()
@click.argument('path')
def all(path):
    run_tests.all_tests(path)

@main.command()
@click.argument('module')
def one(module):
    run_tests.one_file(module)
