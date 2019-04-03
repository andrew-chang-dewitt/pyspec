"""
Test runner for python, see runner_spec for example usage
"""

import sys
import traceback
from pub_sub import stable
from . import comparisons as Comparisons

PUB_SUB = stable.event('pyspec')

COLOR_GREEN = "\033[32m"
COLOR_RED = "\033[31m"
COLOR_RESET = "\033[0m"

def describe(description, alt_pub_sub=None):
    """
    Initilizes a new test group object using Describe

    Accepts:
    - description   (STRING)                a string describing the test group
    - [outer]       (Describe instance)     another test group to inherit common state
                                            from, optional

    Returns:
    - An instance of Describe
    """

    group = Describe(description)

    if alt_pub_sub:
        used_pub_sub = alt_pub_sub
    else:
        used_pub_sub = PUB_SUB

    used_pub_sub.topic('new test group').pub(group)

    return group

class Describe:
    """
    A class to describe a new test group

    On initialization, accepts:
    - description           (STRING)                see above

    Returns: An instance of Describe with the following attributes & methods, plus those above:
    - tests                 (LIST)      an empty list where each test function will be stored
    - [outer]               (Describe)  the outer test group, if nested, optional
    - inners                (LIST)      an empty list where any nested test groups will be stored
    - results               (LIST)      an empty list where test results are stored by `run`
    - base, tab, & tabplus  (STRING)    strings used to increment tabs for results printing
    - let                   (METHOD)    set common values to be shared between all tests in a group
    - before                (METHOD)    set values to be re-evaluated before each test
    - it                    (METHOD)    a method used to create a new test in the group,
                                        adds an instance of Test to the self.tests list
    - [run]                 (METHOD)    a method used to run the test group & any inners,
                                        this one will only exist if it has no outer attribute

    This class has a modified __get_attr__() method used to inherit attributes & methods
    from the Describe object designated at self.outer (if there is one). This is what allows
    a form of prototypical inheritance between test groups.
    """

    def __init__(self, description):
        self.description = description

        self.tests = []
        self.__outer = None
        self.inners = []
        self.results = []
        self.lets = {}
        self.befores = {}

        self.base = ''
        self.tab = '  '
        self.tabplus = self.tab + '  '

    def let(self, name, value):
        """
        set common values to be shared between all tests in a group
        """
        self.lets[name] = value

    def before(self, name, value):
        """
        set values to be re-evaluated before each test
        """
        self.befores[name] = value

    # A short name is chosen as the method will be referenced very often by the
    # end user of this test runner; the pylint warning about name snake case
    # has been disabled.
    def it(self, description): # pylint: disable=invalid-name
        """
        A method used to create a new test in the group, adds an instance of Test to
        the self.tests list.

        Accepts:

        - description (STRING)  a short description to be printed when the test is ran

        Returns:

        An instance of Test()
        """

        test_obj = Test(description, self.befores)
        self.tests.append(test_obj)

        return test_obj

    def describe(self, description):
        """
        Method used for creating an inner test group on an existing group.
        """
        inner = Describe(description)
        self.inners.append(inner)
        inner.outer = self

        inner.base = self.tab
        inner.tab += '  '
        inner.tabplus = inner.tab + '  '

        return inner

    @property
    def outer(self):
        """
        Property containing a reference to an outer test group. Defaults to None
        """
        return self.__outer

    @outer.setter
    def outer(self, outer):
        if isinstance(outer, Describe):
            self.__outer = outer
        else:
            raise TypeError(f'{outer} is not an instance of {Describe}')

    def run(self, muted=False, verbose=False):
        """
        Runs all tests within a group, so long as it is not an inner group.
        """

        if self.outer is not None:
            return None

        return self._run(muted, verbose)

    def _run(self, muted=False, verbose=False):
        """
        A method used to run the test group & any inners, accessed via the
        Describe.run attribute (which will only exist for instances with no
        Describe.outer attribute).

        Describe._run accepts no arguments & has no returns.
        """

        self.results = []

        self.results.append(f'{self.base}{self.description}')

        for inner in self.inners:
            # pass outer befores to inner
            for key, value in self.befores.items():
                # only if not already defined on the inner
                if key not in inner.befores:
                    inner.befores[key] = value

            # call to inner's protected run() method first to display any nested
            # test group's results before displaying the outer class results last
            inner._run(True, verbose) # pylint: disable=protected-access

            for line in inner.results:
                self.results.append(line)

        for test in self.tests:
            # setup befores
            for key, value in self.befores.items():
                setattr(self, key, value)

            # run test
            test.run()

            # tear down befores
            # for key in self.befores:
            #     del get

            test_title = f'{self.tab}- {test.description}'

            # parse results & generate human readable results strings
            if test.result['success'] and verbose:
                self.results.append(f'{test_title}: {COLOR_GREEN}ok{COLOR_RESET}')
            elif not test.result['success']:
                self.results.append(f'{test_title}: {COLOR_RED}fail{COLOR_RESET}')

                self.results.append(f'{self.tabplus}{COLOR_RED}* STACK TRACE{COLOR_RESET}')

                for line in test.result['stack_trace']:
                    self.results.append(f'{self.tabplus}{COLOR_RED}|{COLOR_RESET} {line}')

                err_text = test.result['err']
                err_name = err_text.__class__.__name__

                self.results.append(
                    f'{self.tabplus}{COLOR_RED}* {err_name}: {err_text}{COLOR_RESET}'
                )

        def total_num_nested(inners):
            """
            helper function to count number of inners in describe groups of an
            arbitrary nesting depth
            """
            if not inners:
                return 1
            return 1 + sum(total_num_nested(inner.inners) for inner in inners)

        recursive_length = total_num_nested(self.inners)
        # check if all tests passed & append 'ok' if true
        if len(self.results) == recursive_length:
            self.results[0] += f': {COLOR_GREEN}ok{COLOR_RESET}'

        # hide output if muted
        if not muted:
            for line in self.results:
                print(line)

        # publish results to any listener
        PUB_SUB.topic('test group results').pub(self.results)

        # return results to any handler that may have called _run
        return self.results

    def __getattr__(self, method_name):
        def doesnt_exist():
            raise AttributeError(f'No such attribute: {method_name}')

        if method_name in ('run', 'outer'):
            return doesnt_exist()

        try:
            return self.lets[method_name]
        except KeyError:
            if self.outer:
                try:
                    return self.outer.lets[method_name]
                except KeyError:
                    return doesnt_exist()

            return doesnt_exist()

class Test:
    """
    An object used to represent a single test.

    On initialization, it takes:
    - description   (STRING)        a description to print when running the test,
                                    should be descriptive, readable, & concise

    A test object also has the following attribute:
    - success   (BOOL)          represents if the test is successful or not,
                                value is set methods on Should

    A Test object also contains a Should object that makes Assertations &
    determines if the test passes or fails
    """

    def __init__(self, description, befores):
        self.description = description
        self.befores = befores
        self.comparison = None
        self.actual = None
        self.expected = None
        self.error = None
        self.result = {
            'success': None,
            'err': None,
            'stack_trace': None
        }

    def expect(self, actual):
        if callable(actual):
            self.actual = actual
        else:
            msg = 'Actual values must be callable so that execution is deferred until runtime.'

            self.error = Exception(msg)

        return self

    def to(self, comparison_method, *args):
        def set_result(**kwargs):
            if kwargs['success']:
                self.result['success'] = True
            else:
                self.result['success'] = False
                self.result['err'] = kwargs['err']
                self.result['stack_trace'] = kwargs['stack_trace']

            return self

        self.comparison = comparison_method
        self.expected = args
        self._set_result = set_result

        return self

    def to_not(self, comparison_method, *args):
        def set_result(**kwargs):
            incorrect_success = (
                f'The test passed when it should have failed in a should_not statement'
            )

            if kwargs['success']:
                self.result['success'] = False
                self.result['err'] = incorrect_success
                self.result['stack_trace'] = [incorrect_success]
            else:
                self.result['success'] = True

            return self

        self.comparison = comparison_method
        self.expected = args
        self._set_result = set_result

    def run(self):
        """
        execute the test

        accepts no args & returns the evaluated test with new values in self.result
        """
        try:
            if isinstance(self.comparison, Exception):
                raise self.comparison
            if self.error:
                raise self.error

            self.comparison(self, self.actual, self.expected)
            self._set_result(success=True)
        except Exception:
            exc_obj = sys.exc_info()[1]
            exc_tb = sys.exc_info()[2]

            self._set_result(
                success=False,
                err=exc_obj,
                stack_trace=traceback.format_tb(exc_tb)
            )
