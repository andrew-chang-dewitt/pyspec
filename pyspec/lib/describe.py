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

def describe(description, outer=None, alt_pub_sub=None):
    """
    Initilizes a new test group object using Describe

    Accepts:
    - description   (STRING)                a string describing the test group
    - [runner]      (SpecStruct instance)   a class used by the CLI to parse the test
                                            group, optional
    - [outer]       (Describe instance)     another test group to inherit common state
                                            from, optional

    Returns:
    - An instance of Describe
    """

    group = Describe(description, outer)

    if alt_pub_sub:
        used_pub_sub = alt_pub_sub
    else:
        used_pub_sub = PUB_SUB

    if outer is None:
        used_pub_sub.topic('new test group').pub(group)

    return group

class Describe:
    """
    A class to describe a new test group

    On initialization, accepts:
    - description           (STRING)                see above
    - [runner]              (SpecStruct instance)   a class used by the CLI to parse the test group
    - [outer]               (Describe instance)     see above, optional

    Returns: An instance of Describe with the following attributes & methods, plus those above:
    - tests                 (LIST)      an empty list where each test function will be stored
    - inners                (LIST)      an empty list where any nested test groups will be stored
    - base, tab, & tabplus  (STRING)    strings used to increment tabs for results printing
    - it                    (METHOD)    a method used to create a new test in the group,
                                        adds an instance of Test to the self.tests list
    - [outer]               (Describe)  the outer test group, if nested, optional
    - [run]                 (METHOD)    a method used to run the test group & any inners,
                                        this one will only exist if it has no outer attribute

    This class has a modified __get_attr__() method used to inherit attributes & methods
    from the Describe object designated at self.outer (if there is one). It is used similarly
    to Ruby's method_missing.
    """

    def __init__(self, description, outer=None):
        self.description = description

        self.outer = outer
        self.tests = []
        self.inners = []
        self.results = []
        self.lets = {}

        self.base = ''
        self.tab = '  '
        self.tabplus = self.tab + '  '

        if outer is not None:
            self.base = self.tab
            self.tab += '  '
            outer.inners.append(self)
        else:
            self.run = self._run

    def let(self, name, value):
        """
        set common values
        """
        self.lets[name] = value

    # A short name is chosen as the method will be referenced very often by the
    # end user of this test runner; the pylint warning about name snake case
    # has been disabled.
    def it(self, description): # pylint: disable=invalid-name
        """
        A method used to create a new test in the group, adds an instance of Test to
        the self.tests list.

        Accepts:

        - description (STRING)  a short description to be printed when the test is ran
        - code (EXPRESSION)     a python expression to be executed & have the result
                                used as the ACTUAL value to be compared against an
                                EXPECTED value

        Returns:

        An instance of Test(), an inner class on Describe()
        """

        test_obj = Test(description, self.lets)
        self.tests.append(test_obj)

        return test_obj

    def _run(self, muted=False):
        """
        A method used to run the test group & any inners, accessed via the
        Describe.run attribute (which will only exist for instances with no
        Describe.outer attribute).

        Describe._run accepts no arguments & has no returns.
        """

        self.results = []

        self.results.append(f'{self.base}{self.description}')

        for inner in self.inners:
            # call to inner's protected run() method first to display any nested
            # test group's results before displaying the outer class results last
            inner._run(muted) # pylint: disable=protected-access

            for line in inner.results:
                self.results.append(line)

        for test in self.tests:
            test.run()
            test_title = f'{self.tab}- {test.description}'

            if test.result['success']:
                self.results.append(f'{test_title}: {COLOR_GREEN}ok{COLOR_RESET}')
            else:
                self.results.append(f'{test_title}: {COLOR_RED}fail{COLOR_RESET}')

                self.results.append(f'{self.tabplus}{COLOR_RED}* STACK TRACE{COLOR_RESET}')

                for line in test.result['stack_trace']:
                    self.results.append(f'{self.tabplus}{COLOR_RED}|{COLOR_RESET} {line}')

                err_text = test.result['err']
                err_name = err_text.__class__.__name__

                self.results.append(
                    f'{self.tabplus}{COLOR_RED}* {err_name}: {err_text}{COLOR_RESET}'
                )

        if not muted:
            for line in self.results:
                print(line)

        PUB_SUB.topic('test group results').pub(self.results)
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

    def __init__(self, description, lets):
        self.description = description
        self.comparison = lambda x, y, z: x
        self.actual = None
        self.expected = None
        self.result = {
            'success': None,
            'err': None,
            'stack_trace': None
        }

    def expect(self, actual):
        self.actual = Actual(self, actual)

        return self.actual

    def run(self):
        """
        execute the test

        accepts no args & returns the evaluated test with new values in self.result
        """
        try:
            if isinstance(self.comparison, Exception):
                raise self.comparison

            self.comparison(self, self.actual.result, self.expected)
            self._set_result(success=True)
        except Exception:
            exc_obj = sys.exc_info()[1]
            exc_tb = sys.exc_info()[2]

            self._set_result(
                success=False,
                err=exc_obj,
                stack_trace=traceback.format_tb(exc_tb)
            )

class Actual:
    # FIXME: improve docstring
    """
    - code          (FUNCTION)      a function to be run when the test is executed,
                                    the code must return a result to be handled by one
                                    of the methods given by Should
                    (EXPRESSION)    alternatively, code can be a non-callable value
    """

    def __init__(self, calling_test, actual):
        self.calling_test = calling_test
        self.actual = actual

    def to(self, comparison_method, *args):
        def set_result(**kwargs):
            if kwargs['success']:
                self.calling_test.result['success'] = True
            else:
                self.calling_test.result['success'] = False
                self.calling_test.result['err'] = kwargs['err']
                self.calling_test.result['stack_trace'] = kwargs['stack_trace']

            return self.calling_test

        self.calling_test.comparison = comparison_method
        self.calling_test.expected = args
        self.calling_test.actual = self
        self.calling_test._set_result = set_result

        return self.calling_test

    def to_not(self, comparison_method, *args):
        def set_result(**kwargs):
            incorrect_success = (
                f'The test passed when it should have failed in a should_not statement'
            )

            if kwargs['success']:
                self.calling_test.result['success'] = False
                self.calling_test.result['err'] = incorrect_success
                self.calling_test.result['stack_trace'] = [incorrect_success]
            else:
                self.calling_test.result['success'] = True

            return self.calling_test

        self.calling_test.comparison = comparison_method
        self.calling_test.expected = args
        self.calling_test.actual = self
        self.calling_test._set_result = set_result

    def result(self):
        return self.actual() if callable(self.actual) else self.actual
