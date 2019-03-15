"""
Testing the cli functions
"""

import os
import shutil
from pyspec import describe, runner, cli

RUNNER = runner()

COMMANDS = describe('the cli has commands for running *_spec files', RUNNER)

PATH = os.getcwd()
TEMP = PATH + '/temp'
os.mkdir(TEMP)
with open(TEMP + '/temp_spec.py', 'w') as temp_spec:
    temp_spec.write('from pyspec import describe, runner')
    temp_spec.write('RUNNER = runner()')
    temp_spec.write('TEST = describe("this is a test")')
    temp_spec.write('TEST.it("can pass", 1).should.eq(1)')
    temp_spec.write('TEST.it("can fail", 1).should.eq(2)')

for item in os.scandir(TEMP):
    print(item)

COMMANDS.it(
    'can run all tests in a given directory',
    lambda: cli.run_tests.all_tests('tests/temp')
).should.eq(True)

COMMANDS.it(
    'can run just the tests for one file',
    lambda: cli.run_tests.one_file('tests/temp/temp_spec')
).should.eq(True)

# this is being called before line 33 is executed, somehow this needs to be fixed
shutil.rmtree(TEMP)
