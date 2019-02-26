import os
import importlib.machinery
import types
from pyspec.api.runner import Describe
from types import ModuleType

def all_tests(test_dir_str, is_dir):
    # test_dir = importlib.import_module(test_dir_str)
    test_dir = _get_module(test_dir_str, is_dir)

    for mod in dir(test_dir):
        mod_obj = getattr(test_dir, mod)
        if isinstance(mod_obj, ModuleType):
            print('\n' + f'running module {mod}')
            _run(mod_obj)

def one_file(file_path_str):
    # mod_obj = importlib.import_module(file_path_str)
    mod_obj = _get_module(file_path_str)
    _run(mod_obj)

def _get_module(name, is_dir=False, given_extension=None):
    cwd = os.getcwd()
    
    if given_extension is not None:
        extension = given_extension
    elif is_dir:
        extension = ''
    else:
        extension = '.py'
        
    path = cwd + '/' + name + extension

    # using SourceFileLoader & .exec_module from this answer on SO:
    # https://stackoverflow.com/a/19011259/4642869
    loader = importlib.machinery.SourceFileLoader(name, path)
    module = types.ModuleType(loader.name)
    loader.exec_module(module)

    return module

def _run(mod):
    for item in dir(mod):
        item_obj = getattr(mod, item)
        if isinstance(item_obj, Describe) and not hasattr(item_obj, 'outer'):
            item_obj.run()
