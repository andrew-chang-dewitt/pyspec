import  pyspec
from pub_sub import stable

C = pyspec.Comparisons

PUB_SUB = stable.event('temp spec')

TEST = pyspec.describe('this is a test', None, PUB_SUB)

TEST.it('can pass').expect(1).to(C.eq, 1)
TEST.it('can fail').expect(1).to(C.eq, 2)
