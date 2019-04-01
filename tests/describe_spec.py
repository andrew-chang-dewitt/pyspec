"""tests for python test runner"""

import random
from pyspec import describe
from pyspec import comparisons as C
from pyspec.lib.comparisons import AssertionError
from pub_sub import stable

### EXPECTATIONS ###
# group tests together by creating a new Describe object using `describe()`
EXPECTATIONS = describe('set expectations')

# tests can be set up to expect a return value
EXPECTATIONS.it(
    'can expect values'
    # which can be tested for by passing an Actual Value (in this case, 1 + 1)
    # to `expect()`, then passing a comparison method & an expected value to  `to`
    # (in this case, eq & 2). You can read this line as "expect 1 + 1 to equal 2"
).expect(lambda: 1 + 1).to(C.eq, 2)

# tests can also be set up to expect a specific error class
EXPECTATIONS.it(
    'can expect exceptions'
).expect(lambda: 1/0).to(C.raise_error, ZeroDivisionError)
# note: when directly evaluating an expression that will result in an error, it
# must be wrapped in a function, otherwise the error will be raised before the
# expression is passed to the test runner

EXPECTATIONS.it(
    'can expect a specific object type',
).expect(lambda: 1).to(C.be_a, int)

EXPECTATIONS.it(
    'can expect an object to be a member of a collection'
).expect(lambda: ['other_member', 'member', 1, 2, 3]).to(C.include, 'member')

EXPECTATIONS.it(
    'can check that an iterable is empty'
).expect(lambda: []).to(C.be_empty)

EXPECTATIONS.it(
    'can check for the existance of specified keys in a dictionary'
).expect(
    lambda:
        {
            'a_key': 1,
            'another_key': 2
        }
).to(C.have_keys, 'a_key', 'another_key')

EXPECTATIONS.it(
    'can check for the existance of specified attributes on an object'
).expect(lambda: EXPECTATIONS).to(C.have_attributes, 'it', 'tests')

EXPECTATIONS.it(
    'can check for methods on an object'
).expect(lambda: EXPECTATIONS).to(C.have_methods, 'it', 'run')

### BOOLEAN OPERATIONS ###
# You can use standard boolean operators to modify a test

BOOLEANS = describe('use boolean operators')

BOOLEANS.it(
    'can negate an expectation using should_not'
).expect(lambda: True).to_not(C.eq, False)

### FAILURES ###
# you can also test that a given test will always fail as expected
FAILURES = describe('communicate failures')

# to do this, first create a failing test
FAILURES.fail_pubsub = stable.event('FAILURES')
FAILURES.fail_group = describe('failure', None, FAILURES.fail_pubsub)
FAILURES.fail_group.it('should fail').expect(lambda: 1).to(C.eq, 2)
FAILURES.fail_group.run(True)

# create a new function to defer re-raising the error
def failed():
    """this mehod will fail"""
    # & grab the error off the test result object & re-raise it
    raise FAILURES.fail_group.tests[0].result['err']

# then assign that function to a method on common state for the test group
FAILURES.failed = failed
# you can grab just the error message from the args attribute of the returned error
FAILURES.failed_msg = FAILURES.fail_group.tests[0].result['err']

# lastly, call it on the common method as the expected value with
# AssertionError as the error that should be raised by the failing test
FAILURES.it(
    'can show the expected error type'
).expect(lambda: FAILURES.failed).to(C.raise_error, AssertionError)

FAILURES.it(
    'can show the expected error message'
).expect(lambda: str(FAILURES.failed_msg)).to(C.eq, 'expected 2, but got 1')

LET = describe('let')

# # this is done by creating new attributes on the test group
LET.let('five', 5)

# you can assign simple values (or values from expressions) as above,
# or you can define a function & assign it as a new method
def five_mthd():
    """testing common methods"""
    return 5
LET.let('five_mthd', five_mthd)

LET.let('will_error', lambda: 1/0)

LET.let('rand', random.random())

def changed_let():
    LET.five = 6

    return LET.five

LET.let('changed_let', changed_let)

LET.it(
    'can use common attributes'
).expect(lambda: LET.five).to(C.eq, 5)

LET.it(
    'can use common methods'
).expect(LET.five_mthd).to(C.eq, 5)

LET.it(
    'can change the value of a let in a test'
).expect(LET.changed_let).to(C.eq, 6)

LET.it(
    'can expect changes in a let to persist between tests'
).expect(lambda: LET.five).to(C.eq, 6)

LET.it(
    'can defer errors thrown by a let'
).expect(LET.will_error).to(C.raise_error, ZeroDivisionError)

LET.it(
    'always returns the same object'
).expect(lambda: LET.rand).to(C.eq, LET.rand)

LET.it(
    'raises the correct error when an attribute on the Test Group does not exist'
).expect(lambda: LET.does_not_exist).to(C.raise_error, AttributeError)


BEFORE = describe('before')

def changed_before():
    BEFORE.five = 6

    return BEFORE.five

BEFORE.let('changed_before', changed_before)
BEFORE.before('five', 5)
BEFORE.let('will_error', lambda: 1/0)
BEFORE.let('rand', random.random())


BEFORE.it(
    'is visible to the test'
).expect(lambda: BEFORE.five).to(C.eq, 5)

BEFORE.it(
    'can change the value of a before in a test'
).expect(BEFORE.changed_before).to(C.eq, 6)

BEFORE.it(
    'resets the value of the before between each test'
    ).expect(lambda: BEFORE.five).to(C.eq, 5)

BEFORE.it(
    'can defer errors thrown by a let'
).expect(BEFORE.will_error).to(C.raise_error, ZeroDivisionError)

BEFORE.it(
    'always returns the same object'
).expect(lambda: BEFORE.rand).to(C.eq, BEFORE.rand)

BEFORE.it(
    'raises the correct error when an attribute on the Test Group does not exist'
).expect(lambda: BEFORE.does_not_exist).to(C.raise_error, AttributeError)

# # You can also have one group of tests inherit state from another
# # for example, you may have a standard test group
# OUTER = describe('outer')
# 
# # with some state containing methods & attributes
# def method(arg):
#     """testing method inheritance"""
#     return f'cool method, {arg}'
# 
# OUTER.attr = 'attribute'
# OUTER.mthd = method
# 
# # then you want to run another set of tests that may use some of those
# # same methods & attributes, but exist as a separate test group
# # to designate this new group as 'nested within' or inheriting from another,
# # just pass the first group as a second argument to `describe()`
# INNER = describe('inner', OUTER)
# 
# # this inner, nested test will be able to referr to the outer group's
# # attributes & methods as if it were its own without having to directly
# # refer to the outer test group, seen below by using `inner.attr`, although
# # an `attr` attribute was never explicitly defined on inner
# INNER.it('can see outer attributes',
#          INNER.attr).should.eq('attribute')
# 
# INNER.it('can use outer methods',
#          lambda: INNER.mthd('brah')).should.eq('cool method, brah')
# 
# # the nested test can then change the values of any inherited attributes or
# # methods & continue to use them as desired
# INNER.attr = 'inner attribute'
# 
# INNER.it('can redefine/reassign outer methods/attributes',
#          INNER.attr).should.eq('inner attribute')
# 
# # but the outer, enclosing group will still retain its orinal value for the
# # changed attribute
# OUTER.it('but outer methods/attributes will remain unchanged',
#          OUTER.attr).should.eq('attribute')
# 
# # then, you can always refer to an attribute of another test group by explicitly
# # specifying it, seen here by using `inner.attr` in a test run by `outer`
# OUTER.it('outer groups can also access the attributes of an inner group',
#          INNER.attr).should.eq('inner attribute')
