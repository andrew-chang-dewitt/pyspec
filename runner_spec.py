from runner import *

# Describe a group of tests by defining a class that inherits from 
# Runner's Describe class
class Expectations(Describe):
    # then define a set of tests in that class' `test` method
    def test(self):
        # tests can be set up to expect a return value
        def can_expect_values():
            # which can be tested for by passing an expression to test to Runner's 
            # `expect()` function & asserting a value it should equal using `to(eq(...))`
            # read the following line like 'expect one plus one to equal two'
            expect(1 + 1).to(eq(2))
        # then use the `it()` method of your created child of Describe to 
        # name & store the test
        self.it('can expect values', can_expect_values)

        # tests can also be set up to expect a specific error class
        def can_expect_exceptions():
            # complicated expressions (or those that you want to defer the evaluation of
            # until the test is run) can be defined as a function within the test, 
            def divide_by_zero():
                return 1/0

            # then passed, uncalled, to `expect()`
            # to test for an expected error, use Runner's `raise_error()` method, 
            # giving it the expected error class
            # this line can be read like 'expect *expression* to raise a ZeroDivisionError'
            expect(divide_by_zero).to(raise_error(ZeroDivisionError))
        # all tests are named & stored using the same pattern
        self.it('can expect exceptions', can_expect_exceptions)

        # you can also test that a given test will always fail as expected
        # def correct_failure_type():
        #     expect(expect(1).to(eq(2))).to(raise_error(AssertionError))

# A group of tests is ran by initializing the defined class with a description, 
# then calling the `run()` method it inherits from `Describe`
Expectations('set expectations & test versus actual expression results').run()

# You can also define common variables for a group of tests
class Let(Describe):
    # this can be done any of a few of ways:

    # first, name a class variable & assign it a value
    five = 5

    # or second, define a class @property
    @property
    def five_prop(self): return 5

    # or third, define an instance variable in `__init__`
    def __init__(self, description):
        # this requires first calling Describe's init & passing `description`
        # otherwise the other methods of Describe won't be initialized in the right order
        super().__init__(description)

        # then you can name your instance variable & assign it a value
        self.five_inst = 5

    # then define your tests that may use these variables just as before
    def test(self):
        def available_inside_tests():
            # and refer to the common variable using `self.variable_name`
            expect(self.five).to(eq(5))
            expect(self.five_prop).to(eq(5))
            expect(self.five_inst).to(eq(5))
        self.it('available inside the tests', available_inside_tests)

Let('create local state for testing purposes').run()

# You can also have one group of tests inherit class & instance variables from
# another group of tests by passing the intended parent class 
# instead of Runner's `Describe` class
class Inherit(Let):
    def test(self):
        def see_inherited_variables():
            # then you can refer to it as if it were a variable of this class
            # instance:
            expect(self.five).to(eq(5))
            # class:
            expect(self.five_prop).to(eq(5))
            expect(self.five_inst).to(eq(5))
        self.it('see inherited variables', see_inherited_variables)

        # you can even modify the inherited instance & class variables without
        # modifying it in the parent test group class
        def modify_inherited_variables():
            self.five_inst = 6
            expect(self.five_inst).to(eq(6))
        self.it('modify inherited variables', modify_inherited_variables)

        # unmodified variables from the parent test group can be accessed directly
        def access_original_variable():
            # do this by initializing an instance of the parent & requesting 
            # it's instance variable directly with dot notation
            expect(Let('let').five_inst).to(eq(5))

            # or by initializing it & assigning it to a variable, then
            # using it as needed
            let = Let('let')
            six = let.five_inst + 1
            expect(six).to(eq(6))
        self.it('access original variable from parent', access_original_variable)

        # but original values are not changed in the parent test group
        def original_values_unchanged():
            expect(Let('let').five_inst).to(eq(5))
        self.it("won't change original values in parent", original_values_unchanged)

Inherit('inherit state from a parent test group').run()
