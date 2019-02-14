import traceback

COLOR_GREEN = "\033[32m"
COLOR_RED = "\033[31m"
COLOR_RESET = "\033[0m"

def expect(actual):
    return Actual(actual)

def raise_error(exception_class):
    return Expectations.Error(exception_class)

def eq(expected):
    return Expectations.Equal(expected)

class Describe:
    def __init__(self, description, parent=None):
        self.description = description
        self.tests = {}
        self.tab = '\t'

        if not parent is None:
            self.parent = parent
            self.tab = self.parent.tab + self.tab

    def it(self, name, block):
        self.tests[name] = block

    def run(self):
        print(self.description)
        self.test()

        for test in self.tests:
            print(f'  - {test}', end='')
            try:
                self.tests[test]()
                print(f': {COLOR_GREEN}ok{COLOR_RESET}')
            except Exception as e:
                print(f': {COLOR_RED}fail{COLOR_RESET}')

                tb = traceback.format_exc().splitlines()

                print(f'{self.tab}{COLOR_RED}* STACK TRACE{COLOR_RESET}')

                for line in tb[:-1]:
                    print(f'{self.tab}{COLOR_RED}|{COLOR_RESET} {line}')

                print(f'{self.tab}{COLOR_RED}* {tb[-1]}{COLOR_RESET}')

class Actual:
    def __init__(self, actual):
        self.actual = actual

    def to(self, expectation):
        return expectation.run(self.actual) 

class Expectations:
    def __init__(self):
        self.Equal = Equal

    def err_msg(actual, expected):
        return f"Expected {expected}, but got {actual}"

    class Equal:
        def __init__(self, expected):
            self.expected = expected

        def run(self, actual):
            try:
                actual_res = actual() if callable(actual) else actual 
            except Exception as e:
                actual_res = type(e)

            assert actual_res == self.expected, err_msg(actual_res, self.expected)

    class Error:
        def __init__(self, exception_class):
            self.exception_class = exception_class

        def run(self, actual):
            try:
                actual_res = actual() if callable(actual) else actual 
            except Exception as e:
                actual_res = type(e)

            assert actual_res == self.exception_class, err_msg(actual_res, self.exception_class)

class AssertionError(Exception):
    def __init__(self, expected, actual):
        super().__init__(f"Expected {expected}, but got {actual}")
