#! /usr/bin/env python
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
FAILURES.fail_group = describe('failure', FAILURES.fail_pubsub)
FAILURES.fail_group.it('should fail').expect(lambda: 1).to(C.eq, 2)
FAILURES.fail_group.it(
    'should fail on error type'
).expect(lambda: 1/0).to(C.raise_error, TypeError)
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
FAILURES.raise_error_failed_msg = FAILURES.fail_group.tests[1].result['err']

# lastly, call it on the common method as the expected value with
# AssertionError as the error that should be raised by the failing test
FAILURES.it(
    'can show the expected error type'
).expect(lambda: FAILURES.failed).to(C.raise_error, AssertionError)

FAILURES.it(
    'can show the expected error message'
).expect(lambda: str(FAILURES.failed_msg)).to(C.eq, 'expected 2, but got 1')

FAILURES.it(
    'can show the expected error message when expecting an exception'
).expect(
    lambda: str(FAILURES.raise_error_failed_msg)
).to(
    C.eq,
    "expected <class 'TypeError'>, but got <class 'ZeroDivisionError'>"
)

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

RAND = random.random()

def will_error():
    return 1/0

BEFORE.let('changed_before', changed_before)
BEFORE.before('five', 5)
BEFORE.before('will_error', will_error)
BEFORE.before('rand', RAND)

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
    'can defer errors thrown by a before'
).expect(lambda: BEFORE.will_error()).to(C.raise_error, ZeroDivisionError)

BEFORE.it(
    'always returns the same object'
).expect(lambda: BEFORE.rand).to(C.eq, RAND)

BEFORE.it(
    'raises the correct error when an attribute on the Test Group does not exist'
).expect(lambda: BEFORE.does_not_exist).to(C.raise_error, AttributeError)


OUTER = describe('outer')

OUTER.let('five', 5)
OUTER.before('six', 6)

INNER = OUTER.describe('inner')

def changed():
    INNER.let('five', 6)

    return INNER.five

INNER.let('changed', changed)

INNER.it('can view befores on the outer group').expect(lambda: INNER.six).to(C.eq, 6)
INNER.it('can view lets on the outer group').expect(lambda: INNER.five).to(C.eq, 5)
INNER.it('can change the value of lets defined by outer').expect(INNER.changed).to(C.eq, 6)

OUTER.it('but the value on outer will remain the same').expect(lambda: OUTER.five).to(C.eq, 5)


if __name__ == '__main__':
    EXPECTATIONS.run()
    BOOLEANS.run()
    FAILURES.run()
    LET.run()
    BEFORE.run()
    OUTER.run()
