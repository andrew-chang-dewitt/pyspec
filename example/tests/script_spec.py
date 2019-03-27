from pyspec import describe, spec_struct
from example import script

RUNNER = spec_struct()

TEST = describe('example test on script.test()', RUNNER)

TEST.it('returns 1',
        lambda: script.test()).should.eq(1)

TEST.it('errors when given an argument',
        lambda: script.test('unexpected arg')).should.raise_error(TypeError)
