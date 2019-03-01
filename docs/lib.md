PySpec Library API
==================

There are two top level functions exposed by the PySpec Library:

##### pyspec.describe(_description_, _metastructure=None_, _outergroup=None_):

Initializes & returns a **Describe()** object with the given _description_. If given,
the returned Describe() object will be initialized with a _metastructure_ (an 
instance of _[SpectStruct]()_ for making the Describe object available to the PySpec
CLI tools, and/or an _outergroup_ that this Describe object will be nested within 
(see _[class Describe.outer]()_ for more).

    Initilizes a new test group object using Describe

    Accepts:
    - description   (STRING)                a string describing the test group
    - [runner]      (SpecStruct instance)   a class used by the CLI to parse the test group
    - [outer]       (Describe instance)     another test group to inherit common state from, optional

    Returns:
    - An instance of Describe

##### pyspec.spec_struct():

Initializes & returns a **SpecStruct()** object for PySpec CLI parsing. This 
object can be passed to any Describe object on initialization to make the test
group available for the CLI tool to view, run, & print.

Describe class
--------------

The PySpec Library is organized with one core Class, Describe(). This class 
contains a series of inner classes that are used to create tests, encapsulate 
and share scope between tests & then run the tests. Describe objects can be 
nested indefinitely to inherit scope from an outer Describe object & organize 
testing groups as subsets of related test groups.

#### Test class

#### Should class

SpecStruct class
----------------
