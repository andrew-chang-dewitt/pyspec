import traceback

COLOR_GREEN = "\033[32m"
COLOR_RED = "\033[31m"
COLOR_RESET = "\033[0m"

def describe(description):
    return Describe(description)

# def expect(test):
#     return Actual(test)
# 
# def eq(expected):
#     return Expectations.Equal(expected)

# def raise_error(exception_class):
#     return Expectations.Error(exception_class)

class Describe:
    def __init__(self, description, parent=None):
        self.description = description
        self.tests = []
        self.tab = '\t'

    def it(self, description, code):
        test_obj = Test(description, code)
        self.tests.append(test_obj)

        return test_obj

    def run(self):
        print(self.description)

        for test in self.tests:
            print(f'  - {test.name}', end='')

            if test.success == True:
                print(f': {COLOR_GREEN}ok{COLOR_RESET}')
            else:
                print(f': {COLOR_RED}fail{COLOR_RESET}')

                print(f'{self.tab}{COLOR_RED}* STACK TRACE{COLOR_RESET}')

                for line in test.tb[:-1]:
                    print(f'{self.tab}{COLOR_RED}|{COLOR_RESET} {line}')

                print(f'{self.tab}{COLOR_RED}* {test.tb[-1]}{COLOR_RESET}')

class Test:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.should = self.init_should()

    def init_should(self):
        return self.Should(self.code, self)

    class Should:
        def __init__(self, code, test_called):
            self.code = code
            self.test_called = test_called

        def _code_result(self):
            return self.code() if callable(self.code) else self.code

        def eq(self, expected):
            try:
                code_result = self._code_result()

                if not code_result == expected:
                    raise AssertionError(f'expected {expected}, but got {code_result}')

                self.test_called.success = True

            except Exception as err:
                self.test_called.success = False
                self.test_called.err = err
                self.test_called.tb = traceback.format_exc().splitlines()

            return self.test_called

        def raise_error(self, expected_err):
            try:
                code_result = self._code_result()

                self.test_called.success = False
                self.test_called.err = 'No error was raised'
                self.test_called.tb = ['No error was raised']

            except Exception as err:
                if not type(err) == expected_err:
                    raise AssertionError(f'expected {expected_err}, but got {err}')

                self.test_called.success = True

            except AssertionError as err:
                self.test_called.success = False
                self.test_called.err = err
                self.test_called.tb = traceback.format_exc().splitlines()

            return self.test_called

# class Actual:
#     def __init__(self, actual):
#         self.actual = actual
# 
#     def to(self, expectation):
#         return expectation.run(self.actual) 
# 
# class Expectations:
#     def __init__(self):
#         self.Equal = Equal
# 
#     def err_msg(actual, expected):
#         return f"Expected {expected}, but got {actual}"
# 
#     class Equal:
#         def __init__(self, expected):
#             self.expected = expected
# 
#         def run(self, actual):
#             try:
#                 actual_res = actual() if callable(actual) else actual 
#             except Exception as e:
#                 actual_res = type(e)
# 
#             try:
#                 assert actual_res == self.expected, Expectations.err_msg(
#                     actual_res,
#                     self.expected)
#             except AssertionError as e:
#                 return Expectations.Result(False, e)
# 
#             return Expectations.Result(True)
# 
#     class Error:
#         def __init__(self, exception_class):
#             self.exception_class = exception_class
# 
#         def run(self, actual):
#             try:
#                 actual_res = actual() if callable(actual) else actual 
#             except Exception as e:
#                 actual_res = type(e)
# 
#             assert actual_res == self.exception_class, Expectations.err_msg(
#                 actual_res,
#                 self.exception_class)
# 
#     class Result:
#         def __init__(self, success, name, err=None):
#             self.success = success
#             self.name = name
#             self.err = err
