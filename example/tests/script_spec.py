from api import describe
import os
print(os.getcwd())
import sys
print(sys.path)

from example import script

test = describe('example test on script.test()')

test.it('returns 1',
        lambda: script.test()).should.eq(1)

test.it('errors when given an argument',
        lambda: script.test('unexpected arg')).should.raise_error(TypeError)
