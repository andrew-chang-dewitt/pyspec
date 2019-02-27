import os
import sys
import glob
import importlib.machinery
from types import ModuleType
from pyspec.api.runner import Describe

cwd = os.getcwd()
# ugly sys.path hack, necessary to allow tests to correctly import any
# local modules in their package
sys.path.append(cwd)

def all_tests(test_dir_str):
    path = cwd + '/' + test_dir_str + '/*_spec.py'
    spec_files = glob.glob(path)
    print(f'spec_files: {spec_files}')

    for spec_file in spec_files:
        mod_obj = _get_module(spec_file, True)
        _run(mod_obj)

def one_file(file_path_str):
    mod_obj = _get_module(file_path_str)
    _run(mod_obj)

def _get_module(name, full_path=False):
    path = name if full_path else cwd + '/' + name + '.py'

    # using SourceFileLoader & .exec_module from this answer on SO:
    # https://stackoverflow.com/a/19011259/4642869
    loader = importlib.machinery.SourceFileLoader(name, path)
    module = ModuleType(loader.name)
    loader.exec_module(module)

    return module

def _run(mod):
    for item in dir(mod):
        item_obj = getattr(mod, item)
        if isinstance(item_obj, Describe) and not hasattr(item_obj, 'outer'):
            item_obj.run()
