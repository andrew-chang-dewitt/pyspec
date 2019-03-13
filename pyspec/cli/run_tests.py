import os
import sys
import glob
import importlib.machinery
from types import ModuleType
from pyspec.cli import click_cust

CWD = os.getcwd()
# ugly sys.path hack, necessary to allow tests to correctly import any
# local modules in their package
sys.path.append(CWD)

def all_tests(test_dir_str):
    path = CWD + '/' + test_dir_str + '/*_spec.py'
    spec_files = glob.glob(path)

    for spec_file in spec_files:
        mod_obj = _get_module(spec_file, True)
        _run(mod_obj)

    return True

def one_file(file_path_str):
    mod_obj = _get_module(file_path_str)
    _run(mod_obj)

    return True

def _get_module(name, full_path=False):
    path = name if full_path else CWD + '/' + name + '.py'

    # using SourceFileLoader & .exec_module from this answer on SO:
    # https://stackoverflow.com/a/19011259/4642869
    loader = importlib.machinery.SourceFileLoader(name, path)
    module = ModuleType(loader.name)
    loader.exec_module(module)

    return module

def _run(mod):
    try:
        mod.RUNNER.run_all()
    except AttributeError:
        raise click_cust.NoRunnerError(mod.__name__)
