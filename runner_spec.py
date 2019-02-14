from runner import *

### EXPECTATIONS ###
# Describe a group of tests by defining a class that inherits from 
# Runner's Describe class
# class Expectations(Describe):
expectations = describe('set expectations')

# tests can be set up to expect a return value
expectations.it('can expect values',
    # which can be tested for by passing a function as the second argument to 
    # `it()`; functions are required to deferr the execution of any passed expression
    # read the following line as one plus one should equal two
    1 + 1).should.eq(2)

# tests can also be set up to expect a specific error class
expectations.it('can expect exceptions',
    lambda: 1/0).should.raise_error(ZeroDivisionError)

# A group of tests is ran by calling it's `run()` method
expectations.run()

### COMMON###
# You can also define common variables for a group of tests
common = Describe('set common state')

# this is done by creating new attributes on the test group
common.five = 5
# you can assign simple values (or values from expressions) as above,
# or you can define a function & assign it as a new method
def five_mthd(): return 5
common.five_mthd = five_mthd

common.it('can use common attributes',
    common.five).should.eq(5)

common.it('can use common methods',
    common.five_mthd).should.eq(5)

common.run()

### FAILURES ###
# you can also test that a given test will always fail as expected
failures = describe('communicate failures')

# to do this, first create a failing test
failures.fail = Describe('failure').it('should fail', 1).should.eq(2)

# create a new function to deferr re-raising the error
def failed():
    # & grab the error off the test result object & re-raise it
    raise failures.fail.err

# then assign that function to a method on common state for the test group
failures.failed = failed
# you can grab just the error message from the args attribute of the returned error
failures.failed_msg = failures.fail.err.args[0]

# lastly, call it on the common method as the expected value with
# AssertionError as the error that should be raised by the failing test
failures.it('can show the expected error type',
    failures.failed).should.raise_error(AssertionError)

failures.it('can show the expected error message',
    failures.failed_msg).should.eq('expected 2, but got 1')

failures.run()

# 
# # You can also have one group of tests inherit class & instance variables from
# # another group of tests by passing the intended parent class 
# # instead of Runner's `Describe` class
# class Inherit(Let):
#     def test(self):
#         def see_inherited_variables():
#             # then you can refer to it as if it were a variable of this class
#             # instance:
#             expect(self.five).to(eq(5))
#             # class:
#             expect(self.five_prop).to(eq(5))
#             expect(self.five_inst).to(eq(5))
#         self.it('see inherited variables', see_inherited_variables)
# 
#         # you can even modify the inherited instance & class variables without
#         # modifying it in the parent test group class
#         def modify_inherited_variables():
#             self.five_inst = 6
#             expect(self.five_inst).to(eq(6))
#         self.it('modify inherited variables', modify_inherited_variables)
# 
#         # unmodified variables from the parent test group can be accessed directly
#         def access_original_variable():
#             # do this by initializing an instance of the parent & requesting 
#             # it's instance variable directly with dot notation
#             expect(Let('let').five_inst).to(eq(5))
# 
#             # or by initializing it & assigning it to a variable, then
#             # using it as needed
#             let = Let('let')
#             six = let.five_inst + 1
#             expect(six).to(eq(6))
#         self.it('access original variable from parent', access_original_variable)
# 
#         # but original values are not changed in the parent test group
#         def original_values_unchanged():
#             expect(Let('let').five_inst).to(eq(5))
#         self.it("won't change original values in parent", original_values_unchanged)
# 
# Inherit('inherit state from a parent test group').run()
