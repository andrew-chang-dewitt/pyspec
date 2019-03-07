"""tests for SpecStruct metastructure"""

import pyspec

RUNNER = pyspec.spec_struct()

STATS_OBJ = pyspec.describe('generate stats info in the runner metastructure', RUNNER)

def test_run():
    """
    Test run to get stats
    """
    runner = pyspec.spec_struct()
    test_group = pyspec.describe('test stats', runner)
    test_group.it('can do stuff', 1).should.eq(1)
    runner.run_all(True)

    return runner

STATS_OBJ.test_run = test_run

STATS_OBJ.it(
    'has a stats object',
    lambda: STATS_OBJ.test_run().stats
).should.be_a(pyspec.lib.metastructure.StatsObj)

STATS_OBJ.it(
    'that stats object has attributes for time, number of tests, & success/failure rates',
    lambda: STATS_OBJ.test_run().stats
).should.have_attributes(
    'total_time_elapsed',
    'number_of_tests',
    'success_failure_rate'
)

STATS_OBJ.it(
    'tracks time on spec_struct() using methods on Stats class',
    STATS_OBJ.test_run().stats
).should.have_methods('start_time_tracking', 'stop_time_tracking')

DISPLAY = pyspec.describe('display stats info to the user', RUNNER)

DISPLAY.test_run = test_run

DISPLAY.it(
    'prints stats on the last line of a test',
    lambda: DISPLAY.test_run().results[-1]
).should.eq('Total time:')
