from runner import describe

### EXPECTATIONS ###
# group tests together by creating a new Describe object using `describe()`
expectations = describe('set expectations')

# tests can be set up to expect a return value
expectations.it('can expect values',
    # which can be tested for by passing a function as the second argument to 
    # `it()`; functions are required to deferr the execution of any passed expression
    # read the following line as one plus one should equal two
    1 + 1).should.eq(2)

# tests can also be set up to expect a specific error class
expectations.it('can expect exceptions',
    lambda: 1/0).should.raise_error(ZeroDivisionError)
# note: when directly evaluating an expression that will result in an error, it 
# must be wrapped in a function, otherwise the error will be raised before the 
# expression is passed to the test runner

# A group of tests is ran by calling it's `run()` method
expectations.run()

### COMMON###
# You can also define common variables for a group of tests
common = describe('set common state')

# this is done by creating new attributes on the test group
common.five = 5
# you can assign simple values (or values from expressions) as above,
# or you can define a function & assign it as a new method
def five_mthd(): return 5
common.five_mthd = five_mthd

common.it('can use common attributes',
    common.five).should.eq(5)

common.it('can use common methods',
    common.five_mthd).should.eq(5)

common.run()

### FAILURES ###
# you can also test that a given test will always fail as expected
failures = describe('communicate failures')

# to do this, first create a failing test
failures.fail = describe('failure').it('should fail', 1).should.eq(2)

# create a new function to deferr re-raising the error
def failed():
    # & grab the error off the test result object & re-raise it
    raise failures.fail.err

# then assign that function to a method on common state for the test group
failures.failed = failed
# you can grab just the error message from the args attribute of the returned error
failures.failed_msg = failures.fail.err.args[0]

# lastly, call it on the common method as the expected value with
# AssertionError as the error that should be raised by the failing test
failures.it('can show the expected error type',
    failures.failed).should.raise_error(AssertionError)

failures.it('can show the expected error message',
    failures.failed_msg).should.eq('expected 2, but got 1')

failures.run()

# You can also have one group of tests inherit state from another
# for example, you may have a standard test group
outer = describe('outer')

# with some state containing methods & attributes
def method(arg):
    return f'cool method, {arg}'

outer.attr = 'attribute'
outer.mthd = method

# then you want to run another set of tests that may use some of those
# same methods & attributes, but exist as a separate test group
# to designate this new group as 'nested within' or inheriting from another, 
# just pass the first group as a second argument to `describe()`
inner = describe('inner', outer)

# this inner, nested test will be able to referr to the outer group's 
# attributes & methods as if it were its own without having to directly
# refer to the outer test group, seen below by using `inner.attr`, although
# an `attr` attribute was never explicitly defined on inner
inner.it('can see outer attributes',
    inner.attr).should.eq('attribute')

inner.it('can use outer methods',
    lambda: inner.mthd('brah')).should.eq('cool method, brah')

# the nested test can then change the values of any inherited attributes or
# methods & continue to use them as desired
inner.attr = 'inner attribute'

inner.it('can redefine/reassign outer methods/attributes',
    inner.attr).should.eq('inner attribute')

# but the outer, enclosing group will still retain its orinal value for the 
# changed attribute
outer.it('but outer methods/attributes will remain unchanged',
    outer.attr).should.eq('attribute')

# then, you can always refer to an attribute of another test group by explicitly
# specifying it, seen here by using `inner.attr` in a test run by `outer`
outer.it('outer groups can also access the attributes of an inner group',
    inner.attr).should.eq('inner attribute')

# lastly, inner test groups can not be be explicitly called, as they will
# instead be called by their enclosing test group at run time
outer.run()
