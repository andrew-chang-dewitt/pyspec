#! /usr/bin/env python
"""tests for SpecStruct metastructure"""

import pyspec

C = pyspec.Comparisons

RUNNER = pyspec.describe('create & manage metastructures')

RUNNER.struct = pyspec.lib.runner.Runner(None)

RUNNER.it(
    'can create a new structure'
).expect(lambda: RUNNER.struct).to(C.be_a, pyspec.lib.runner.Runner)

RUNNER.it(
    'initializes with no test groups'
).expect(lambda: RUNNER.struct.test_groups).to(C.be_empty)

RUNNER.test_group = pyspec.lib.describe.Describe('this is a test group')

RUNNER.it(
    'can add new test groups to the metastructure'
).expect(lambda: RUNNER.struct.add_group(RUNNER.test_group)).to(C.include, RUNNER.test_group)

RUNNER.it(
    'can remove specified test groups'
).expect(lambda: RUNNER.struct.remove_group(RUNNER.test_group)).to_not(C.include, RUNNER.test_group)

if __name__ == '__main__':
    RUNNER.run()
