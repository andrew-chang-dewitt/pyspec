PySpec Library API
==================

Contents
--------

- Top level functions
  - [pyspec.describe](#pyspecdescribe)
  - [pyspec.spec\_struct](#pyspecspec_struct)
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
- [Comparisons class](#should-class)
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
- [Runner class](#runner-class)
  - [Attributes](#attributes-2)
  - [Methods](#methods-3)
    - [Runner.run\_all](#runnerrun_all)
    - [Runner.run\_one](#runnerrun_one)
    - [Runner.add\_group](#runneradd_group)
    - [Runner.remove\_group](#runnerremove_group)

There are two top level functions exposed by the PySpec Library:

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

#### pyspec.runner:
(*alt_pub_sub=None*)

Initializes & returns a **Runner()** object for PySpec CLI parsing. The Describe object 
has no awareness of the Runner object and has no direct interface with it. The Runner 
object depends upon an understanding of the structure of Describe & Test.

_Accepts_:

- [`alt_pub_sub`] \(pub\_sub.Event instance) an Event module to publish & subscribe to
  used to receive Describe objects from `pyspec.describe` & commands from the CLI tool

_Returns_: An instance of the Runner class with an empty `test_groups` attribute.


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

- description (STRING)

  a description to print when running the test, should be descriptive, readable, & concise

- comparison (pyspec.Comparisons)

  the method to be used for comparing the actual result to the expected value of the Test

- actual (FUNCTION)

  a function to be executed when evaluating the test, returns the 'actual' value

- expected (EXPRESSION)

  an expression that evaluates to the expected value that will be compared to `actual`

- self.error (EXCEPTION)

  used to store any error that is raised before a test is ran; this error will later be
  re-raised at test run time

- results (DICT)

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
  the results will compared to their expected value

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
TEST.it('can add numbers').expect(lambda: 1 + 1) # more methods to come ...
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

#### Test.to\_not

#### Test.run


Comparisons class
------------

An class that stores methods used to evaluate expressions or functions passed to 
[Test.expect](#testexpect) & make a comparison of ACTUAL vs. EXPECTED values. 
Exposes a series of methods that each offer different types of comparisons.

### Methods:

Each of the following methods is used to make an assertation about the ACTUAL result the code 
passed to `Test` will evaluate to versus the EXPECTED value given to the method. All of these 
methods will return the original Test object that the method was called on.

#### Comparisons.eq:
(_expected_)

Compares the evaluated result of `Test.code` to `expected` & modifies the outer Test 
instance's success attribute accordingly, then returns the newly modified Test instance. If 
`expected` does not equal `Test.code`'s result, then `Test.success` will be made to equal 
to False, otherwise it will be made to be equal to True.

_Accepts_:

- `expected` (EXPRESSION) a value that `Test.code` is expected to evaluate to.

#### Comparisons.raise\_error:
(_expected\_err_)

Compares the evaluated result of `Test.code` to `expected_err` & modifies the outer Test 
instance's success attribute accordingly, then returns the newly modified Test instance. 
If `expected_err` does not equal the error that should be raise by executing `Test.code` 
(or if `Test.code` does not raise an error when evaluated), then `Test.success` will be 
made to equal to False, otherwise it will be made to be equal to True.

_Accepts_:

- `expected_err` (EXPRESSION) A class of Exception that `Test.code` is expected to raise.

#### Comparisons.be\_a:
(_expected\_class_)

Compares the class of the evaluated result of `Test.code` to `expected_class` & modifies the 
outer Test instance's success attribute accordingly, then returns the newly modified Test 
instance. If `expected_class` does not equal `Test.code`'s result, then `Test.success` will 
be made to equal to False, otherwise it will be made to be equal to True.

_Accepts_:

- `expected_class` (EXPRESSION) a class that the evaluated result of `Test.code` is
  expected to be a member of.

#### Comparisons.include:
(_expected\_member_)

Checks if `expected_member` is a member of a collection returned by the evaluated result of 
`Test.code` & modifies the outer Test instance's success attribute accordingly, then returns 
the newly modified Test instance. If `expected_member` is not a member of the collection, or if 
`Test.code` does not evaluate to a collection searchable using Python's `if member in collection`, 
then `Test.success` will be made to be False. If `expected_member` is found to be in the 
collection, then `Test.success` will be assigned a value of True.

_Accepts_:

- `member` (EXPRESSION) a value that is expected to be a member of the collection that `Test.code` 
  evaluates to.


SpecStruct class
----------------

The SpecStruct class is a separate part of the PySpec Library that is only necessary if you 
wish to use the PySpec CLI tool with your test scripts. The class is used by passing an instance 
to **[pyspec.describe()](#pyspecdescribe)** when creating a test group.

### Attributes:

- `test_groups` (LIST) SpecStruct initializes with just one attribute: test_groups. All groups will be stored here. A list is used because it preserves member order with a numbered index & is easily searchable. This list starts as empty, but each time a SpecStruct instance is passed to **[pyspec.describe()](#pyspecdescribe)** the resulting **[Describe()](#describe-class) will also be added to this list.

### Methods:

SpecStruct exposes the following methods for consumption by the CLI.

#### SpecStruct.run\_all:

This function is the single entry point for running all tests held in
`test_groups`. This allows any other program interfacing with the library
to not need to know anything about how individual test groups are
structured.

`SpecStruct.run_all()` accepts no arguments & returns no results.

#### SpecStruct.run\_one:
(group)

A simple wrapper to a Describe object's `run()` method. Includes a
guard against calling `run()` on an inner test group since this would
result in an AttributeError.

_Accepts_: 

- `group` (Describe instance) The Describe instance for the single group of 
  tests you wish to run.

`SpecStruct.run_one()` returns no results.

<div style="text-align: right">Copyright (c) 2019 Andrew DeWitt</div>
