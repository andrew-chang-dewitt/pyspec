#! /usr/bin/env python
"""
Testing the cli functions
"""

import pyspec
from pyspec.lib.runner import Runner
from pub_sub import stable

C = pyspec.Comparisons

COMMANDS = pyspec.describe('the cli has commands for running *_spec files')

COMMANDS.let('cli_run', pyspec.cli.run_tests.RunTests(stable.event('temp spec')))

COMMANDS.it(
    'can run all tests in a given directory'
).expect(lambda: COMMANDS.cli_run.all_tests('tests/test_examples', False, True)).to(C.be_a, Runner)

COMMANDS.it(
    'can run just the tests for one file'
).expect(
    lambda: COMMANDS.cli_run.one_file('tests/test_examples/temp_spec', False, True)
).to(C.be_a, Runner)

COMMANDS.it(
    'can request a list of all test groups in a test directory'
).expect(
    lambda: COMMANDS.cli_run.explore('tests/test_examples')[0].description
).to(C.eq, 'this is a test')

if __name__ == '__main__':
    COMMANDS.run()
