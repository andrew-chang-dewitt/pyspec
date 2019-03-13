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
    test_group.it('this will fail', 1).should.eq(2)
    runner.run_all(True)

    return runner

STATS_OBJ.test_run = test_run

STATS_OBJ.it(
    'has a stats object',
    lambda: STATS_OBJ.test_run().stats
).should.be_a(pyspec.lib.metastructure.StatsObj)

STATS_OBJ.it(
    'tracks number the number of tests',
    lambda: STATS_OBJ.test_run().stats.number_of_tests
).should.eq(2)

STATS_OBJ.it(
    'tracks the success/failure rate',
    lambda: STATS_OBJ.test_run().stats.success_failure_rate
).should.eq(.5)

STATS_OBJ.it(
    'tracks time on spec_struct() using methods on Stats class',
    STATS_OBJ.test_run().stats
).should.have_methods('start_time_tracking', 'stop_time_tracking')

STATS_OBJ.it(
    'tracks time elapsed for running tests',
    lambda: STATS_OBJ.test_run().stats.total_time_elapsed > 0
).should.eq(True)
