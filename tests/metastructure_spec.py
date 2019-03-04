"""tests for SpecStruct metastructure"""

import pyspec

describe = pyspec.describe
spec_struct = pyspec.spec_struct

RUNNER = spec_struct()

meta = describe('create & manage metastructures', RUNNER)

meta.struct = spec_struct()

meta.it(
    'can create a new structure',
    meta.struct
).should.be_a(pyspec.lib.metastructure.SpecStruct)

meta.it(
    'initializes with no test groups',
    meta.struct.test_groups
).should.be_empty()

meta.test_group = describe('this is a test group')

meta.it(
    'can add new test groups to the metastructure',
    meta.struct.add_group(meta.test_group)
).should.include(meta.test_group)

meta.it(
    'can remove specified test groups',
    meta.struct.remove_group(meta.test_group)
).should_not.include(meta.test_group)
