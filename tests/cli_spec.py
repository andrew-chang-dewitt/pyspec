"""
Testing the cli functions
"""

from pyspec import describe, cli
from pub_sub import stable

PUB_SUB = stable.event('CLI test')

COMMANDS = describe('the cli has commands for running *_spec files')

COMMANDS.it(
    'can run all tests in a given directory',
    lambda: cli.run_tests.all_tests('tests/test_examples', PUB_SUB, True)
).should.eq(True)

COMMANDS.it(
    'can run just the tests for one file',
    lambda: cli.run_tests.one_file('tests/test_examples/temp_spec', PUB_SUB, True)
).should.eq(True)
