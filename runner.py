import traceback

COLOR_GREEN = "\033[32m"
COLOR_RED = "\033[31m"
COLOR_RESET = "\033[0m"

def describe(description, outer=None):
    return Describe(description, outer)

class Describe:
    def __init__(self, description, outer=None):
        self.description = description
        self.tests = []
        self.inners = []
        self.base = ''
        self.tab = '  '
        self.tabplus = self.tab + '  '

        if outer is not None:
            self.outer = outer
            self.base = self.tab
            self.tab += '  '
            outer.inners.append(self)

    def it(self, description, code):
        test_obj = Test(description, code)
        self.tests.append(test_obj)

        return test_obj

    def run(self):
        print(f'{self.base}{self.description}')

        if self.inners is not None:
            for inner in self.inners: inner.run()

        for test in self.tests:
            print(f'{self.tab}- {test.name}', end='')

            if test.success == True:
                print(f': {COLOR_GREEN}ok{COLOR_RESET}')
            else:
                print(f': {COLOR_RED}fail{COLOR_RESET}')

                print(f'{self.tabplus}{COLOR_RED}* STACK TRACE{COLOR_RESET}')

                for line in test.tb[:-1]:
                    print(f'{self.tabplus}{COLOR_RED}|{COLOR_RESET} {line}')

                print(f'{self.tabplus}{COLOR_RED}* {test.tb[-1]}{COLOR_RESET}')

    def __getattr__(self, method_name):
        for key in dir(self.outer):
            if key == method_name:
                return getattr(self.outer, key)

        else: raise AttributeError(f'No such attribute: {method_name}')

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
