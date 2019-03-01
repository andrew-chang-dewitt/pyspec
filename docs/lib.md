PySpec Library API
==================

There are two top level functions exposed by the PySpec Library:

#### pyspec.describe(_description_, _metastructure=None_, _outergroup=None_):

Initializes & returns a **Describe()** object with the given _description_. If given,
the returned Describe() object will be initialized with a _metastructure_ (an 
instance of _[SpectStruct](#specstruct-class)_ for making the Describe object available 
to the PySpec CLI tools, and/or an _outergroup_ that this Describe object will be 
nested within (see _[class Describe.outer](#describe-class)_ for more).

    Initilizes a new test group object using Describe

    Accepts:
    - description   (STRING)                a string describing the test group
    - [runner]      (SpecStruct instance)   a class used by the CLI to parse the test
                                            group, optional
    - [outer]       (Describe instance)     another test group to inherit common state
                                            from, optional

    Returns:
    - An instance of Describe

#### pyspec.spec_struct():

Initializes & returns a **SpecStruct()** object for PySpec CLI parsing. This 
object can be passed to any Describe object on initialization to make the test
group available for the CLI tool to view, run, & print.

    Used to initialize a new SpecStruct instance. This is the only function
    directly exposed by the API from this module.

    Arguments: 	None
    Returns: 	An instance of the SpecStruct class with an empty 
    		test_groups attribute.


Describe class
--------------

The PySpec Library is organized with one core Class, Describe(). This class 
contains a series of inner classes that are used to create tests, encapsulate 
and share scope between tests & then run the tests. Describe objects can be 
nested indefinitely to inherit scope from an outer Describe object & organize 
testing groups as subsets of related test groups.


### Attributes:

- **description** (STRING)

  a string describing the test group

- **inners** (LIST)			

  an empty list where any nested test groups will be stored

- **outer** (Describe instance), optional

  another test group to inherit common state from, optional
  
- **runner** (SpecStruct instance), optional 
  
  a class used by the CLI to parse the test group, optional

- **tests** (LIST)			

  an empty list where each test function will be stored

- **base**, **tab**, & **tabplus** (STRING)		
  
  strings used to increment tabs for results printing


### Methods:

The Describe class has two methods used to create new tests & run all tests 
included in the `tests` attribute list.

#### Describe.it(_description_, _code_):

A method used to create a new test in the group, adds an instance of Test to
the self.tests list and returns it.

    Accepts:
    
    - description (STRING)  a short description to be printed when the test is ran
    - code (EXPRESSION)     a python expression to be executed & have the result 
                            used as the ACTUAL value to be compared against an 
                            EXPECTED value

    Returns:

    An instance of Test(), an inner class on Describe()

_**Example usage:**_

```python
test_group_instance.it('can add 1', some_script.add_one(1)) # more methods follow...
```

#### Describe._run():

A method used to run the test group & any inners, accessed via the 
Describe.run attribute (which will only exist for instances with no
Describe.outer attribute).

Describe._run accepts no arguments & has no returns.


### Inner classes:

#### Test class

#### Should class

SpecStruct class
----------------

    SpecStruct initializes with just one attribute: test_groups.
    All groups will be stored here. A list is used because it preserves
    member order with a numbered index & is easily searchable.
