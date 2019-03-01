PySpec Library API
==================

There are two top level functions exposed by the PySpec Library:

### pyspec.describe(_description_, _metastructure=None_, _outergroup=None_):

Initializes & returns **Describe()** object

### pyspec.spec_struct():

The PySpec Library is organized with one core Class, Describe(). This class 
contains a series of inner classes that are used to create tests, encapsulate 
and share scope between tests & then run the tests. Describe objects can be 
nested indefinitely to inherit scope from an outer Describe object & organize 
testing groups as subsets of related test groups.


