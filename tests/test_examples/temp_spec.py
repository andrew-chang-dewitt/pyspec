from pyspec import describe
from pub_sub import stable

PUB_SUB = stable.event('CLI test')

TEST = describe('this is a test', None, PUB_SUB)

TEST.it('can pass', 1).should.eq(1)
TEST.it('can fail', 1).should.eq(2)
