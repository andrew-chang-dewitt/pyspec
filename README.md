PySpec
======
A barebones BDD style test runner for python 

Loosely inspired by RSpec, PySpec is intended for use in a behavior-driven 
development workflow (although it may work for unit testing, depending on 
your needs). It includes a testing library & a basic CLI tool. 
PySpec is a work in progress. 

Contents
--------

- [Installation](#installation)
- [Quickstart](#quickstart)
  - [Basic example](#basic-example)
  - [Adding CLI support](#adding-cli-support)
- [Documentation](#documentation)
  - [Library API](/docs/lib.md)

[//]: # (FIXME: CLI manual still needs to be created & uploaded)

Installation
------------

Currently, the only installation option is through self-installation using 
`git clone` & `pip install .`. In the future, installation may be made available 
via distribution on PyPi. 

To install **PySpec**, first cd to the directory of your choosing. For 
this example, we are installing to ~/test. Then, install from git using pip:

```bash
user@host:~/test $ pip install git+https://github.com/andrew-dewitt/pyspec.git
```

Confirm the CLI installed correctly & is available at your path using  
`pyspec --version`, which should return the following: 

```bash
user@host:~/pyspec $ pyspec -V
PySpec: version 1.1.0
--------------------------------------------
a barebones BDD style test runner for python
```

Quickstart
----------


The simplest use case is to write spec files intended to be directly called 
by python, without any support for the CLI tool.

### Basic example

Writing a test script begins with **describing** a test group, then 
adding tests to **it** using `describe()` & `Describe.it()`. To do this, first 
import `describe` from `pyspec` & any modules your are testing & assign 
pyspec.describe & pyspec.Comparisons some names:

```python
import pyspec
import example

describe = pyspec.describe
C = pyspec.Comparisons
```

Next, use PySpec's `describe()` method, giving it a short description of 
the test group, & assign it to a variable. 

```python
group = describe('this is a test group')
```

This returns an instance of `Describe` & assigns it to `group`. To create a 
test, use the `it()` method from `Describe` with a short description of the 
test as the only argument.

```python
group.it('this test will pass')
```

The `it()` method returns a Test object, with an attribute `expect` that is
used to indicate what code you are testing. `Test.expect` requires a callable
object as its argument, but if you need to pass only an expression or value, 
you can simply wrap it in a `lambda`.

```python
group.it('this test will pass').expect(lambda: 1)          # more methods to follow ...
group.it('this test will also pass').expect(some_function) # ...
```

To state what the _expected_ value that the _actual_ passed to `Test.expect` should, 
result in (or not result in), use `Test.to` or `Test.to_not`:

```python
group.it('normal testing').expect(lambda: 1).to(C.eq, 1)       # pass `eq` from `pyspec.Comparisons`
group.it('negative testing').expect(lambda: 1).to_not(C.eq, 2) # use `to_not` to negate a result
```

To test something from a module you've written, refer to it by the name you 
imported it as above, & pass the desired expression or function as your 
second argument to `it`. 

```python
group.it('This test is from `example.py`').expect(example.two).to(eq, 2)
group.it(
    'Another test from `example.py`'
).expect(
    example.divide_by_zero
).to(C.raise_error, ZeroDivisionError)
```

Lastly, to run this example, you just need to call `Describe`'s `run()` 
method on `group`, like this:

```python
group.run()
```

Then, run this script using `$ python example_spec.py`, which will 
return the following:

```bash
$ python example_spec.py

This is a test group
  - normal testing ok
  - negative testing ok
  - This test is from `example.py` ok
  - Another test from `example.py` ok
```

At the end, your `example_spec.py` should look like this:

```python
import pyspec
import example

describe = pyspec.describe
C = pyspec.Comparisons

group = describe('this is a test group')

group.it('normal testing').expect(lambda: 1).to(C.eq, 1)       # pass `eq` from `pyspec.Comparisons`
group.it('negative testing').expect(lambda: 1).to_not(C.eq, 2) # use `to_not` to negate a result
group.it('This test is from `example.py`').expect(example.two).to(eq, 2)
group.it(
    'Another test from `example.py`'
).expect(
    example.divide_by_zero
).to(C.raise_error, ZeroDivisionError)

group.run()
```

Running tests on an `example.py`: 

```python
def two():
    return 2

def divide_by_zero():
    return 1 / 0
```

With a file structure like this: 

```
.
|__ example.py
|__ example_spec.py

```

### Adding CLI support

To add CLI support to the above example, a few small changes need to
be made.

First, another method needs imported from the PySpec library: 
`spec_struct`. This method builds a meta structure of the spec file
that is used by the CLI tools to parse & run the tests. Add the following
import statement between `from pyspec import describe` & `import example` 
in `example_spec.py`

```python
from pyspec import describe
from pyspec import spec_struct
import example

...
```

Next, a SpectStruct object needs to be initialized using the `spect_struct()`
method after `import example`

```python 
...

import example

RUNNER = spect_struct()

group = describe('...
```

Then, the newly created SpectStruct object, `RUNNER` needs passed as the 
second argument each time a test group is described:

```python
...

RUNNER = spect_struct()

group = describe('this is a test group', RUNNER)

...
```

Lastly, you must remove the last line, `group.run()`, of `example_spec.py` 
as `Describe.run()`will now be invoked by the CLI through the metastructure 
RUNNER. Alternatively, you can guard the line by wrapping it in an `if` 
statement checking if the file is imported, or ran directly:

```python
...

if __name__ == '__main__':
    group.run()
```

Now, you should be able to run the spec using the CLI command `one`, 
referring to `example_spec` in your arguments:

```bash
user@host:~/example $ pyspec one example_spec

This is a test group
  - this test will pass ok
  - Two should be an instance of Int ok
  - This test is from `example.py` ok
  - Another test from `example.py` ok
```

### Using the PySpec CLI

The two most general commands are `all` & `one`.

#### All

`$ pyspec all <PATH>`

Runs all tests in a given directory. The argment given as `<PATH>` must be relative to 
the current working directory. This command will only find files in the given 
directory that end in `_spec.py`.

#### One

`$ pyspec one <MODULE>`

Runs the specified test file given as a module name. `<MODULE>` must be just the file
name, without any file type extensions.

#### See more

For more information on using the CLI, try `$ pyspec --help` for general help text 
or `$pyspec <command> --help` for more specific assistance.


Documentation
-------------

For more detailed information on using the PySpec Library, see the [API Documentation](/docs/lib.md). Currently, no documentation for the CLI tool exists outside of `$ pyspec --help`, but more detailed documentation will be completed later.
