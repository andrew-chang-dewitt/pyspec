"""
Testing the cli functions
"""

from pyspec import describe, cli
from tests.test_examples.temp_pub_sub import temp_pub_sub

COMMANDS = describe('the cli has commands for running *_spec files')

COMMANDS.it(
    'can run all tests in a given directory',
    lambda: cli.run_tests.all_tests('tests/test_examples', temp_pub_sub, True)
).should.eq(True)

COMMANDS.it(
    'can run just the tests for one file',
    lambda: cli.run_tests.one_file('tests/test_examples/temp_spec', temp_pub_sub, True)
).should.eq(True)
