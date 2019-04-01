#! /usr/bin/env python
"""tests for SpecStruct metastructure"""

import pyspec
from pub_sub import stable

C = pyspec.Comparisons

STATS_OBJ = pyspec.describe('generate stats info in the runner metastructure')

test_run = pyspec.cli.run_tests.RunTests(stable.event('temp spec')).one_file(
    'tests/test_examples/temp_spec',
    True
)

STATS_OBJ.let('test_run', test_run)

STATS_OBJ.it(
    'has a stats object'
).expect(
    lambda: STATS_OBJ.test_run.stats
).to(C.be_a, pyspec.lib.runner.StatsObj)

STATS_OBJ.it(
    'tracks number the number of tests'
).expect(
    lambda: STATS_OBJ.test_run.stats.number_of_tests
).to(C.eq, 2)

STATS_OBJ.it(
    'tracks the success/failure rate'
).expect(
    lambda: STATS_OBJ.test_run.stats.success_failure_rate
).to(C.eq, .5)

STATS_OBJ.it(
    'tracks time on spec_struct() using methods on Stats class'
).expect(
    lambda: STATS_OBJ.test_run.stats
).to(
    C.have_methods,
    'start_time_tracking',
    'stop_time_tracking'
)

STATS_OBJ.it(
    'tracks time elapsed for running tests'
).expect(
    lambda: STATS_OBJ.test_run.stats.total_time_elapsed > 0
).to(C.eq, True)

if __name__ == '__main__':
    STATS_OBJ.run()
