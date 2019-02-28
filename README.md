pyspec
======
A barebones BDD style test runner for python

Loosley inspired by RSpec, pyspec is intended for use in a behavior-driven
development workflow (although it may work for unit testing, depending on
your needs). It includes a testing library & a basic CLI tool.
Pyspec is a work in progress.

Installation
------------

Currently, the only installation option is through self-installation using 
`git clone` & `pip install .`. In the future, installation may be made available
via distribution on PyPi.

To install **pyspec**, first clone this repo in the directory of your choosing. For
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
pyspec: version 0.1.0
--------------------------------------------
a barebones BDD style test runner for python
```
