import importlib
from app.runner import Describe
from types import ModuleType

def all_tests(test_dir_str):
    test_dir = importlib.import_module(test_dir_str)

    for mod in dir(test_dir):
        mod_obj = getattr(test_dir, mod)
        if isinstance(mod_obj, ModuleType):
            print('\n', f'running module {mod}')
            _run(mod_obj)

def one_file(file_name):
    mod_obj = getattr(tests, file_name)
    _run(mod_obj)

def _run(mod):
    for item in dir(mod):
        item_obj = getattr(mod, item)
        if isinstance(item_obj, Describe) and not hasattr(item_obj, 'outer'):
            item_obj.run()
