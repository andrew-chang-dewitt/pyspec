PySpec Library API
==================

There are two top level functions exposed by the PySpec Library:

#### pyspec.describe:
(_description_, _metastructure=None_, _outergroup=None_)

Initializes & returns a **Describe()** object with the given _description_. If given,
the returned Describe() object will be initialized with a _metastructure_ (an 
instance of _[SpectStruct](#specstruct-class)_ for making the Describe object available 
to the PySpec CLI tools, and/or an _outergroup_ that this Describe object will be 
nested within (see _[class Describe.outer](#describe-class)_ for more).

Accepts:

- `description` (STRING) a string describing the test group
- [`runner`] \(SpecStruct instance) a class used by the CLI to parse the test group, optional
- [`outer`] \(Describe instance) another test group to inherit common state from, optional

Returns: An instance of Describe

#### pyspec.spec_struct:

Initializes & returns a **SpecStruct()** object for PySpec CLI parsing. This 
object can be passed to any Describe object on initialization to make the test
group available for the CLI tool to view, run, & print.

_**Arguments**_: None
Returns: An instance of the SpecStruct class with an empty `test_groups` attribute.


Describe class
--------------

The PySpec Library is organized with one core Class, **[Describe()](#describe-class)**. 
This class references a few other classes that are used to create tests 
(**[Test()](#test-class)**) & optionally make tests available to the PySpec CLI tools 
(**[SpecStruct()](#specstruct-class)**). Describe objects can be nested indefinitely 
to inherit scope from an outer Describe object & organize testing groups as subsets of 
related test groups. 


### Attributes:

- `description` (STRING)

  a string describing the test group

- `inners` (LIST)			

  an empty list where any nested test groups will be stored

- `outer` (Describe instance), optional

  another test group to inherit common state from, optional
  
- `runner` (SpecStruct instance), optional 
  
  a class used by the CLI to parse the test group, optional

- `tests` (LIST)			

  an empty list where each test function will be stored

- `base`, `tab`, & `tabplus` (STRING)		
  
  strings used to increment tabs for results printing


### Methods:

The Describe class has two methods used to create new tests & run all tests 
included in the `tests` attribute list.

#### Describe.it:
(_description_, _code_)

A method used to create a new test in the group, adds an instance of Test to
the self.tests list and returns it.

Accepts:

- `description` (STRING) a short description to be printed when the test is ran
- `code` (EXPRESSION) a python expression to be executed & have the result used as 
the ACTUAL value to be compared against an EXPECTED value.

Returns: An instance of Test(), an inner class on Describe()

_**Example usage:**_

```python
test_group_instance.it('can add 1', some_script.add_one(1)) # more methods follow...
```

#### Describe.\_run:

A method used to run the test group & any inners, accessed via the 
Describe.run attribute (which will only exist for instances with no
Describe.outer attribute).

`Describe._run` accepts no arguments & has no returns.


Test class
----------

An instance of the Test class is created with each call to 
**[Describe.it()](describeitdescription-code)**. This class is used to store a 
test's description, code, & success [attributes](#test-attributes) & exposes an 
inner class, [Should()](#should-class), used to make assertations & evaluate 
results (stored at Test.result).

### Attributes:

- `description` (STRING) 

  A description to print when running the test. It should be descriptive, 
  readable, & concise

- `code` (FUNCTION -or- EXPRESSION)

  A function to be run when the test is executed, the code must return a result 
  to be handled by one. Alternatively, code can be a non-callable expression such as 
  `1 + 1` or a variable name where a value desired to be tested is stored.

- `should` (Should instance)

  An attribute pointing to an instance of [Should()](#should-class), allowing for more
  concise & readable syntax when writing tests.

After a test has been run, the Test object will also have the following attribute: 

- `success` (BOOL)

  Represents if the test is successful or not, the value is set by methods on 
  [Should()](#should-class). This attribute will not exist until after a method on Should()
  has been used to evaluate the result (or value) of Test().code (the ACTUAL value) against 
  an EXPECTED value given later.


Should class
------------

An inner class on [Test()](#test-class) used to evaluate expression or function passed to 
_Test().code_ & make a comparison of ACTUAL vs. EXPECTED values. Exposes a series of methods 
that each offer different types of comparisons.

### Methods:

Each of the following methods is used to make an assertation about the ACTUAL result the code 
passed to `Test` will evaluate to versus the EXPECTED value given to the method. All of these 
methods will return the original Test object that the method was called on.

#### Should.eq:
(_expected_)

Compares the evaluated result of `Test.code` to `expected` & modifies the outer Test 
instance's success attribute accordingly, then returns the newly modified Test instance. If 
`expected` does not equal `Test.code`'s result, then `Test.success` will be made to equal 
to False, otherwise it will be made to be equal to True.

Accepts:

- `expected` (EXPRESSION) a value that `Test.code` is expected to evaluate to.

#### Should.raise\_error:
(_expected\_err_)

Compares the evaluated result of `Test.code` to `expected_err` & modifies the outer Test 
instance's success attribute accordingly, then returns the newly modified Test instance. 
If `expected_err` does not equal the error that should be raise by executing `Test.code` 
(or if `Test.code` does not raise an error when evaluated), then `Test.success` will be 
made to equal to False, otherwise it will be made to be equal to True.

Accepts:

- `expected_err` (EXPRESSION) A class of Exception that `Test.code` is expected to raise.

#### Should.be\_a:
(_expected\_class_)

Compares the class of the evaluated result of `Test.code` to `expected_class` & modifies the 
outer Test instance's success attribute accordingly, then returns the newly modified Test 
instance. If `expected_class` does not equal `Test.code`'s result, then `Test.success` will 
be made to equal to False, otherwise it will be made to be equal to True.

Accepts:

- `expected_class` (EXPRESSION) a class that the evaluated result of `Test.code` is
  expected to be a member of.

#### Should.include:
(_expected\_member_)

Checks if `expected_member` is a member of a collection returned by the evaluated result of 
`Test.code` & modifies the outer Test instance's success attribute accordingly, then returns 
the newly modified Test instance. If `expected_member` is not a member of the collection, or if 
`Test.code` does not evaluate to a collection searchable using Python's `if member in collection`, 
then `Test.success` will be made to be False. If `expected_member` is found to be in the 
collection, then `Test.success` will be assigned a value of True.

Accepts:

- `member` (EXPRESSION) a value that is expected to be a member of the collection that `Test.code` 
  evaluates to.


SpecStruct class
----------------

The SpecStruct class is a separate part of the PySpec Library that is only necessary if you 
wish to use the PySpec CLI tool with your test scripts. The class is used by passing an instance 
to **[pyspec.describe()](#pyspecdescribe)** when creating a test group.

    SpecStruct initializes with just one attribute: test_groups.
    All groups will be stored here. A list is used because it preserves
    member order with a numbered index & is easily searchable.
