from app.runner import Describe
import tests
from types import ModuleType

def all_tests():
    for mod in dir(tests):
        mod_obj = getattr(tests, mod)
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

print('\n\nrunning all tests\n')
all_tests()

print('\n\nrunning one_file tests\n')
one_file('runner_spec')
