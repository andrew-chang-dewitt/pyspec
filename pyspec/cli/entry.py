#!/usr/bin/env python
"""
entry point for the pyspec program
"""

import click
from pyspec.cli.run_tests import RunTests
from pyspec.cli.click_cust import ErrorHandlingGroup

run_tests = RunTests()

@click.group(cls=ErrorHandlingGroup)
def entry_point():
    """
    CLI companion tool for the Pyspec testing library.
    """

@entry_point.command('all')
@click.argument('path')
def all_tests(path):
    """
    Runs all tests in a given directory. PATH must be relative to the current $PWD.
    This command will only find files in the given directory that end in `_spec.py`.
    """
    return run_tests.all_tests(path)

@entry_point.command()
@click.argument('module')
def one(module):
    """
    Runs the specific test file given as a module name. MODULE must be just the file
    name, without any file type extensions.
    """
    return run_tests.one_file(module)

@entry_point.command()
@click.argument('path')
def list(path):
    """
    Lists all test groups available in in a given directory. PATH must be relative
    to the current $PWD. This command will only find files in the given directory
    that end in `_spec.py`.
    """
    res = run_tests.explore(path)
    num = 0

    click.echo('')
    for group in res:
        click.echo('%(num)s. %(desc)s' % { 'num': num, 'desc': group.description })
        num += 1

    req = input('\nWhich test group would you like to run? ')
    req_int = int(req)
    print('')
    results_str = res[req_int].run()

    for line in results_str:
        click.echo(line)

        return True

    return False
