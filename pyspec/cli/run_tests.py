import os
import glob
import importlib.machinery
from types import ModuleType
from pyspec.api.runner import Describe

cwd = os.getcwd()

def all_tests(test_dir_str):
    print('running all_tests()')
    path = cwd + '/' + test_dir_str + '/*_spec.py'
    print(f'searching in {path}')
    spec_files = glob.glob(path)
    print(f'spec_files found: {spec_files}')

    for spec_file in spec_files:
        print(f'fetching {spec_file}')
        mod_obj = _get_module(spec_file, True)
        print(f'running')
        _run(mod_obj)

def one_file(file_path_str):
    mod_obj = importlib.import_module(file_path_str)
    _run(mod_obj)

def _get_module(name, full_path=False):
    
    if full_path:
        path = name
    else:
        path = cwd + '/' + name + '.py'

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
