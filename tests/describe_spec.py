"""tests for python test runner"""

from pyspec import describe

### EXPECTATIONS ###
# group tests together by creating a new Describe object using `describe()`
EXPECTATIONS = describe('set expectations')

# tests can be set up to expect a return value
EXPECTATIONS.it('can expect values',
                # which can be tested for by passing a function as the second argument to
                # `it()`; functions are required to deferr the execution of any passed expression
                # read the following line as one plus one should equal two
                1 + 1).should.eq(2)

# tests can also be set up to expect a specific error class
EXPECTATIONS.it('can expect exceptions',
                lambda: 1/0).should.raise_error(ZeroDivisionError)
# note: when directly evaluating an expression that will result in an error, it
# must be wrapped in a function, otherwise the error will be raised before the
# expression is passed to the test runner

EXPECTATIONS.it('can expect a specific object type',
                1).should.be_a(int)

EXPECTATIONS.it('can expect an object to be a member of a collection',
                ['other_member', 'member', 1, 2, 3]).should.include('member')

EXPECTATIONS.it(
    'can check for the existance of specified keys in a dictionary',
    {
        'a_key': 1,
        'another_key': 2
    }
).should.have_keys('a_key', 'another_key')

### BOOLEAN OPERATIONS ###
# You can use standard boolean operators to modify a test

BOOLEANS = describe('use boolean operators')

BOOLEANS.it(
    'can negate an expectation using should_not',
    True
).should_not.eq(False)

### COMMON ###
# You can also define common variables for a group of tests
COMMON = describe('set common state')

# this is done by creating new attributes on the test group
COMMON.five = 5
# you can assign simple values (or values from expressions) as above,
# or you can define a function & assign it as a new method
def five_mthd():
    """testing common methods"""
    return 5
COMMON.five_mthd = five_mthd

COMMON.it('can use common attributes',
          COMMON.five).should.eq(5)

COMMON.it('can use common methods',
          COMMON.five_mthd).should.eq(5)

### FAILURES ###
# you can also test that a given test will always fail as expected
FAILURES = describe('communicate failures')

# to do this, first create a failing test
FAILURES.fail = describe('failure').it('should fail', 1).should.eq(2)

# create a new function to deferr re-raising the error
def failed():
    """this mehod will fail"""
    # & grab the error off the test result object & re-raise it
    raise FAILURES.fail.err

# then assign that function to a method on common state for the test group
FAILURES.failed = failed
# you can grab just the error message from the args attribute of the returned error
FAILURES.failed_msg = FAILURES.fail.err.args[0]

# lastly, call it on the common method as the expected value with
# AssertionError as the error that should be raised by the failing test
FAILURES.it('can show the expected error type',
            FAILURES.failed).should.raise_error(AssertionError)

FAILURES.it('can show the expected error message',
            FAILURES.failed_msg).should.eq('expected 2, but got 1')

# You can also have one group of tests inherit state from another
# for example, you may have a standard test group
OUTER = describe('outer')

# with some state containing methods & attributes
def method(arg):
    """testing method inheritance"""
    return f'cool method, {arg}'

OUTER.attr = 'attribute'
OUTER.mthd = method

# then you want to run another set of tests that may use some of those
# same methods & attributes, but exist as a separate test group
# to designate this new group as 'nested within' or inheriting from another,
# just pass the first group as a second argument to `describe()`
INNER = describe('inner', OUTER)

# this inner, nested test will be able to referr to the outer group's
# attributes & methods as if it were its own without having to directly
# refer to the outer test group, seen below by using `inner.attr`, although
# an `attr` attribute was never explicitly defined on inner
INNER.it('can see outer attributes',
         INNER.attr).should.eq('attribute')

INNER.it('can use outer methods',
         lambda: INNER.mthd('brah')).should.eq('cool method, brah')

# the nested test can then change the values of any inherited attributes or
# methods & continue to use them as desired
INNER.attr = 'inner attribute'

INNER.it('can redefine/reassign outer methods/attributes',
         INNER.attr).should.eq('inner attribute')

# but the outer, enclosing group will still retain its orinal value for the
# changed attribute
OUTER.it('but outer methods/attributes will remain unchanged',
         OUTER.attr).should.eq('attribute')

# then, you can always refer to an attribute of another test group by explicitly
# specifying it, seen here by using `inner.attr` in a test run by `outer`
OUTER.it('outer groups can also access the attributes of an inner group',
         INNER.attr).should.eq('inner attribute')
