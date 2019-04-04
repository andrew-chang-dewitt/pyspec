import os
import sys
import glob
import importlib.machinery
from types import ModuleType
from pyspec.lib.runner import runner
# from pyspec.cli import click_cust
from pub_sub import stable

class RunTests:
    CWD = os.getcwd()
    # ugly sys.path hack, necessary to allow tests to correctly import any
    # local modules in their package
    sys.path.append(CWD)

    def __init__(self, pub_sub=stable.event('pyspec')):
        self.results = None
        self.pub_sub = pub_sub
        self.runner = None

    def all_tests(self, test_dir_str, muted=False):
        self._publish_runner()
        self._get_directory(test_dir_str)

        self.pub_sub.topic('run results').sub(self._results_received)
        self.pub_sub.topic('run requested').pub(muted)

        return self.results

    def one_file(self, file_path_str, muted=False):
        self._publish_runner()

        self._import_module(file_path_str)
        self.pub_sub.topic('run results').sub(self._results_received)
        self.pub_sub.topic('run requested').pub(muted)

        return self.results

    def explore(self, test_dir_str, muted=False):
        self._publish_runner()
        self._get_directory(test_dir_str)
        res = []

        for group in self.runner.test_groups:
            res.append(group)

        return res

    def _import_module(self, name, full_path=False):
        path = name if full_path else self.CWD + '/' + name + '.py'

        # using SourceFileLoader & .exec_module from this answer on SO:
        # https://stackoverflow.com/a/19011259/4642869
        loader = importlib.machinery.SourceFileLoader(name, path)
        module = ModuleType(loader.name)
        loader.exec_module(module)

        return module

    def _get_directory(self, test_dir_str):
        path = self.CWD + '/' + test_dir_str + '/*_spec.py'
        spec_files = glob.glob(path)

        for spec_file in spec_files:
            self._import_module(spec_file, True)

        return True

    def _publish_runner(self):
        self.runner = runner(self.pub_sub)
        self.pub_sub.topic('runner').pub(self.runner)

        return self.runner

    def _results_received(self, results):
        self.results = results

        return bool(self.results is not None)
