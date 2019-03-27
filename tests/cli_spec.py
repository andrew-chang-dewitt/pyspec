"""
Testing the cli functions
"""

from pyspec import describe, cli
from pyspec.lib.runner import Runner
from pub_sub import stable

COMMANDS = describe('the cli has commands for running *_spec files')

COMMANDS.cli_run = cli.run_tests.RunTests(stable.event('temp spec'))

COMMANDS.it(
    'can run all tests in a given directory',
    lambda: COMMANDS.cli_run.all_tests('tests/test_examples', True)).should.be_a(Runner)

COMMANDS.it(
    'can run just the tests for one file',
    COMMANDS.cli_run.one_file('tests/test_examples/temp_spec', True)
).should.be_a(Runner)

COMMANDS.it(
    'can request a list of all test groups in a test directory',
    lambda: COMMANDS.cli_run.explore('tests/test_examples', True)[0].description
).should.eq('this is a test')
