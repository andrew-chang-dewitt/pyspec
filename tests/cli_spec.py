"""
Testing the cli functions
"""

from pyspec import describe, cli
from pyspec.lib.runner import Runner
from pub_sub import stable

COMMANDS = describe('the cli has commands for running *_spec files')

def test_all():
    cli_run = cli.run_tests.RunTests(stable.event('CLI test'))

    return cli_run.all_tests('tests/test_examples', True)

COMMANDS.it(
    'can run all tests in a given directory',
    test_all
).should.be_a(Runner)

def test_one():
    cli_run = cli.run_tests.RunTests(stable.event('CLI test no. 2'))

    return cli_run.one_file('tests/test_examples/temp_spec', True)

COMMANDS.it(
    'can run just the tests for one file',
    test_one
).should.be_a(Runner)
