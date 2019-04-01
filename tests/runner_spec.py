"""tests for SpecStruct metastructure"""

import pyspec

META = pyspec.describe('create & manage metastructures')

META.struct = pyspec.lib.runner.Runner(None)

META.it(
    'can create a new structure',
    META.struct
).should.be_a(pyspec.lib.runner.Runner)

META.it(
    'initializes with no test groups',
    META.struct.test_groups
).should.be_empty()

META.test_group = pyspec.lib.describe.Describe('this is a test group')

META.it(
    'can add new test groups to the metastructure',
    META.struct.add_group(META.test_group)
).should.include(META.test_group)

META.it(
    'can remove specified test groups',
    META.struct.remove_group(META.test_group)
).should_not.include(META.test_group)
