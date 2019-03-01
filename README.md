PySpec
======
A barebones BDD style test runner for python 

Loosley inspired by RSpec, PySpec is intended for use in a behavior-driven 
development workflow (although it may work for unit testing, depending on 
your needs). It includes a testing library & a basic CLI tool. 
PySpec is a work in progress. 

Contents
--------

- [Installation](#installation)
- [Quickstart](#quickstart)
  - [Basic example](#basic-example)
  - [Adding CLI support](#adding-cli-support)
- Documentation
  - [Library API](/docs/lib.md)
  - [CLI manual](/docs/cli.md)

Installation
------------

Currently, the only installation option is through self-installation using 
`git clone` & `pip install .`. In the future, installation may be made available 
via distribution on PyPi. 

To install **PySpec**, first clone this repo in the directory of your choosing. For 
this example, we are installing to ~/pyspec. 

```bash
user@host:~/ $ git clone git@github.com:andrew-dewitt/pyspec.git
```

Then `cd` into the project root, activate your chosen python virtual 
environment (this example assumes virtualenv, installed at pyspec/env), & 
install using pip: 

```bash
user@host:~/ $ cd pyspec
user@host:~/pyspec $ source env/bin/activate
(env)
user@host:~/pyspec $ pip install .
```

Confirm the CLI installed correctly & is available at your path using  
`pyspec -V`, which should return the following: 

```bash
user@host:~/pyspec $ pyspec -V
PySpec: version 0.1.0
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
import `describe` from `pyspec` & any modules your are testing: 

```python
from pyspec import describe
import example
```

Next, use PySpec's `describe()` method, giving it a short description of 
the test group, & assign it to a variable. 

```python
group = describe('this is a test group')
```

This returns an instance of `Describe` & assigns it to `group`. To create a 
test, use the `it()` method from `Describe` with a short description of the 
test as the first argument. The second argument should be the expression 
being tested.

```python
group.it('this test will pass', 1)
```

The `it()` method returns a Test object, with an attribute `should` with 
methods such as `eq` & `raise_error`. These are used to make statements 
about what the second method passed to `it` should resolve to. For 
example, you can say 'One should equal one' by writing the following:

```python
group.it('this test will pass', 1).should.eq(1)
```

Or you could say 'Two should be an instance of `Int`' with:

```python
group.it('Two should be an instance of Int', 2).should.be_a(Int)
```

To test something from a module you've written, refer to it by the name you 
imported it as above, & pass the desired expression or function as your 
second argument to `it`. 

```python
group.it('This test is from `example.py`', example.two).should.eq(2)
group.it(
    'Another test from `example.py`',
    example.divide_by_zero
).should.raise_error(ZeroDivisionError)
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
  - this test will pass ok
  - Two should be an instance of Int ok
  - This test is from `example.py` ok
  - Another test from `example.py` ok
```

At the end, your `example_spec.py` should look like this:

```python
from pyspec import describe
import example

group = describe('this is a test group')

group.it('this test will pass', 1)
group.it('this test will pass', 1).should.eq(1)
group.it('Two should be an instance of Int', 2).should.be_a(Int)
group.it('This test is from `example.py`', example.two).should.eq(2)
group.it(
    'Another test from `example.py`',
    example.divide_by_zero
).should.raise_error(ZeroDivisionError)

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
