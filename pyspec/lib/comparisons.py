"""
Comparison methods
"""

class Comparisons:
    """
    The following methods are all functions that can be used in a test
    to compare an actual result (stored in the test at the `code`
    attribute) against the expected attribute (passed to each method).

    Typical usage will be to pass the method to a `should` or `should_not`
    call (above) as the first argument, with the expected value (that will
    be passed to this Comparison method) as the second argument. This
    structure allows the execution of the comparison to be deferred until
    the Test's `run` method is called.

    A short name is chosen as the method will be referenced very often by the
    end user of this test runner; the pylint warning about name snake case
    has been disabled.
    """

    def __getattr__(self, method_name):
        return NoComparison(method_name)

    @staticmethod
    def eq(caller, actual, expected_arr): # pylint: disable=invalid-name
        """
        Compares _code_result() to expected, modifies the outer Test instance's
        success attribute accordingly, & returns the newly modified Test instance
        """

        actual_result = actual()

        if len(expected_arr) > 1:
            raise Exception('Too many positional arguments given in expect.to()')

        expected = expected_arr[0]

        if not actual_result == expected:
            raise AssertionError(expected, actual_result)

        return caller

    @staticmethod
    def raise_error(caller, actual, expected_arr):
        """
        Compares _code_result() to expected_err, modifies the outer Test instance's
        success attribute accordingly, & returns the newly modified Test instance
        """

        if len(expected_arr) > 1:
            raise Exception('Too many positional arguments given in expect.to()')

        expected = expected_arr[0]

        try:
            actual_result = actual()

            raise AssertionError(message=f'No error was raised, instead got {actual_result}')

        # All exceptions are caught in order to continue parsing other tests.
        # Caught exceptions are stored at the Test instance's `err` & `stack_trace`
        # attributes & will be displayed in the test failure message
        except Exception as err: # pylint: disable=broad-except
            # disabling pylint warning on typecheck as the only test that should
            # pass is if the exact specified error is passed, not any children of
            # the exception class
            err_type = type(err)

            if not err_type == expected: # pylint: disable=unidiomatic-typecheck
                # AssertionErrors are re-raised if the type of error does not match
                # the expected error class, these will be caught in the next block
                raise AssertionError(expected, err_type)

        return caller

    @staticmethod
    def be_a(caller, actual, expected_arr):
        """
        Compares _code_result() to expected_class & changes outer Test instance's
        success attribute to True if they match, or False if they don't.
        """

        if len(expected_arr) > 1:
            raise Exception('Too many positional arguments given in expect.to()')

        expected_class = expected_arr[0]

        actual_result = actual()

        if not isinstance(actual_result, expected_class):
            raise AssertionError(expected_class, actual_result)

        return caller

    @staticmethod
    def include(caller, actual, expected_array):
        """
        Requires `self._code_result()` to return an iterable.
        Checks all object names given in `*args` against the iterable & returns a
        successful test if they are found; otherwise returns a failing test with
        a list of what objects weren't found.
        """

        try:
            actual_array = actual()

            not_found = []

            for item in expected_array:
                if item not in actual_array:
                    not_found.append(item)

            if not_found:
                raise AssertionError(expected_array, actual_array)

        except TypeError:
            raise TypeError(f'the result of the test is not an iterable')

        return caller

    @staticmethod
    def be_empty(caller, actual, expected_empty):
        """
        Requires `self._code_result()` to return an iterable.
        Checks if the iterable is empty. If it is, the test passes; otherwise an
        AssertionError is raised indicating a failed test.
        """

        if expected_empty:
            raise TypeError('Actual.to() be_empty must be the only argument when it is used')
        try:
            actual_result = actual()

            if len(actual_result) > 0:
                raise AssertionError(f'expected an empty iterable, but got {actual_result}')

        except TypeError:
            raise TypeError(f'the result of the test is not an iterable')

        return caller

    @staticmethod
    def have_keys(caller, actual, expected_keys):
        """
        Requires the tested code to result in a dictionary.
        Checks the dictionary for any keys given in *expected_keys.
        """

        actual_result = actual()

        if not isinstance(actual_result, dict):
            raise TypeError(f'the result of the test is not a dictionary')

        actual_keys = actual_result.keys()

        for item in expected_keys:
            if item not in actual_keys:
                raise AssertionError(expected_keys, actual_result)

        return caller

    @staticmethod
    def have_attributes(caller, actual, expected_attributes):
        """
        Checks a given object for the attributes given as expected_attributes.
        """

        actual_result = actual()
        actual_keys = dir(actual_result)

        for item in expected_attributes:
            if item not in actual_keys:
                raise AssertionError(expected_attributes,actual_keys)

        return caller

    @staticmethod
    def have_methods(caller, actual, expected_methods):
        """
        Checks a given object for the methods given as expected_methods.
        """

        actual_result = actual()
        actual_methods = []

        for attribute in dir(actual_result):
            if callable(getattr(actual_result, attribute)):
                actual_methods.append(attribute)

        for item in expected_methods:
            if item not in actual_methods:
                raise AssertionError(expected_methods, actual_methods)

        return caller

class AssertionError(Exception):
    def __init__(self, expected=None, actual=None, **kwargs):
        try:
            msg = kwargs['message']
        except KeyError:
            if expected is not None and actual is not None:
                msg = f'expected {expected}, but got {actual}'
            else:
                msg = (
                    f'Unclear Assertion Error raised, pass `expected` & `actual` '
                    f'values as your first & second arguments or use a custom `message` '
                    f'keyword argument to improve error clarity'
                    f'\n'
                    f'You passed {expected} as expected & {actual} as actual'
                )

        super().__init__(msg)

class NoComparison(Exception):
    def __init__(self, method_name):
        msg = f'PySpec has no comparison method named {method_name}'
        super().__init__(msg)
