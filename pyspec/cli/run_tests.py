import os
import sys
import glob
import importlib.machinery
from types import ModuleType
from pyspec import runner
# from pyspec.cli import click_cust
from pub_sub import stable

PUB_SUB = stable.event('pyspec')

CWD = os.getcwd()
# ugly sys.path hack, necessary to allow tests to correctly import any
# local modules in their package
sys.path.append(CWD)

def all_tests(test_dir_str, passed_pub_sub=None, muted=False):
    used_pub_sub = _passed_pub_sub(passed_pub_sub)
    _publish_runner(passed_pub_sub)

    path = CWD + '/' + test_dir_str + '/*_spec.py'
    spec_files = glob.glob(path)

    for spec_file in spec_files:
        _import_module(spec_file, True)

    used_pub_sub.topic('run requested').pub(muted)

    return True

def one_file(file_path_str, passed_pub_sub=None, muted=False):
    used_pub_sub = _passed_pub_sub(passed_pub_sub)
    _publish_runner(passed_pub_sub)

    _import_module(file_path_str)
    used_pub_sub.topic('run requested').pub(muted)

    return True

def _import_module(name, full_path=False):
    path = name if full_path else CWD + '/' + name + '.py'

    # using SourceFileLoader & .exec_module from this answer on SO:
    # https://stackoverflow.com/a/19011259/4642869
    loader = importlib.machinery.SourceFileLoader(name, path)
    module = ModuleType(loader.name)
    loader.exec_module(module)

    return module

def _passed_pub_sub(passed):
    if passed is None:
        return PUB_SUB

    return passed

def _publish_runner(passed):
    if passed is None:
        return PUB_SUB.topic('runner').pub(runner())

    return passed.topic('runner').pub(runner(passed))
