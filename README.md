pyspec
===
a barebones rspec style test runner for python

Super simple & not at all well-tested installation instructions:

1. clone this repo wherever you like
  `git clone git@github.com:andrew-dewitt/pyspec.git`
2. change directory to the repo root 
  `cd pyspec`
2. check out the release branch because none of the path installation 
    features for CLI or library are merged to master yet
  `git checkout release`
3. make sure your desired python environment is activated (if desired)
5. install the pyspec package locally
  `pip install .`
  use the `--editable` flag if you wish to make changes and/or contribute
  
You should now have pyspec installed in your chosen environment. It should be 
available as a CLI using `$ pyspec --help` & available to import as a python library 
using `import pyspec`.
