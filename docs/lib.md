PySpec Library API
==================

Contents
--------

- Top level functions
  - [pyspec.describe](#pyspecdescribe)
  - [pyspec.Comparisons](#pyspecComparisons)
  - [Describe class](#describe-class)
  - [Attributes](#attributes)
  - [Methods](#methods)
    - [Describe.let](#describelet)
    - [Describe.before](#describebefore)
    - [Describe.it](#describeit)
    - [Describe.describe](#describedescribe)
    - [Describe.run](#describerun)
- [Test class](#test-class)
  - [Attributes](#attributes-1)
  - [Methods](#methods-1)
    - [Test.expect](#testexpect)
    - [Test.to](#testto)
    - [Test.to\_not](#testto_not)
    - [Test.run](#testrun)
- [Comparisons class](#comparisons-class)
  - [Methods](#methods-2)
    - [Comparisons.eq](#comparisonseq)
    - [Comparisons.raise\_error](#comparisonsraise_error)
    - [Comparisons.be\_a](#comparisonsbe_a)
    - [Comparisons.include](#comparisonsinclude)
    - [Comparisons.be\_empty](#comparisonsbe_empty)
    - [Comparisons.have\_keys](#comparisonshave_keys)
    - [Comparisons.have\_attributes](#comparisonshave_attributes)
    - [Comparisons.have\_methods](#comparisonshave_methods)
  - [Exceptions](#exceptions)
    - [Comparisons.AssertionError](#comparisonsassertionerror)
    - [Comparisons.NoComparison](#comparisonsnocomparison)

There are two top level objects exposed by the PySpec Library:

#### pyspec.describe:
(_description_, *alt_pub_sub=None*)

Initializes & returns a **Describe()** object with the given `description`. If given,
the returned Describe() object will be initialized with an alternate pub_sub.Event object (an 
instance of [PyPubSub's Event class](https://github.com/andrew-dewitt/py-pub-sub).

_Accepts_:

- `description` (STRING) a string describing the test group
- [`alt_pub_sub`] \(pub\_sub.Event instance) an Event module to publish & subscribe to
  used to pass information to PySpec's CLI tool

_Returns_: An instance of Describe

#### pyspec.Comparisons:

A class of static methods used to compare an _actual result_ to an _expected value_.

_Accepts_: pyspec.Comparisons takes no arguments

_Returns_: 

A class of comparisons methods that all accept an _actual result_ & a list of one
or more _expected values_.


Describe class
--------------

The PySpec Library is organized with one core Class, **[Describe()](#describe-class)**. 
This class references one other classe that is used to create tests 
(**[Test()](#test-class)**). Describe objects can be nested indefinitely 
to inherit scope from an outer Describe object & organize testing groups as subsets of 
related test groups. 


### Attributes:

- `description` (STRING)

  a string describing the test group

- `tests` (LIST)			

  an empty list where each test function will be stored

- `outer` (Describe instance), optional

  another test group to inherit common state from, optional

- `inners` (LIST)			

  an empty list where any nested test groups will be stored
  
- `results` (LIST)

  an empty list where test results are stored by `run`

- `base`, `tab`, & `tabplus` (STRING)		
  
  strings used to increment tabs for results printing


### Methods:

The Describe class has four methods used to set up variables & state for tests, 
create new tests, & run all tests included in the `tests` attribute list.

#### Describe.let
(_name_, _value_)

Sets values on the test group to be parsed later when the test is ran. If an error
is thrown in the definition of a `let`, it will be raised in any test that depends
upon it the let. Lets are evaluated once before any tests in the group are ran & 
are not re-evaluated again.

_Accepts_:

- `name` (STRING)

  the name that will be given to the `let`. 

- `value` (EXPRESSION)

  an expression that will be retrived by the `let` using `DESCRIBE_INSTANCE.[value]`

`Describe.let()` has no returns.

#### Describe.before
(_name_, _value_)

Sets values on the test group to be parsed later when the test is ran. If an error
is thrown in the definition of a `before`, it will be raised in any test that depends
upon it the before. Befores are evaluated right before each test is ran & are re-evaluated
for each test.

_Accepts_:

- `name` (STRING)

  the name that will be given to the `before`. 

- `value` (EXPRESSION)

  an expression that will be retrived by the `before` using `DESCRIBE_INSTANCE.[value]`

`Describe.before()` has no returns.

#### Describe.it:
(_description_)

A method used to create a new test in the group, adds an instance of Test to
the self.tests list and returns it.

_Accepts_:

- `description` (STRING)

  a short description to be printed when the test is ran

_Returns_: An instance of Test()

_Example usage_:

```python
TEST_GROUP = describe('some description')

TEST_GROUP.it('can add 1') # more methods follow...
```

#### Describe.describe
(_description_)

Similar to the top-level [pyspec.describe](#pyspecdescribe), but for creating a new
test group that will be nested within the existing test group that this method is
called on. Defining a test group with this method will automatically add the new group
to this instance's `inners` list attribute & initialize the new group with this instance
as the new group's `outer` attribute.

_Accepts_:

- `description` (STRING) a string describing the test group

_Returns_: An instance of Describe

_Example usage_:

```python
OUTER = describe('outer group')

INNER = OUTER.describe('inner group')
```

#### Describe.run:
(*muted=False*, *verbose=False*)

A method used to run the test group & any inners, accessed via the 
Describe.run attribute (which will only exist for instances with no
Describe.outer attribute). Prints results to stdout by default; also
publishes results to Event module for any subscriber listening on 
the 'test group results' topic.

_Accepts_:

- `muted` (BOOLEAN)

  defaults to FALSE, will not print results to stdout if TRUE

- `verbose` (BOOLEAN)

  defaults to FALSE, supresses printing results for indivual passing tests

_Returns_:

An a list containing strings to be used to print lines of human-readable
results for a user.

_Example usage_:

This method can be called directly in a spec file to make it runnable directly
by Python.

```python
TEST_GROUP = describe('some description')

# ... some tests here

TEST_GROUP.run() # prints results to stdout
```

If you want to be able to run the file directly, or by using the CLI tool, 
guard your calls to `Describe.run()` as follows:

```python
if __name__ = '__main__':
    TEST_GROUP.run()
```


Test class
----------

An instance of the Test class is created with each call to 
**[Describe.it()](describeitdescription-code)**. This class is used to store a 
test's description, actual code/value, expected value, comparison method, & 
comparison results [attributes](#test-attributes).

### Attributes:

- `description` (STRING)

  a description to print when running the test, should be descriptive, readable, & concise

- `comparison` (pyspec.Comparisons)

  the method to be used for comparing the actual result to the expected value of the Test

- `actual` (FUNCTION)

  a function to be executed when evaluating the test, returns the 'actual' value

- `expected` (EXPRESSION)

  an expression that evaluates to the expected value that will be compared to `actual`

- `error` (EXCEPTION)

  used to store any error that is raised before a test is ran; this error will later be
  re-raised at test run time

- `results` (DICT)

  a dictionary for storing the results when a test is run

### Methods:

#### Test.expect
(_actual_)

A method that is used to tell the test what code to run or expression to evaluate. The value 
given to `actual` is what will be evaluated & compared to the _expected_ value passed later in 
[Expect.to](#expectto) or [Expect.to\_not](#expectto_not).

_Accepts_:

- `actual` (FUNCTION)

  a function to be evaluated at test runtime; this is the code that you are testing &
  the results will compared to their expected value; `Test.expect` will throw an Exception if 
  this argument is not callable

_Returns_:

The Test object expect was called on.

_Example usage_:

Assuming you have the following function:

```python
def hello():
    return 'Hello world!'
```

You can test it by passing it as the _actual value_ to `expect`:

```python
TEST = describe('hello')

TEST.it('can expect hello').expect(hello) # more methods to come ...
```

If your function requires you to pass it some arguments, or you merely 
need to pass an expression as your _actual value_, it still must be callable
so that PySpec can deferr evaluation of it, thus allowing exceptions to be 
caught by PySpec instead of being thrown & interupting the test. To get around this,
you can simply wrap your code in a `lambda`:

```python
def add(x, y):
    return x + y

TEST.it('can evaluate expressions').expect(lambda: 1 + 1) # more methods to come ...
TEST.it('can pass arguments').expect(lambda: add(1,1))    # ...
```

#### Test.to
(_comparison method_, _*expected_)

A method used to declare an expected result for the test & pass a comparison method that will
be used to evaluate the test. Comparison methods come from the [Comparisons class](#comparisons)
which must be imported into the \_spec file along with [PySpec.describe](#pyspecdescribe).

_Accepts_:

- `comparison_method` (bound method on Comparisons)

  a method from [Comparisons](#comparisons) that is used to evaluate the test

- `*expected` (EXPRESSIONS)

  an expression (or multiple expressions, separated by commas) that defines an _expected value_
  that the function passed as the _actual value_ must return

_Returns_:

The Test object expect was called on.

_Example usage_:

Continuing from the examples above, you add `.to()` at the end of each `Test.it` line
to complete the test expression.

```python
def hello():
    return 'Hello world!'

def add(x, y):
    return x + y

TEST.it('can expect hello').expect(hello).to(Comparisons.eq, 'Hello world!')
TEST.it('can evaluate expressions').expect(lambda: 1 + 1).to(Comparisons.eq, 2)
TEST.it('can pass arguments').expect(lambda: add(1,1)).to(Comparisons.eq, 2)
```

#### Test.to\_not
(_comparison method_, _*expected_)

The same as [Test.to](#testto), but it negates the test result. This means that a test
that would have succeeded in `Test.to` will fail in `Test.to_not` & vice versa.

_Accepts_:

- `comparison_method` (bound method on Comparisons)

  a method from [Comparisons](#comparisons) that is used to evaluate the test

- `*expected` (EXPRESSIONS)

  an expression (or multiple expressions, separated by commas) that defines an _expected value_
  that the function passed as the _actual value_ must _not_ return

_Returns_:

The Test object expect was called on.

_Example usage_:

```python
Test.it('will fail').expect(lambda: 1).to_not(Comparisons.eq, 1) # => this test will fail
Test.it('will fail').expect(lambda: 1).to_not(Comparisons.eq, 2) # => but this test will pass
```


Comparisons class
------------

The following methods are all functions that can be used in a test
to compare an actual result (stored in the test at the `code`
attribute) against the expected attribute (passed to each method).

Typical usage will be to pass the method to a [Expect.to](#expectto) or
[Expect.to\_not](#expectto_not) call as the first argument, with the
expected value (that will be passed to this Comparison method) as the
second argument. This structure allows the execution of the comparison
to be deferred until the Test's `run` method is called.

A short name is chosen as the method will be referenced very often by the
end user of this test runner; the pylint warning about name snake case
has been disabled.

### Methods:

Each of the following methods is used to make an assertation about the ACTUAL result the code 
passed to `Test` will evaluate to versus the EXPECTED value given to the method. All of these 
methods will return the original Test object that the method was called on.

These methods are not intended to be called directly, but rather, to be passed to a Test in
a `to` or `to_not` method call. All methods are used in the same manner:

```python
TEST = pyspec.describe('test group')

TEST.it('can add').expect(lambda: add(1,2)).to(Comparisons.eq, 3)
```

It may be easier to assign the Comparisons class a shorter name for easier test writing:

```python
C = pyspec.Comparisons

Test.it('can add').expect(lambda: 1 + 2).to(C.eq, 3)
```

In this usage, the Comparison method desired is always passed as the first argument to
`Expect.to` to `Expect.to_not` so that it can be executed later when the Test is ran
using `Describe.run`.

#### Comparisons.eq:
(_caller_, _actual_, _expected_)

_Success_: This method results in a success if `actual` is equal to `expected`.

_Failure_: This method fails in any scenario where Python does not consider the result of
evaluating `actual` to be equal to `expected`.

#### Comparisons.raise\_error:
(_caller_, _actual_, _expected_)

_Success_: This method results in a success if evaluating `actual` raises an error of 
the exact type supplied in `expected`. It _will not_ succeed if the `actual` error is _an instance_
(or child of) the `expected` error type.

_Failure_: This method fails in any scenario where Python does not raise an error when 
evaluating `actual`, or when the error that is raised is not of the type supplied by `expected`.

#### Comparisons.be\_a:
(_caller_, _actual_, _expected_)

_Success_: This method results in a success if `actual` is an instance of the `expected` class.
It _will_ succeed if the result of `actual` is of a type that inherits from `expected`.

_Failure_: This method fails in any scenario where `actual` is not an instance of `expected`.

#### Comparisons.include:
(_caller_, _actual_, _expected_)

_Success_: This method results in a success if `actual` is an iterable that includes _all_ of the 
values given by the `expected` list.

_Failure_: This method fails in any scenario where one or more of the members of `expected` are not 
included in the iterable given by evaluating `actual`. It will also fail if `actual` does not 
result in an iterable.

#### Comparisons.be\_empty:
(_caller_, _actual_, _expected_

_Success_: This method results in a success if `actual` is an empty iterable.

_Failure_: This method results in a failure in any situation where `actual` does not result in an
iterable, or where it results in an iterable that contains members.

#### Comparisons.have\_keys:
(_caller_, _actual_, _expected_

_Success_: This method results in a success if `actual` is a dictionary that a member for _every_
key listed in `expected`.

_Failure_: This method results in a failure in any situation where `actual` is not a dictionary,
or any situation where one or more values given in `expected` does not have a matching key.

#### Comparisons.have\_attributes:
(_caller_, _actual_, _expected_

_Success_: This method results in a success if all of the names listed in `expected` can be 
matched to an attribute in the object given by evaluating `actual`.

_Failure_: This method results in a failure in any situation where one or more of the names given by
`expected` is not represented as an attribute on the `actual` result.

#### Comparisons.have\_methods:
(_caller_, _actual_, _expected_

_Success_: This method results in a success if all of the names listed in `expected` can be matched
to a method on the object returned by `actual`.

_Failure_: This method results in a failure in any situation where one or more of the names can not
be matched to a method on `actual`.


<div style="text-align: right">Copyright (c) 2019 Andrew DeWitt</div>
