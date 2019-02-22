from api import describe

example = describe('example')

example.it('a new test, should fail', 1).should.eq(2)
