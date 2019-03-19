"""
Test runner for python, see runner_spec for example usage
"""

import traceback
from pub_sub import pub_sub

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
        used_pub_sub = pub_sub

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

        self.base = ''
        self.tab = '  '
        self.tabplus = self.tab + '  '

        if outer is not None:
            self.base = self.tab
            self.tab += '  '
            outer.inners.append(self)
        else:
            self.run = self._run

    # A short name is chosen as the method will be referenced very often by the
    # end user of this test runner; the pylint warning about name snake case
    # has been disabled.
    def it(self, description, code): # pylint: disable=invalid-name
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

        test_obj = Test(description, code)
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
            test_title = f'{self.tab}- {test.description}'

            if test.success:
                self.results.append(f'{test_title}: {COLOR_GREEN}ok{COLOR_RESET}')
            else:
                self.results.append(f'{test_title}: {COLOR_RED}fail{COLOR_RESET}')

                self.results.append(f'{self.tabplus}{COLOR_RED}* STACK TRACE{COLOR_RESET}')

                for line in test.stack_trace[:-1]:
                    self.results.append(f'{self.tabplus}{COLOR_RED}|{COLOR_RESET} {line}')

                self.results.append(
                    f'{self.tabplus}{COLOR_RED}* {test.stack_trace[-1]}{COLOR_RESET}'
                )

        if not muted:
            for line in self.results:
                print(line)

        pub_sub.topic('test group results').pub(self.results)
        return self.results

    def __getattr__(self, method_name):
        def doesnt_exist():
            raise AttributeError(f'No such attribute: {method_name}')

        if method_name in ('run', 'outer'):
            return doesnt_exist()

        if self.outer:
            for key in dir(self.outer):
                if key == method_name:
                    return getattr(self.outer, key)

        return doesnt_exist()

# ignoring too-few-public-methods pylint warning as Test class is a data structure with
# inner classes that expose all necessary methods
class Test: # pylint:disable=too-few-public-methods
    """
    An object used to represent a single test.

    On initialization, it takes:
    - description   (STRING)        a description to print when running the test,
                                    should be descriptive, readable, & concise
    - code          (FUNCTION)      a function to be run when the test is executed,
                                    the code must return a result to be handled by one
                                    of the methods given by Should
                    (EXPRESSION)    alternatively, code can be a non-callable value

    A test object also has the following attribute:
    - success   (BOOL)          represents if the test is successful or not,
                                value is set methods on Should

    A Test object also contains a Should object that makes Assertations &
    determines if the test passes or fails
    """

    def __init__(self, description, code):
        self.description = description
        self.code = code
        self.should = self._init_should()
        self.should_not = self._init_should_not()

    def _init_should(self):
        return self.Should(self.code, self)

    def _init_should_not(self):
        return self.ShouldNot(self.code, self)

    class Should:
        """
        An object containing methods for making Assertations of different types.
        An inner class to Test & always initialized when a Test instance is initialized.

        On initialization, it takes:
        - code          (FUNCTION)      a function that evaluates to an Actual result, to be
                                        compared against the Expected result using one of the
                                        methods of Should
                        (EXPRESSION)    alternatively, code can be a non-callable value
        - test_called   (Test)          the instance of Test that initialized this instance
                                        of Should

        Contains the following methods:
        - eq            compares the result of code to a given value, modifies test.success
                        accordingly, & returns the newly modified Test object
        - raise_error   compares the code result to an expected Exception class,
                        otherwise the same as eq
        """

        def __init__(self, code, test_called):
            self.code = code
            self.test_called = test_called

        def _code_result(self):
            return self.code() if callable(self.code) else self.code

        def _set_result(self, **kwargs):
            if kwargs['success']:
                self.test_called.success = True
            else:
                self.test_called.success = False
                self.test_called.err = kwargs['err']
                self.test_called.stack_trace = kwargs['stack_trace']

        # A short name is chosen as the method will be referenced very often by the
        # end user of this test runner; the pylint warning about name snake case
        # has been disabled.
        def eq(self, expected): # pylint: disable=invalid-name
            """
            Compares _code_result() to expected, modifies the outer Test instance's
            success attribute accordingly, & returns the newly modified Test instance
            """

            try:
                code_result = self._code_result()

                if not code_result == expected:
                    raise AssertionError(f'expected {expected}, but got {code_result}')

                self._set_result(success=True)

            # All exceptions are caught in order to continue parsing other tests.
            # Caught exceptions are stored at the Test instance's `err` & `stack_trace`
            # attributes & will be displayed in the test failure message
            except Exception as err: # pylint: disable=broad-except
                self._set_result(
                    success=False,
                    err=err,
                    stack_trace=traceback.format_exc().splitlines()
                )

            return self.test_called

        def raise_error(self, expected_err):
            """
            Compares _code_result() to expected_err, modifies the outer Test instance's
            success attribute accordingly, & returns the newly modified Test instance
            """

            try:
                code_result = self._code_result()

                no_err_msg = f'No error was raised, instead got {code_result}'
                self._set_result(
                    success=False,
                    err=no_err_msg,
                    stack_trace=[no_err_msg]
                )

            # All exceptions are caught in order to continue parsing other tests.
            # Caught exceptions are stored at the Test instance's `err` & `stack_trace`
            # attributes & will be displayed in the test failure message
            except Exception as err: # pylint: disable=broad-except
                # disabling pylint warning on typecheck as the only test that should
                # pass is if the exact specified error is passed, not any children of
                # the exception class
                if not type(err) == expected_err: # pylint: disable=unidiomatic-typecheck
                    # AssertionErrors are re-raised if the type of error does not match
                    # the expected error class, these will be caught in the next block
                    raise AssertionError(f'expected {expected_err}, but got {err}')

                self._set_result(success=True)

            # Assertion Errors are caught after the general `except Exception` clause
            # as the Assertion error should be raised by the previous, more general clause
            except AssertionError as err: # pylint: disable=bad-except-order
                self._set_result(
                    success=False,
                    err=err,
                    stack_trace=traceback.format_exc().splitlines()
                )

            return self.test_called

        def be_a(self, expected_class):
            """
            Compares _code_result() to expected_class & changes outer Test instance's
            success attribute to True if they match, or False if they don't.
            """

            try:
                code_result = self._code_result()

                if not isinstance(code_result, expected_class):
                    raise AssertionError(f'expected {expected_class}, but got {type(code_result)}')

                self._set_result(success=True)

            except Exception as err: # pylint: disable=broad-except
                self._set_result(
                    success=False,
                    err=err,
                    stack_trace=traceback.format_exc().splitlines()
                )

            return self.test_called

        def include(self, *args):
            """
            Requires `self._code_result()` to return an iterable.
            Checks all object names given in `*args` against the iterable & returns a
            successful test if they are found; otherwise returns a failing test with
            a list of what objects weren't found.
            """

            try:
                actual_groups = self._code_result()
                expected_groups = args

                not_found = []

                for item in expected_groups:
                    if item not in actual_groups:
                        not_found.append(item)

                if not_found:
                    raise AssertionError(f'expected {expected_groups}, but got {actual_groups}')

                self._set_result(success=True)

            except TypeError:
                raise TypeError(f'the result of the test is not an iterable')

            except Exception as err: # pylint: disable=broad-except
                self._set_result(
                    success=False,
                    err=err,
                    stack_trace=traceback.format_exc().splitlines()
                )

            return self.test_called

        def be_empty(self):
            """
            Requires `self._code_result()` to return an iterable.
            Checks if the iterable is empty. If it is, the test passes; otherwise an
            AssertionError is raised indicating a failed test.
            """

            try:
                actual = self._code_result()

                if len(actual) > 0:
                    raise AssertionError(f'expected an empty iterable, but got {actual}')

                self.test_called.success = True

            except TypeError:
                raise TypeError(f'the result of the test is not an iterable')

            except Exception as err: # pylint: disable=broad-except
                self._set_result(
                    success=False,
                    err=err,
                    stack_trace=traceback.format_exc().splitlines()
                )

            return self.test_called

        def have_keys(self, *args):
            """
            Requires the tested code to result in a dictionary.
            Checks the dictionary for any keys given in *args.
            """

            try:
                result_dict = self._code_result()

                if not isinstance(result_dict, dict):
                    raise TypeError(f'the result of the test is not a dictionary')

                actual_keys = result_dict.keys()
                expected_keys = args

                not_found = []

                for item in expected_keys:
                    if item not in actual_keys:
                        not_found.append(item)

                if not_found:
                    raise AssertionError(f'expected {expected_keys}, but got {actual_keys}')

                self._set_result(success=True)

            except Exception as err: # pylint: disable=broad-except
                self._set_result(
                    success=False,
                    err=err,
                    stack_trace=traceback.format_exc().splitlines()
                )

            return self.test_called

        def have_attributes(self, *args):
            """
            Checks a given object for the attributes given as arguments.
            """

            try:
                result = self._code_result()
                actual_keys = dir(result)
                expected_keys = args

                not_found = []

                for item in expected_keys:
                    if item not in actual_keys:
                        not_found.append(item)

                if not_found:
                    raise AssertionError(f'expected {expected_keys}, but got {actual_keys}')

                self._set_result(success=True)

            except Exception as err: # pylint: disable=broad-except
                self._set_result(
                    success=False,
                    err=err,
                    stack_trace=traceback.format_exc().splitlines()
                )

            return self.test_called

        def have_methods(self, *args):
            """
            Checks a given object for the methods given as arguments.
            """

            try:
                result = self._code_result()
                actual_keys = []

                for attribute in dir(result):
                    if callable(getattr(result, attribute)):
                        actual_keys.append(attribute)

                expected_keys = args

                not_found = []

                for item in expected_keys:
                    if item not in actual_keys:
                        not_found.append(item)

                if not_found:
                    raise AssertionError(f'expected {expected_keys}, but got {actual_keys}')

                self._set_result(success=True)

            except Exception as err: # pylint: disable=broad-except
                self._set_result(
                    success=False,
                    err=err,
                    stack_trace=traceback.format_exc().splitlines()
                )

            return self.test_called

    class ShouldNot(Should):
        """
        ShouldNot inherits all comparison methods (e.g. `eq()`, `be_a()`, etc.), but
        negates the result. It redefines only one attribute/method, _set_result, by
        setting the opposite result compared to the same function in `Should`.

        An inner class to Test & always initialized when a Test instance is initialized.
        """
        def _set_result(self, **kwargs):
            incorrect_success = (
                f'The test passed when it should have failed in a should_not statement'
            )

            if kwargs['success']:
                self.test_called.success = False
                self.test_called.err = incorrect_success
                self.test_called.stack_trace = [incorrect_success]
            else:
                self.test_called.success = True

    # class BooleanShould(Should):
    #     """
    #     BooleanShould inherits all comparison methods, just like ShouldNot, but it
    #     also modifies the test to take multiple pending results, then determines the final
    #     result using standard boolean rules combining each pending result.

    #     For example, if BooleanShould is initialized with 'and' passed to it, then
    #     it will give a final result of `Test.success = True` only if BOTH pending
    #     results succeeded, otherwise the final result will be false.

    #     An inner class to Test & always initialized when a Test instance is initialized.
    #     """

    #     def __init__(self, option):
    #         super().__init__()
    #         self.pending_results = [self.test_called.result]
    #         self.test_called.result = self.get_results
    #         self.option = option

    #     def get_results(self):
    #         """
    #         This method is used to compile results according to the option stored at
    #         self.option
    #         """
    #         is_and = True if self.option == 'and' else False
    #         is_or = True if self.option == 'or' else False

    #         for result in pending_results:
    #             if not result.success and is_and:
    #                 msg = f'One of the tests failed in the and_should statement'

    #                 return self._set_result(
    #                     success=False
    #                     err=msg
    #                     stack_trace=[msg]
    #                 )
    #             elif not result.success and is_or:
