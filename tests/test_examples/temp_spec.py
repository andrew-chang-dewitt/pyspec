#! /usr/bin/env python

import  pyspec
from pub_sub import stable

C = pyspec.Comparisons

PUB_SUB = stable.event('temp spec')

TEST = pyspec.describe('this is a test', PUB_SUB)

TEST.it('can pass').expect(lambda: 1).to(C.eq, 1)
TEST.it('can fail').expect(lambda: 1).to(C.eq, 2)

if __name__ == '__main__':
    TEST.run()
