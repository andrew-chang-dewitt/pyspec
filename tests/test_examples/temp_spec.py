from pyspec import describe
from tests.test_examples.temp_pub_sub import temp_pub_sub

TEST = describe('this is a test', None, temp_pub_sub)

TEST.it('can pass', 1).should.eq(1)
TEST.it('can fail', 1).should.eq(2)
