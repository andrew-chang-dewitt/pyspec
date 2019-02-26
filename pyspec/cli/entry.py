#!/usr/bin/env python
"""
entry point for the pyspec program
"""

import click
from pyspec.cli import run_tests
from pyspec.api import describe

@click.command()
@click.argument('method')
@click.argument('module_path')
@click.option('-d', '--directory', is_flag=True,
              help='tells pyspec to look for all modules in an entire directory')
def main(method, module_path, directory):
    def all_tests(path):
        run_tests.all_tests(path, directory)

    def one_file(path):
        run_tests.one_file(path)

    options = {
        'all': all_tests,
        # 'one': one_file
    }

    options[method](module_path)
